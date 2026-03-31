"""
sign_service.py — Document signing and storage.

When a document is signed:
  1. The content is signed with the doctor's RSA private key.
  2. The content is also AES-256-GCM encrypted (for crypto-shredding support).
  3. The document record (with encrypted content) is stored in `documents`.
  4. The AES key is stored separately in `keys`.
  5. The action is logged in the audit trail.
"""

import uuid
from datetime import datetime, timezone

from fastapi import HTTPException, status

from app.db import doctors_col, documents_col, keys_col
from app.utils.crypto import sign_document as rsa_sign, encrypt_content, generate_symmetric_key
from app.utils.helpers import normalize
from app.services import audit_service


def sign_document(doctor_id: str, content: bytes, ip: str) -> dict:
    """
    Sign a document and store it in an encrypted form for crypto-shredding.

    Args:
        doctor_id: The signing doctor's short ID.
        content:   Plain-text document content.
        ip:        Client IP address for audit logging.

    Returns:
        {"message": "Document signed", "document_id": ..., "signature": ...}

    Raises:
        HTTPException 404 if doctor not found.
    """
    doctor_id = normalize(doctor_id)

    # Fetch doctor and private key
    doctor = doctors_col.find_one({"doctor_id": doctor_id})
    if not doctor:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Doctor not found.")

    private_key_pem = doctor["private_key"]

    # RSA signature over the plain-text content
    signature = rsa_sign(private_key_pem, content)

    # Symmetric encryption (AES-256-GCM) for crypto-shredding support
    sym_key   = generate_symmetric_key()
    encrypted = encrypt_content(sym_key, content)

    # Unique identifiers
    document_id = str(uuid.uuid4())
    key_id      = str(uuid.uuid4())

    # Persist the symmetric key separately
    keys_col.insert_one({
        "key_id": key_id,
        "key":    sym_key.hex(),          # store as hex string
    })

    # Persist the document (stores encrypted content, NOT plaintext)
    documents_col.insert_one({
        "document_id":       document_id,
        "doctor_id":         doctor_id,
        "encrypted_content": encrypted,
        "signature":         signature,
        "key_id":            key_id,
        "created_at":        datetime.now(timezone.utc).isoformat(),
    })

    # Audit
    audit_service.log_action(doctor_id, "SIGN", ip, document_id=document_id)

    return {
        "message":     "Document signed",
        "document_id": document_id,
        "signature":   signature,
    }

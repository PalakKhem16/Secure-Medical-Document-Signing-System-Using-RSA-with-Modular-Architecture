"""
shred_service.py — Crypto-shredding implementation.

Crypto-shredding concept:
  - Documents are stored in ENCRYPTED form (AES-256-GCM).
  - The encryption key is stored SEPARATELY in the `keys` collection.
  - Shredding = deleting only the key.
  - The encrypted document record remains (proof of existence),
    but the content can NEVER be recovered.
"""

from fastapi import HTTPException, status

from app.db import documents_col, keys_col
from app.services import audit_service
from app.utils.helpers import normalize


def shred_document(document_id: str, doctor_id: str, ip: str) -> dict:
    """
    Crypto-shred a document by destroying its encryption key.

    After shredding:
      - The document record still exists in MongoDB.
      - The encrypted_content field is permanently unreadable.
      - The key record is deleted and is unrecoverable.

    Args:
        document_id: UUID of the document to shred.
        doctor_id:   Requesting doctor (must own the document).
        ip:          Client IP for audit logging.

    Returns:
        {"status": "DATA UNRECOVERABLE", "document_id": ...}

    Raises:
        HTTPException 404 if document not found.
        HTTPException 403 if doctor does not own the document.
        HTTPException 410 if the key has already been shredded.
    """
    doctor_id   = normalize(doctor_id)
    document_id = normalize(document_id)

    # Locate the document
    doc = documents_col.find_one({"document_id": document_id})
    if not doc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Document not found.")

    # Ownership check
    if doc["doctor_id"] != doctor_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to shred this document.",
        )

    key_id = doc.get("key_id")
    if not key_id:
        raise HTTPException(
            status_code=status.HTTP_410_GONE,
            detail="Key reference missing. Document may already be shredded.",
        )

    # Verify the key still exists
    key_doc = keys_col.find_one({"key_id": key_id})
    if not key_doc:
        raise HTTPException(
            status_code=status.HTTP_410_GONE,
            detail="Encryption key not found. Document already shredded.",
        )

    # Delete the key — this is the shredding step
    keys_col.delete_one({"key_id": key_id})

    # Audit
    audit_service.log_action(doctor_id, "SHRED", ip, document_id=document_id)

    return {"status": "DATA UNRECOVERABLE", "document_id": document_id}

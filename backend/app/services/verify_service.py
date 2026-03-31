"""
verify_service.py — RSA signature verification.

Fetches the doctor's public key and verifies the provided signature
against the provided content.  Returns "VALID" or "TAMPERED".
"""

from fastapi import HTTPException, status

from app.db import doctors_col
from app.utils.crypto import verify_document as rsa_verify
from app.utils.helpers import normalize
from app.services import audit_service


def verify_document(doctor_id: str, content: bytes, signature: str, ip: str) -> dict:
    """
    Verify an RSA-signed document.

    Args:
        doctor_id: The doctor whose public key is used for verification.
        content:   Plain-text document content to verify.
        signature: Hex-encoded RSA signature.
        ip:        Client IP address for audit logging.

    Returns:
        {"status": "VALID"} or {"status": "TAMPERED"}

    Raises:
        HTTPException 404 if doctor not found.
    """
    doctor_id = normalize(doctor_id)
    signature = normalize(signature)

    # Fetch doctor and public key
    doctor = doctors_col.find_one({"doctor_id": doctor_id})
    if not doctor:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Doctor not found.")

    public_key_pem = doctor["public_key"]

    # RSA verification
    is_valid = rsa_verify(public_key_pem, content, signature)
    result   = "VALID" if is_valid else "TAMPERED"

    # Audit log
    audit_service.log_action(doctor_id, "VERIFY", ip)

    return {"status": result}

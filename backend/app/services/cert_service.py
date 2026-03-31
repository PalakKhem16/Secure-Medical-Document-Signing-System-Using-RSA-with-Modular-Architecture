"""
cert_service.py — Doctor certificate issuance.

Generates RSA key pairs, hashes passwords, assigns doctor IDs,
and persists new doctor records to MongoDB.
"""

import bcrypt
from datetime import datetime, timezone
from fastapi import HTTPException, status

from app.db import doctors_col
from app.utils.crypto import generate_rsa_keypair
from app.utils.helpers import generate_doctor_id, normalize


def issue_certificate(name: str, email: str, password: str) -> dict:
    """
    Issue a new doctor certificate (create a new doctor account).

    Steps:
      1. Normalize and validate inputs.
      2. Check email uniqueness.
      3. Generate a unique DOC-XXXX identifier.
      4. Generate RSA 2048-bit key pair.
      5. Hash the password with bcrypt.
      6. Persist the doctor record to MongoDB.

    Args:
        name:     Doctor's full name.
        email:    Doctor's email address (must be unique).
        password: Plain-text password (will be hashed).

    Returns:
        {"message": "Doctor created successfully", "doctor_id": <id>}

    Raises:
        HTTPException 409 if email is already registered.
    """
    name     = normalize(name)
    email    = normalize(email).lower()
    password = normalize(password)

    # Ensure email uniqueness
    if doctors_col.find_one({"email": email}):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="A doctor with this email already exists.",
        )

    # Generate a collision-resistant short doctor ID
    doctor_id = _unique_doctor_id()

    # RSA key pair generation
    private_pem, public_pem = generate_rsa_keypair()

    # bcrypt password hashing (salt is built-in)
    password_hash = bcrypt.hashpw(
        password.encode("utf-8"), bcrypt.gensalt()
    ).decode("utf-8")

    # Persist to MongoDB
    doctors_col.insert_one({
        "doctor_id":     doctor_id,
        "name":          name,
        "email":         email,
        "password_hash": password_hash,
        "public_key":    public_pem,
        "private_key":   private_pem,
        "created_at":    datetime.now(timezone.utc).isoformat(),
    })

    return {"message": "Doctor created successfully", "doctor_id": doctor_id}


#  Internal helpers 

def _unique_doctor_id(max_attempts: int = 20) -> str:
    """
    Generate a DOC-XXXX identifier guaranteed to be unique within the database.
    Retries up to `max_attempts` times in the rare case of a collision.
    """
    for _ in range(max_attempts):
        candidate = generate_doctor_id()
        if not doctors_col.find_one({"doctor_id": candidate}):
            return candidate
    raise HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail="Could not generate a unique doctor ID. Please try again.",
    )

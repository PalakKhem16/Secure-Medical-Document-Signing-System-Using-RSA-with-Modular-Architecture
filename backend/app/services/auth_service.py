"""
auth_service.py — Doctor authentication logic.

Handles login by verifying the bcrypt password hash stored in MongoDB.
"""

import bcrypt
from fastapi import HTTPException, status
from app.db import doctors_col
from app.utils.helpers import normalize


def login(doctor_id: str, password: str) -> dict:
    """
    Authenticate a doctor by ID and password.

    Args:
        doctor_id: Doctor's short ID (e.g. DOC-4821).
        password:  Plain-text password submitted at login.

    Returns:
        The doctor document (with keys) on success.

    Raises:
        HTTPException 401 if doctor not found or password mismatch.
    """
    doctor_id = normalize(doctor_id)
    password  = normalize(password)

    # Fetch doctor record
    doctor = doctors_col.find_one({"doctor_id": doctor_id})
    if not doctor:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid doctor ID or password.",
        )

    # Verify bcrypt hash
    if not bcrypt.checkpw(password.encode("utf-8"), doctor["password_hash"].encode("utf-8")):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid doctor ID or password.",
        )

    return doctor

"""
doctor_routes.py — Doctor self-service endpoints.

GET /doctor/{doctor_id}/profile   →  View profile + keys
GET /doctor/{doctor_id}/documents →  View signed documents list
"""

from fastapi import APIRouter, HTTPException, status
from app.db import doctors_col, documents_col

router = APIRouter()


@router.get("/{doctor_id}/profile")
def get_profile(doctor_id: str):
    """
    Return a doctor's profile including their RSA public and private keys.
    Private key is included so the doctor can inspect or back it up.
    """
    doctor = doctors_col.find_one({"doctor_id": doctor_id}, {"_id": 0, "password_hash": 0})
    if not doctor:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Doctor not found.")
    return doctor


@router.get("/{doctor_id}/documents")
def get_documents(doctor_id: str):
    """
    Return all documents signed by the given doctor, newest first.
    """
    doctor = doctors_col.find_one({"doctor_id": doctor_id})
    if not doctor:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Doctor not found.")

    docs = list(
        documents_col.find(
            {"doctor_id": doctor_id},
            {"_id": 0, "document_id": 1, "doctor_id": 1, "created_at": 1, "signature": 1}
        ).sort("created_at", -1)
    )
    return {"documents": docs}

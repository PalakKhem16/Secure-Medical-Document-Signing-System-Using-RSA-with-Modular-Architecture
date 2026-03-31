"""
admin_routes.py — Admin-only endpoints (no auth required in this prototype).

POST /admin/issue            →  Issue a new doctor certificate
GET  /admin/doctors          →  View all doctors
GET  /admin/logs             →  View all audit logs
GET  /admin/logs/{doctor_id} →  View logs for a specific doctor
"""

from fastapi import APIRouter
from app.models.doctor import CreateDoctorRequest
from app.services import cert_service, audit_service
from app.db import doctors_col

router = APIRouter()


@router.post("/issue")
def issue_certificate(payload: CreateDoctorRequest):
    """
    Create a new doctor account.
    Generates RSA keys, hashes password, assigns a unique DOC-XXXX ID.
    """
    result = cert_service.issue_certificate(
        name=payload.name,
        email=payload.email,
        password=payload.password,
    )
    return result


@router.get("/doctors")
def get_all_doctors():
    """
    Return a list of all registered doctors (safe fields only).
    """
    doctors = list(
        doctors_col.find(
            {},
            {"_id": 0, "doctor_id": 1, "name": 1, "email": 1, "created_at": 1}
        ).sort("created_at", -1)
    )
    return {"doctors": doctors}


@router.get("/logs")
def get_all_logs():
    """Return all audit trail entries, newest first."""
    return {"logs": audit_service.get_all_logs()}


@router.get("/logs/{doctor_id}")
def get_logs_by_doctor(doctor_id: str):
    """Return audit entries for a specific doctor."""
    return {"logs": audit_service.get_logs_by_doctor(doctor_id)}

"""
auth_routes.py — Authentication endpoints.

POST /auth/login  →  Doctor login
"""

from fastapi import APIRouter, Request
from app.models.doctor import LoginRequest
from app.services import auth_service, audit_service

router = APIRouter()


@router.post("/login")
def login(payload: LoginRequest, request: Request):
    """
    Authenticate a doctor with their doctor_id and password.

    Returns safe doctor info (excludes keys and password hash) on success.
    """
    ip = request.client.host

    doctor = auth_service.login(payload.doctor_id, payload.password)

    # Log successful login
    audit_service.log_action(doctor["doctor_id"], "LOGIN", ip)

    return {
        "message":   "Login successful",
        "doctor_id": doctor["doctor_id"],
        "name":      doctor["name"],
        "email":     doctor["email"],
    }

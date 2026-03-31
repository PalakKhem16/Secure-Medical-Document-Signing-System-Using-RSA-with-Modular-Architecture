"""
doctor.py — Pydantic models for doctor-related requests and responses.
"""

from pydantic import BaseModel, EmailStr


class CreateDoctorRequest(BaseModel):
    """Request body for issuing a new doctor certificate."""
    name: str
    email: str
    password: str


class LoginRequest(BaseModel):
    """Request body for doctor login."""
    doctor_id: str
    password: str


class DoctorOut(BaseModel):
    """Safe response model — excludes keys and password hash."""
    doctor_id: str
    name: str
    email: str
    created_at: str

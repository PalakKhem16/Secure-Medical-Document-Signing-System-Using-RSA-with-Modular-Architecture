"""
sign_routes.py — Document signing endpoint.

POST /sign  →  Sign a document with the doctor's RSA private key
"""

from fastapi import APIRouter, Request, File, Form, UploadFile
from app.services import sign_service

router = APIRouter()


@router.post("/")
def sign_document(
    request: Request,
    file: UploadFile = File(...),
    doctor_id: str = Form(...)
):
    """
    Sign a document and store it encrypted in MongoDB.

    Returns the RSA signature and the new document_id.
    """
    ip = request.client.host
    content_bytes = file.file.read()
    return sign_service.sign_document(doctor_id, content_bytes, ip)

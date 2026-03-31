"""
verify_routes.py — Document verification endpoint.

POST /verify  →  Verify an RSA signature against document content
"""

from fastapi import APIRouter, Request, File, Form, UploadFile
from app.services import verify_service

router = APIRouter()


@router.post("/")
def verify_document(
    request: Request,
    file: UploadFile = File(...),
    signature: str = Form(...),
    doctor_id: str = Form(...)
):
    """
    Verify a document signature using the doctor's RSA public key.

    Returns {"status": "VALID"} or {"status": "TAMPERED"}.
    """
    ip = request.client.host
    content_bytes = file.file.read()
    return verify_service.verify_document(
        doctor_id, content_bytes, signature, ip
    )

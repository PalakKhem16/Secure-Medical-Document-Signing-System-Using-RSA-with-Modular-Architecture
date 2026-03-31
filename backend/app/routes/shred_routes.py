"""
shred_routes.py — Crypto-shredding endpoint.

POST /shred  →  Destroy the encryption key for a document
"""

from fastapi import APIRouter, Request
from app.models.document import ShredRequest
from app.services import shred_service

router = APIRouter()


@router.post("/")
def shred_document(payload: ShredRequest, request: Request):
    """
    Crypto-shred a document by deleting its encryption key.

    The encrypted document record remains but can never be decrypted.
    Returns {"status": "DATA UNRECOVERABLE"}.
    """
    ip = request.client.host
    return shred_service.shred_document(payload.document_id, payload.doctor_id, ip)

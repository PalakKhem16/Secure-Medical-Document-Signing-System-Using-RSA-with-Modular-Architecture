"""
document.py — Pydantic models for document-related operations.
"""

from pydantic import BaseModel





class ShredRequest(BaseModel):
    """Request body for crypto-shredding a document."""
    document_id: str
    doctor_id: str


class DocumentOut(BaseModel):
    """Safe output model for a stored document."""
    document_id: str
    doctor_id: str
    created_at: str

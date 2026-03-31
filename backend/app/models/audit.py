"""
audit.py — Pydantic model for audit trail entries.
"""

from pydantic import BaseModel
from typing import Optional


class AuditEntry(BaseModel):
    """Schema for a single audit log record."""
    doctor_id: str
    action: str           # LOGIN | SIGN | VERIFY | SHRED | STEG_HIDE | STEG_EXTRACT
    document_id: Optional[str] = None
    timestamp: str
    ip_address: str

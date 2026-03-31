"""
audit_service.py — Handles all audit trail operations.

Every significant system action (login, sign, verify, shred, steg) is logged
here with a timestamp, IP address, and optional document reference.
"""

from datetime import datetime, timezone
from app.db import audit_col


def log_action(
    doctor_id: str,
    action: str,
    ip_address: str,
    document_id: str | None = None,
) -> None:
    """
    Insert a new audit log entry into the audit collection.

    Args:
        doctor_id:   The doctor performing the action.
        action:      One of: LOGIN, SIGN, VERIFY, SHRED, STEG_HIDE, STEG_EXTRACT
        ip_address:  The client IP address (from request).
        document_id: Optional reference to a document involved in the action.
    """
    entry = {
        "doctor_id":   doctor_id,
        "action":      action,
        "document_id": document_id,
        "timestamp":   datetime.now(timezone.utc).isoformat(),
        "ip_address":  ip_address,
    }
    audit_col.insert_one(entry)


def get_all_logs() -> list[dict]:
    """
    Return all audit logs sorted by timestamp (newest first).
    """
    logs = list(audit_col.find({}, {"_id": 0}).sort("timestamp", -1))
    return logs


def get_logs_by_doctor(doctor_id: str) -> list[dict]:
    """
    Return audit logs filtered for a specific doctor, newest first.
    """
    logs = list(
        audit_col.find({"doctor_id": doctor_id}, {"_id": 0}).sort("timestamp", -1)
    )
    return logs

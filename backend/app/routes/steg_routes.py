"""
steg_routes.py — Steganography endpoints.

POST /steg/hide     →  Embed text in an image (multipart upload)
POST /steg/extract  →  Extract hidden text from an image (multipart upload)
"""

import os
import uuid

from fastapi import APIRouter, File, Form, UploadFile, Request
from fastapi.responses import FileResponse

from app.services import steg_service, audit_service

router = APIRouter()

UPLOAD_DIR = "uploads"


@router.post("/hide")
def hide_text(
    request: Request,
    file: UploadFile = File(...),
    text: str = Form(...),
    doctor_id: str = Form(...),
):
    """
    Embed secret text inside an uploaded image using LSB steganography.

    Accepts a multipart form with:
      - file:      The carrier image (PNG or BMP recommended).
      - text:      The secret text to embed.
      - doctor_id: Performing doctor (for audit).

    Returns the URL path to download the result image.
    """
    ip = request.client.host

    # Save the uploaded cover image
    ext         = os.path.splitext(file.filename)[1] or ".png"
    cover_path  = os.path.join(UPLOAD_DIR, f"cover_{uuid.uuid4()}{ext}")
    output_path = os.path.join(UPLOAD_DIR, f"steg_{uuid.uuid4()}.png")

    with open(cover_path, "wb") as f:
        f.write(file.file.read())

    steg_service.hide_text(cover_path, text, output_path)

    # Audit
    audit_service.log_action(doctor_id, "STEG_HIDE", ip)

    # Return the relative download URL
    filename = os.path.basename(output_path)
    return {
        "message":      "Text hidden successfully",
        "download_url": f"/uploads/{filename}",
    }


@router.post("/extract")
def extract_text(
    request: Request,
    file: UploadFile = File(...),
    doctor_id: str = Form(...),
):
    """
    Extract hidden text from a LSB-encoded image.

    Accepts a multipart form with:
      - file:      The steg image to analyse.
      - doctor_id: Performing doctor (for audit).

    Returns the extracted hidden text.
    """
    ip = request.client.host

    # Save uploaded image
    ext        = os.path.splitext(file.filename)[1] or ".png"
    save_path  = os.path.join(UPLOAD_DIR, f"extract_{uuid.uuid4()}{ext}")

    with open(save_path, "wb") as f:
        f.write(file.file.read())

    hidden_text = steg_service.extract_text(save_path)

    # Audit
    audit_service.log_action(doctor_id, "STEG_EXTRACT", ip)

    return {"hidden_text": hidden_text}

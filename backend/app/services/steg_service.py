"""
steg_service.py — LSB Steganography operations.

Uses the `stegano` library's LSB (Least Significant Bit) method to:
  - Hide plain-text inside a PNG/BMP image.
  - Extract hidden text from a steg image.
"""

from stegano import lsb
from fastapi import HTTPException, status


def hide_text(image_path: str, text: str, output_path: str) -> str:
    """
    Embed secret text inside an image using LSB steganography.

    Args:
        image_path:  Absolute path to the carrier (cover) image.
        text:        Secret text to embed.
        output_path: Where to save the result image (should be PNG).

    Returns:
        The output_path string on success.

    Raises:
        HTTPException 400 if hiding fails (e.g. image too small for text).
    """
    try:
        secret_image = lsb.hide(image_path, text)
        secret_image.save(output_path)
        return output_path
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Steganography hide failed: {str(exc)}",
        )


def extract_text(image_path: str) -> str:
    """
    Extract hidden text from a LSB-encoded image.

    Args:
        image_path: Path to the image that contains hidden data.

    Returns:
        The extracted secret text string.

    Raises:
        HTTPException 400 if no hidden data is found or extraction fails.
    """
    try:
        hidden = lsb.reveal(image_path)
        if hidden is None:
            raise ValueError("No hidden text found in image.")
        return hidden
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Steganography extract failed: {str(exc)}",
        )

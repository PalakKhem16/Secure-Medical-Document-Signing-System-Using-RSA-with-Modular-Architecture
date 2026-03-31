"""
helpers.py — General-purpose utility functions for the MediSign system.
"""

import random
import string


def generate_doctor_id() -> str:
    """
    Generate a short, human-friendly doctor ID.

    Format: DOC-XXXX  (XXXX = 4 random decimal digits)
    Example: DOC-4821
    """
    digits = "".join(random.choices(string.digits, k=4))
    return f"DOC-{digits}"


def normalize(value: str) -> str:
    """Strip leading/trailing whitespace from a string."""
    return value.strip()

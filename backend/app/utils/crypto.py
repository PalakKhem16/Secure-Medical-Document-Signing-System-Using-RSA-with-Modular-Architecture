"""
crypto.py — Cryptographic primitives for the MediSign system.

Provides:
  - RSA key-pair generation (2048-bit)
  - RSA document signing (SHA-256)
  - RSA signature verification
  - AES-GCM symmetric encryption / decryption (for crypto-shredding)
"""

import os
import base64

from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives.ciphers.aead import AESGCM


#  RSA 

def generate_rsa_keypair() -> tuple[str, str]:
    """
    Generate a 2048-bit RSA key pair.

    Returns:
        (private_key_pem, public_key_pem) — both as UTF-8 strings.
    """
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
    )

    private_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.TraditionalOpenSSL,
        encryption_algorithm=serialization.NoEncryption(),
    ).decode("utf-8")

    public_pem = private_key.public_key().public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo,
    ).decode("utf-8")

    return private_pem, public_pem


def sign_document(private_key_pem: str, content: bytes | str) -> str:
    """
    Sign document content with an RSA private key using PKCS#1v15 + SHA-256.

    Args:
        private_key_pem: PEM-encoded RSA private key string.
        content:         Plain-text document content.

    Returns:
        Hex-encoded signature string.
    """
    private_key = serialization.load_pem_private_key(
        private_key_pem.encode("utf-8"),
        password=None,
    )

    content_bytes = content if isinstance(content, bytes) else content.encode("utf-8")
    
    signature_bytes = private_key.sign(
        content_bytes,
        padding.PKCS1v15(),
        hashes.SHA256(),
    )

    return signature_bytes.hex()


def verify_document(public_key_pem: str, content: bytes | str, signature_hex: str) -> bool:
    """
    Verify an RSA signature against document content.

    Args:
        public_key_pem: PEM-encoded RSA public key string.
        content:        Plain-text document content (must be identical to what was signed).
        signature_hex:  Hex-encoded signature returned by sign_document().

    Returns:
        True if the signature is valid, False if tampered / invalid.
    """
    try:
        public_key = serialization.load_pem_public_key(
            public_key_pem.encode("utf-8")
        )

        signature_bytes = bytes.fromhex(signature_hex)

        content_bytes = content if isinstance(content, bytes) else content.encode("utf-8")

        public_key.verify(
            signature_bytes,
            content_bytes,
            padding.PKCS1v15(),
            hashes.SHA256(),
        )
        return True
    except Exception:
        return False


#  AES-GCM (symmetric, for crypto-shredding) 

def generate_symmetric_key() -> bytes:
    """Generate a random 256-bit AES key."""
    return AESGCM.generate_key(bit_length=256)


def encrypt_content(key: bytes, content: bytes | str) -> str:
    """
    Encrypt plain-text content with AES-256-GCM.

    The 12-byte nonce is prepended to the ciphertext and the whole thing
    is returned as a Base64 string for safe MongoDB storage.

    Args:
        key:     32-byte AES key.
        content: Plain-text string.

    Returns:
        Base64-encoded string: nonce (12 bytes) + ciphertext.
    """
    aesgcm = AESGCM(key)
    nonce  = os.urandom(12)
    content_bytes = content if isinstance(content, bytes) else content.encode("utf-8")
    ct     = aesgcm.encrypt(nonce, content_bytes, None)
    return base64.b64encode(nonce + ct).decode("utf-8")


def decrypt_content(key: bytes, encrypted_b64: str) -> str:
    """
    Decrypt AES-256-GCM ciphertext.

    Args:
        key:           32-byte AES key.
        encrypted_b64: Base64 string produced by encrypt_content().

    Returns:
        Decrypted plain-text string.

    Raises:
        Exception if decryption fails (key deleted / tampered).
    """
    raw   = base64.b64decode(encrypted_b64)
    nonce = raw[:12]
    ct    = raw[12:]
    aesgcm = AESGCM(key)
    return aesgcm.decrypt(nonce, ct, None).decode("utf-8")

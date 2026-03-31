# Secure Medical Document Signing System Using RSA with Modular Architecture

## 1. What is the Problem?
Medical documents (such as prescriptions, test results, and patient histories) are highly sensitive and prone to forgery, tampering, and unauthorized access. Traditional paper-based or basic digital records lack robust cryptographic guarantees. 

Furthermore, in the event of a data breach, or when a patient exercises their "right to be forgotten" (under HIPAA/GDPR regulations), completely erasing data is difficult if physical or digital backups exist. Sharing sensitive medical information over unsecured channels also risks interception and unauthorized viewing.

## 2. Our Solution
MediSign is a comprehensive, modular cryptographic framework and web application designed to secure medical documents. It provides end-to-end security using digital signatures, advanced encryption, and steganography. 

**Key Benefits:**
- **Authentication & Non-repudiation:** Ensures that a medical document was definitively signed by a specific, verified doctor using robust RSA-2048 cryptography.
- **Integrity (Tamper Detection):** Guarantees that any unauthorized modification to a document is instantly detected.
- **Crypto-Shredding:** Securely and permanently deletes data by destroying its encryption key. This renders the ciphertext completely unrecoverable, perfectly satisfying privacy compliance.
- **Steganography:** Hides sensitive authentication tokens or patient data within medical images (like X-rays or MRI scans) to prevent unauthorized viewing during transmission.

## 3. Tech Stack
**Backend (System Logic & Cryptography):**
- **Framework:** FastAPI (Python)
- **Server:** Uvicorn (ASGI)
- **Database:** MongoDB (via PyMongo)
- **Authentication:** `bcrypt` for password hashing
- **Cryptography:** `cryptography` library (RSA key generation, RSA-PSS SHA-256 signing/verifying, AES-256-GCM symmetric encryption)
- **Steganography:** `stegano` and `Pillow` for image-based data hiding

**Frontend (Client Presentation):**
- **Structure:** Vanilla HTML5
- **Logic:** Vanilla JavaScript with Fetch API for backend integration

## 4. System Overview & Features
MediSign operates through several distinct, modular features to ensure complete document security:

### A. Doctor Authentication & Certificate Authority
When an admin issues a certificate to a new doctor, the system generates a unique identifier and a 2048-bit RSA key pair. The private key is securely stored for signing, while the public key is used for verification.

### B. Document Signing & Storage
When a doctor signs a document, the plaintext content is signed using the doctor's RSA private key. To support crypto-shredding, the content is then symmetrically encrypted using a randomly generated AES-256-GCM key. The encrypted ciphertext and the RSA signature are stored in the database, while the AES encryption key is kept securely in a separate collection.

### C. Signature Verification & Tamper Detection
Anyone can verify a document by providing the plaintext content, the signature, and the doctor's ID. The system fetches the doctor's public key and verifies the RSA signature. If even a single character in the document has been altered, the verification correctly fails ("TAMPERED").

### D. Crypto-Shredding
Instead of standard deletion, MediSign implements crypto-shredding. By securely destroying the unique AES encryption key associated with a document, the encrypted ciphertext becomes mathematically impossible to decrypt. The encrypted document record remains as proof of existence, but the data is gone forever.

### E. Steganography (LSB)
Allows hiding text inside the Least Significant Bits (LSB) of a cover image (like a PNG). The modified stego-image looks visually identical to the naked eye but carries hidden data that can be securely extracted by authorized personnel.

### F. Immutable Audit Trail
Every significant system action (Login, Document Sign, Verify, Crypto-Shred, Steganography Hide/Extract) is securely logged with the doctor's ID, a UTC timestamp, and the client's IP address to ensure full accountability.

## 5. Results & Metrics (from Research Notebook)
Extensive benchmarking and validation were conducted in our Python Colab environment (`Secure_Medical_Document_Authentication.ipynb`).

### Cryptographic Performance
- **Key Generation:** Generating an RSA-2048 key pair is a one-time setup cost taking roughly **~58 ms**.
- **Signing Time:** Extremely fast, taking **~0.9 ms** regardless of document size (tested from 10 to 5000 characters). This is because SHA-256 hashing is $O(n)$ but incredibly fast, while the dominant cost—modular exponentiation—is fixed.
- **Verification Time:** Taking **~0.05 to 0.07 ms**. Verification uses the public exponent, making it significantly faster (up to ~15x quicker) than signing.

### Tamper Detection Accuracy
The system achieved **100.0% accuracy** in detecting tampered documents. Scenarios successfully tested include:
- Original baseline (Classified as: `VALID`)
- 1-character change (Classified as: `TAMPERED`)
- Word substitution e.g., changing "Insulin" to "Aspirin" (Classified as: `TAMPERED`)
- Full document replacement (Classified as: `TAMPERED`)

### Crypto-Shredding Effectiveness
- **Recovery Success Rate: 0.00%**. Once the 32-byte AES key is zero-overwritten and deleted, attempting to decrypt the ciphertext guarantees an `InvalidToken` failure. Brute-forcing AES-256 without the key is computationally infeasible.

### Steganography Fidelity
Hiding a secret authentication token inside a carrier image successfully protects the payload. While the file size increases slightly depending on the format, the data is accurately extracted with 100% fidelity without visibly altering the clinical image.

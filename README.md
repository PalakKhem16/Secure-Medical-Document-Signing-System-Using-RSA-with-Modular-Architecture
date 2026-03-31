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

### System Architecture
<img width="617" height="460" alt="image" src="https://github.com/user-attachments/assets/a1b44061-5515-4efd-8b9a-5dd356cd449a" />


### System Workflow
<img width="570" height="701" alt="image" src="https://github.com/user-attachments/assets/74406ee5-025b-479b-b4ba-7e84548e19d0" />



### A. Doctor Authentication & Certificate Authority
When an admin issues a certificate to a new doctor, the system generates a unique identifier and a 2048-bit RSA key pair. The private key is securely stored for signing, while the public key is used for verification.

### B. Document Signing & Storage
When a doctor signs a document, the plaintext content is signed using the doctor's RSA private key. To support crypto-shredding, the content is then symmetrically encrypted using a randomly generated AES-256-GCM key. The encrypted ciphertext and the RSA signature are stored in the database, while the AES encryption key is kept securely in a separate collection.

### C. Signature Verification & Tamper Detection
Anyone can verify a document by providing the plaintext content, the signature, and the doctor's ID. The system fetches the doctor's public key and verifies the RSA signature. If even a single character in the document has been altered, the verification correctly fails ("TAMPERED").
<img width="601" height="535" alt="image" src="https://github.com/user-attachments/assets/ed2cabce-f0af-4cd3-9e2f-a64e2549a025" />


### D. Crypto-Shredding
Instead of standard deletion, MediSign implements crypto-shredding. By securely destroying the unique AES encryption key associated with a document, the encrypted ciphertext becomes mathematically impossible to decrypt. The encrypted document record remains as proof of existence, but the data is gone forever.
<img width="853" height="302" alt="image" src="https://github.com/user-attachments/assets/c0f114b6-a1b7-453b-b1e9-c7d27b2aff6d" />


### E. Steganography (LSB)
Allows hiding text inside the Least Significant Bits (LSB) of a cover image (like a PNG). The modified stego-image looks visually identical to the naked eye but carries hidden data that can be securely extracted by authorized personnel.
<img width="756" height="261" alt="image" src="https://github.com/user-attachments/assets/7e8f6b44-7892-4079-a220-110731a89264" />


### F. Immutable Audit Trail
Every significant system action (Login, Document Sign, Verify, Crypto-Shred, Steganography Hide/Extract) is securely logged with the doctor's ID, a UTC timestamp, and the client's IP address to ensure full accountability.
<img width="951" height="760" alt="image" src="https://github.com/user-attachments/assets/cf94a76e-95a9-4271-9a9c-9fcbebbc6381" />


## 5. Results & Metrics (from Research Notebook)
Extensive benchmarking and validation were conducted in our Python Colab environment (`Secure_Medical_Document_Authentication.ipynb`).

### Cryptographic Performance
- **Key Generation:** Generating an RSA-2048 key pair is a one-time setup cost taking roughly **~58 ms**.
- **Signing Time:** Extremely fast, taking **~0.9 ms** regardless of document size (tested from 10 to 5000 characters). This is because SHA-256 hashing is $O(n)$ but incredibly fast, while the dominant cost—modular exponentiation—is fixed.
- **Verification Time:** Taking **~0.05 to 0.07 ms**. Verification uses the public exponent, making it significantly faster (up to ~15x quicker) than signing.
<img width="1678" height="590" alt="image" src="https://github.com/user-attachments/assets/aecb051d-d9ee-4a7e-9830-aa2cc749a02f" />

### Tamper Detection Accuracy
The system achieved **100.0% accuracy** in detecting tampered documents. Scenarios successfully tested include:
- Original baseline (Classified as: `VALID`)
- 1-character change (Classified as: `TAMPERED`)
- Word substitution e.g., changing "Insulin" to "Aspirin" (Classified as: `TAMPERED`)
- Full document replacement (Classified as: `TAMPERED`)
- <img width="837" height="182" alt="image" src="https://github.com/user-attachments/assets/927f69ac-2238-401b-98f6-900dd48a3f6b" />


### Crypto-Shredding Effectiveness
- **Recovery Success Rate: 0.00%**. Once the 32-byte AES key is zero-overwritten and deleted, attempting to decrypt the ciphertext guarantees an `InvalidToken` failure. Brute-forcing AES-256 without the key is computationally infeasible.
- <img width="813" height="295" alt="image" src="https://github.com/user-attachments/assets/073fb788-2908-46e0-b141-7fab052c653b" />


### Steganography Fidelity
Hiding a secret authentication token inside a carrier image successfully protects the payload. While the file size increases slightly depending on the format, the data is accurately extracted with 100% fidelity without visibly altering the clinical image.
<img width="863" height="490" alt="image" src="https://github.com/user-attachments/assets/f19ff0e4-8752-4454-aa55-6b4371def8b1" />

### Performance Overhead Comparison
<img width="860" height="608" alt="image" src="https://github.com/user-attachments/assets/3316e564-b1a7-4036-b466-a40d84eb9ea9" />

## Legal Compliance with IT ACT 2000

<img width="861" height="463" alt="image" src="https://github.com/user-attachments/assets/d85712a1-1472-4b61-8793-3e57b08fbb2b" />
 
The Digital Personal Data Protection Act, 2023 further supports the design of this system
through principles such as lawful processing, consent-based handling, purpose limitation, and
erasure of unnecessary data. In a medical document system, these ideas are important because
records should be accessed only by authorized roles and used only for the intended healthcare
purpose. The system therefore includes role-based access, logging, and secure deletion support.
This approach is also conceptually aligned with international data protection practices such as
the “right to ensure” (right to be forgotten) under the General Data Protection Regulation
(GDPR). These principles collectively strengthen the system’s alignment with both national and
internationally recognized data protection practices.
The right to privacy under Article 21 provides an important constitutional context for this
project, since medical documents contain highly sensitive personal information.
Accordingly, the system is designed to support confidentiality, restricted access, and secure
handling of records. This discussion is intended for academic understanding and should not be
considered legal advice.



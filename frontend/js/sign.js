/**
 * sign.js — Document signing and crypto-shredding logic.
 */

let _currentSig   = "";
let _currentDocId = "";

window.addEventListener("DOMContentLoaded", () => {
  const s = requireAuth(false);
  if (!s) return;

  // Pre-fill doc id if passed via hash (from logs page)
  const hash = location.hash.replace("#", "");
  if (hash) document.getElementById("shredDocId").value = hash;
});

function logout() { clearSession(); window.location.href = "index.html"; }

/*  Sign  */
document.getElementById("signForm").addEventListener("submit", async (e) => {
  e.preventDefault();
  hideAlert("#signAlert");
  document.getElementById("signResult").style.display = "none";

  const s = getSession();
  if (s.isAdmin) {
    showAlert("#signAlert", "Admins cannot sign documents. Please log in as a real Doctor to use your RSA key.", "error");
    return;
  }

  const fileInput = document.getElementById("signFile");
  if (!fileInput.files.length) {
    showAlert("#signAlert", "Please select a file to sign.", "error");
    return;
  }

  const file = fileInput.files[0];
  const btn  = document.getElementById("signBtn");

  btn.disabled = true;
  btn.innerHTML = '<span class="spinner"></span> Signing…';

  try {
    const formData = new FormData();
    formData.append("doctor_id", s.doctor_id);
    formData.append("file", file);

    const data = await apiUpload("/sign/", formData);
    _currentSig   = data.signature;
    _currentDocId = data.document_id;

    document.getElementById("signatureOutput").textContent = data.signature;
    document.getElementById("docIdOutput").textContent     = data.document_id;
    document.getElementById("signResult").style.display    = "block";
    document.getElementById("shredDocId").value            = data.document_id;

    showAlert("#signAlert", "Document signed and stored successfully.", "success");
  } catch (err) {
    showAlert("#signAlert", err.message, "error");
  } finally {
    btn.disabled = false;
    btn.textContent = "Sign Document";
  }
});

/*  Shred  */
document.getElementById("shredForm").addEventListener("submit", async (e) => {
  e.preventDefault();
  hideAlert("#shredAlert");

  const s           = getSession();
  const document_id = document.getElementById("shredDocId").value.trim();
  const btn         = document.getElementById("shredBtn");

  if (!confirm(` This will permanently destroy the encryption key for document:\n${document_id}\n\nThis action CANNOT be undone. Continue?`)) return;

  btn.disabled = true;
  btn.innerHTML = '<span class="spinner"></span> Shredding…';

  try {
    const data = await apiFetch("/shred/", "POST", { document_id, doctor_id: s.doctor_id });
    showAlert("#shredAlert", ` ${data.status} — Document ID: ${data.document_id}`, "info");
  } catch (err) {
    showAlert("#shredAlert", err.message, "error");
  } finally {
    btn.disabled = false;
    btn.innerHTML = " Shred Document";
  }
});

function copySig() {
  if (!_currentSig) return;
  navigator.clipboard.writeText(_currentSig);
}

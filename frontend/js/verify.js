/**
 * verify.js — Document verification logic.
 */

window.addEventListener("DOMContentLoaded", () => requireAuth(false));
function logout() { clearSession(); window.location.href = "index.html"; }

document.getElementById("verifyForm").addEventListener("submit", async (e) => {
  e.preventDefault();
  hideAlert("#verifyAlert");
  document.getElementById("verifyResult").style.display = "none";

  const doctor_id = document.getElementById("vDoctorId").value.trim().toUpperCase();
  const signature = document.getElementById("vSignature").value.trim();
  const fileInput = document.getElementById("vFile");
  const btn       = document.getElementById("verifyBtn");

  if (!fileInput.files.length) {
    showAlert("#verifyAlert", "Please select a file to verify.", "error");
    return;
  }

  const file = fileInput.files[0];

  btn.disabled = true;
  btn.innerHTML = '<span class="spinner"></span> Verifying…';

  try {
    const formData = new FormData();
    formData.append("doctor_id", doctor_id);
    formData.append("signature", signature);
    formData.append("file", file);

    const data = await apiUpload("/verify/", formData);

    const isValid = data.status === "VALID";
    document.getElementById("verifyBadge").textContent  = isValid ? "" : "";
    document.getElementById("verifyStatus").innerHTML   =
      `<span class="badge ${isValid ? 'badge-valid' : 'badge-tampered'}">${data.status}</span>`;
    document.getElementById("verifyDesc").textContent   = isValid
      ? "The signature is authentic. This document has not been modified."
      : "The signature does not match. The document may have been tampered with.";
    document.getElementById("verifyResult").style.display = "block";

  } catch (err) {
    showAlert("#verifyAlert", err.message, "error");
  } finally {
    btn.disabled = false;
    btn.textContent = "Verify Signature";
  }
});

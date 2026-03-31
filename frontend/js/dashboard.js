/**
 * dashboard.js — Doctor dashboard logic.
 */

let _profile = null;

window.addEventListener("DOMContentLoaded", async () => {
  const s = requireAuth(false);
  if (!s) return;

  document.getElementById("navName").textContent = s.name;
  document.getElementById("navId").textContent   = s.doctor_id;
});

function logout() {
  clearSession();
  window.location.href = "index.html";
}

let settingsOpen = false;

async function toggleSettings(e) {
  e.preventDefault();
  const panel = document.getElementById("settingsPanel");
  settingsOpen = !settingsOpen;
  panel.style.display = settingsOpen ? "block" : "none";
  if (settingsOpen && !_profile) await loadProfile();
}

async function loadProfile() {
  const s       = getSession();
  const content = document.getElementById("profileContent");

  try {
    const data = await apiFetch(`/doctor/${s.doctor_id}/profile`);
    _profile = data;

    content.innerHTML = `
      <div style="display:grid; gap:14px; text-align:left;">
        <div class="form-group" style="margin:0;">
          <label>Doctor ID</label>
          <div class="mono">${data.doctor_id}</div>
        </div>
        <div class="form-group" style="margin:0;">
          <label>Name</label>
          <div class="mono">${data.name}</div>
        </div>
        <div class="form-group" style="margin:0;">
          <label>Email</label>
          <div class="mono">${data.email}</div>
        </div>
        <div class="form-group" style="margin:0;">
          <label>Public Key</label>
          <div class="mono">${data.public_key}</div>
        </div>
        <div class="form-group" style="margin:0;">
          <label>Private Key <span style="color:var(--danger); font-size:0.78rem;">(keep confidential)</span></label>
          <div class="mono">${maskKey(data.private_key)}</div>
        </div>
        <div class="form-group" style="margin:0;">
          <label>Registered</label>
          <div class="mono">${new Date(data.created_at).toLocaleString()}</div>
        </div>
      </div>
    `;
  } catch (err) {
    content.innerHTML = `<span style="color:var(--danger);">${err.message}</span>`;
  }
}

function maskKey(pem) {
  // Show first and last header lines, mask the body
  const lines = pem.split("\n").filter(Boolean);
  const body  = lines.slice(1, -1).join("").substring(0, 30) + "…[MASKED]";
  return `${lines[0]}\n${body}\n${lines[lines.length - 1]}`;
}

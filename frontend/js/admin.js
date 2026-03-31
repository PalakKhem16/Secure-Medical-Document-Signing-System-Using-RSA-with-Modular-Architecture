/**
 * admin.js — Admin dashboard logic.
 */

// Auth guard
window.addEventListener("DOMContentLoaded", () => {
  const s = requireAuth(true);
  if (!s) return;
  loadDoctors();
});

function logout() {
  clearSession();
  window.location.href = "index.html";
}

/*  Issue Certificate  */
document.getElementById("issueForm").addEventListener("submit", async (e) => {
  e.preventDefault();
  hideAlert("#issueAlert");

  const name     = document.getElementById("iName").value.trim();
  const email    = document.getElementById("iEmail").value.trim();
  const password = document.getElementById("iPassword").value.trim();
  const btn      = document.getElementById("issueBtn");

  btn.disabled = true;
  btn.innerHTML = '<span class="spinner"></span> Issuing…';

  try {
    const data = await apiFetch("/admin/issue", "POST", { name, email, password });
    showAlert("#issueAlert", ` Certificate issued! Doctor ID: ${data.doctor_id}`, "success");
    document.getElementById("issueForm").reset();
    loadDoctors();
  } catch (err) {
    showAlert("#issueAlert", err.message, "error");
  } finally {
    btn.disabled = false;
    btn.textContent = "Issue Certificate";
  }
});

/*  Doctors Table  */
async function loadDoctors() {
  const tbody = document.getElementById("doctorsBody");
  tbody.innerHTML = `<tr><td colspan="4" style="color:var(--text-muted); text-align:center;"><span class="spinner"></span></td></tr>`;

  try {
    const data = await apiFetch("/admin/doctors");
    if (!data.doctors.length) {
      tbody.innerHTML = `<tr><td colspan="4" style="color:var(--text-muted); text-align:center;">No doctors yet.</td></tr>`;
      return;
    }
    tbody.innerHTML = data.doctors.map(d => `
      <tr>
        <td><span class="badge badge-login">${d.doctor_id}</span></td>
        <td>${d.name}</td>
        <td>${d.email}</td>
        <td>${new Date(d.created_at).toLocaleString()}</td>
      </tr>
    `).join("");
  } catch (err) {
    tbody.innerHTML = `<tr><td colspan="4" style="color:var(--danger);">${err.message}</td></tr>`;
  }
}

/*  Audit Logs  */
async function loadLogs() {
  const tbody   = document.getElementById("logsBody");
  const filter  = document.getElementById("filterDoc").value.trim();
  const path    = filter ? `/admin/logs/${encodeURIComponent(filter)}` : "/admin/logs";

  tbody.innerHTML = `<tr><td colspan="5" style="color:var(--text-muted); text-align:center;"><span class="spinner"></span></td></tr>`;

  try {
    const data = await apiFetch(path);
    if (!data.logs.length) {
      tbody.innerHTML = `<tr><td colspan="5" style="color:var(--text-muted); text-align:center;">No logs found.</td></tr>`;
      return;
    }
    tbody.innerHTML = data.logs.map(l => `
      <tr>
        <td>${l.doctor_id}</td>
        <td>${actionBadge(l.action)}</td>
        <td style="font-size:0.78rem; color:var(--text-muted);">${l.document_id || "—"}</td>
        <td>${new Date(l.timestamp).toLocaleString()}</td>
        <td>${l.ip_address}</td>
      </tr>
    `).join("");
  } catch (err) {
    tbody.innerHTML = `<tr><td colspan="5" style="color:var(--danger);">${err.message}</td></tr>`;
  }
}

function actionBadge(action) {
  const map = {
    LOGIN:        "badge-login",
    SIGN:         "badge-sign",
    VERIFY:       "badge-valid",
    SHRED:        "badge-shredded",
    STEG_HIDE:    "badge-steg",
    STEG_EXTRACT: "badge-steg",
  };
  return `<span class="badge ${map[action] || ''}">${action}</span>`;
}

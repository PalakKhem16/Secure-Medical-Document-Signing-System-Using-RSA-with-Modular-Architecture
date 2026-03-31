/**
 * logs.js — Doctor's signed documents and personal activity log.
 */

window.addEventListener("DOMContentLoaded", () => {
  const s = requireAuth(false);
  if (!s) return;
  loadDocs();
  loadLogs();
});

function logout() { clearSession(); window.location.href = "index.html"; }

/*  Signed Documents  */
async function loadDocs() {
  const tbody = document.getElementById("docsBody");
  const s     = getSession();
  tbody.innerHTML = `<tr><td colspan="3" style="text-align:center;"><span class="spinner"></span></td></tr>`;

  try {
    const data = await apiFetch(`/doctor/${s.doctor_id}/documents`);
    if (!data.documents.length) {
      tbody.innerHTML = `<tr><td colspan="3" style="color:var(--text-muted); text-align:center;">No documents signed yet.</td></tr>`;
      return;
    }
    tbody.innerHTML = data.documents.map(d => `
      <tr>
        <td style="font-family:monospace; font-size:0.82rem; color:var(--accent);">${d.document_id}</td>
        <td>${new Date(d.created_at).toLocaleString()}</td>
        <td>
          <a href="sign.html#${d.document_id}" class="btn btn-danger" style="padding:5px 14px; font-size:0.8rem;"> Shred</a>
        </td>
      </tr>
    `).join("");
  } catch (err) {
    tbody.innerHTML = `<tr><td colspan="3" style="color:var(--danger);">${err.message}</td></tr>`;
  }
}

/*  Activity Log  */
async function loadLogs() {
  const tbody = document.getElementById("logsBody");
  const s     = getSession();
  tbody.innerHTML = `<tr><td colspan="4" style="text-align:center;"><span class="spinner"></span></td></tr>`;

  try {
    const data = await apiFetch(`/admin/logs/${s.doctor_id}`);
    if (!data.logs.length) {
      tbody.innerHTML = `<tr><td colspan="4" style="color:var(--text-muted); text-align:center;">No activity yet.</td></tr>`;
      return;
    }
    tbody.innerHTML = data.logs.map(l => `
      <tr>
        <td>${actionBadge(l.action)}</td>
        <td style="font-size:0.78rem; color:var(--text-muted);">${l.document_id || "—"}</td>
        <td>${new Date(l.timestamp).toLocaleString()}</td>
        <td>${l.ip_address}</td>
      </tr>
    `).join("");
  } catch (err) {
    tbody.innerHTML = `<tr><td colspan="4" style="color:var(--danger);">${err.message}</td></tr>`;
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

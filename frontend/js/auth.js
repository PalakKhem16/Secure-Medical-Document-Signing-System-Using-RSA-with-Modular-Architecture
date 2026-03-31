/**
 * auth.js — Login page logic.
 *
 * Handles:
 *   - "ADMIN" shortcut login (no server call needed)
 *   - Regular doctor login via POST /auth/login
 */

const ADMIN_ID       = "ADMIN";
const ADMIN_PASSWORD = "admin123";   // Change in production

document.getElementById("loginForm").addEventListener("submit", async (e) => {
  e.preventDefault();
  hideAlert("#loginAlert");

  const doctor_id = document.getElementById("doctorId").value.trim().toUpperCase();
  const password  = document.getElementById("password").value.trim();
  const btn       = document.getElementById("loginBtn");

  btn.disabled = true;
  btn.innerHTML = '<span class="spinner"></span> Signing in…';

  try {
    if (doctor_id === ADMIN_ID) {
      // Admin hardcoded check (prototype only)
      if (password !== ADMIN_PASSWORD) throw new Error("Invalid admin password.");
      saveSession(ADMIN_ID, "System Administrator", true);
      window.location.href = "admin.html";
      return;
    }

    // Doctor login
    const data = await apiFetch("/auth/login", "POST", { doctor_id, password });
    saveSession(data.doctor_id, data.name, false);
    window.location.href = "dashboard.html";

  } catch (err) {
    showAlert("#loginAlert", err.message, "error");
    btn.disabled = false;
    btn.textContent = "Sign In";
  }
});

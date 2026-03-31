/**
 * api.js — Shared API utilities for MediSign frontend.
 *
 * Provides:
 *   - BASE_URL constant
 *   - apiFetch() — thin wrapper around fetch() with JSON handling
 *   - Session storage helpers for doctor_id / name
 */

const BASE_URL = "http://127.0.0.1:8000";

/**
 * Perform a JSON API request.
 *
 * @param {string} path    - Route path (e.g. "/auth/login")
 * @param {string} method  - HTTP method (default "GET")
 * @param {object|null} body - Request body (will be JSON-serialized)
 * @returns {Promise<object>} Parsed JSON response
 * @throws {Error} with detail message on HTTP errors
 */
async function apiFetch(path, method = "GET", body = null) {
  const opts = {
    method,
    headers: { "Content-Type": "application/json" },
  };
  if (body) opts.body = JSON.stringify(body);

  const res = await fetch(`${BASE_URL}${path}`, opts);
  const data = await res.json().catch(() => ({}));

  if (!res.ok) {
    throw new Error(data.detail || `HTTP ${res.status}`);
  }
  return data;
}

/**
 * Perform a multipart/form-data API request (for file uploads).
 *
 * @param {string}   path   - Route path
 * @param {FormData} formData - FormData object with files and fields
 * @returns {Promise<object>} Parsed JSON response
 */
async function apiUpload(path, formData) {
  const res = await fetch(`${BASE_URL}${path}`, { method: "POST", body: formData });
  const data = await res.json().catch(() => ({}));
  if (!res.ok) {
    throw new Error(data.detail || `HTTP ${res.status}`);
  }
  return data;
}

/*  Session helpers  */

function saveSession(doctor_id, name, isAdmin = false) {
  sessionStorage.setItem("doctor_id", doctor_id);
  sessionStorage.setItem("name", name);
  sessionStorage.setItem("isAdmin", isAdmin ? "true" : "false");
}

function getSession() {
  return {
    doctor_id: sessionStorage.getItem("doctor_id"),
    name:      sessionStorage.getItem("name"),
    isAdmin:   sessionStorage.getItem("isAdmin") === "true",
  };
}

function clearSession() {
  sessionStorage.clear();
}

function requireAuth(adminRequired = false) {
  const s = getSession();
  if (!s.doctor_id) {
    window.location.href = "index.html";
    return null;
  }
  if (adminRequired && !s.isAdmin) {
    window.location.href = "dashboard.html";
    return null;
  }
  return s;
}

/*  Alert helper  */
function showAlert(selector, message, type = "info") {
  const el = document.querySelector(selector);
  if (!el) return;
  el.textContent = message;
  el.className = `alert alert-${type} show`;
}

function hideAlert(selector) {
  const el = document.querySelector(selector);
  if (el) el.className = "alert";
}

/**
 * steg.js — Steganography hide/extract logic.
 */

window.addEventListener("DOMContentLoaded", () => requireAuth(false));
function logout() { clearSession(); window.location.href = "index.html"; }

/*  Tabs  */
function switchTab(tab) {
  document.getElementById("panelHide").classList.toggle("active",    tab === "hide");
  document.getElementById("panelExtract").classList.toggle("active", tab === "extract");
  document.getElementById("tabHide").classList.toggle("active",      tab === "hide");
  document.getElementById("tabExtract").classList.toggle("active",   tab === "extract");
}

/*  File input labels  */
document.getElementById("hideFile").addEventListener("change", (e) => {
  const name = e.target.files[0]?.name || "No file selected";
  document.getElementById("hideFileName").textContent = ` ${name}`;
});

document.getElementById("extractFile").addEventListener("change", (e) => {
  const name = e.target.files[0]?.name || "No file selected";
  document.getElementById("extractFileName").textContent = ` ${name}`;
});

/*  Hide  */
document.getElementById("hideForm").addEventListener("submit", async (e) => {
  e.preventDefault();
  hideAlert("#hideAlert");
  document.getElementById("hideResult").style.display = "none";

  const s    = getSession();
  const file = document.getElementById("hideFile").files[0];
  const text = document.getElementById("hideText").value.trim();
  const btn  = document.getElementById("hideBtn");

  if (!file) { showAlert("#hideAlert", "Please select a carrier image.", "error"); return; }
  if (!text) { showAlert("#hideAlert", "Please enter secret text.", "error"); return; }

  btn.disabled = true;
  btn.innerHTML = '<span class="spinner"></span> Hiding…';

  try {
    const form = new FormData();
    form.append("file",      file);
    form.append("text",      text);
    form.append("doctor_id", s.doctor_id);

    const data = await apiUpload("/steg/hide", form);

    const imageUrl = `http://127.0.0.1:8000${data.download_url}`;
    const imgResponse = await fetch(imageUrl);
    const imgBlob = await imgResponse.blob();
    const objectUrl = window.URL.createObjectURL(imgBlob);

    const dlLink = document.getElementById("hideDownload");
    dlLink.href = objectUrl;
    dlLink.download = `steg_hidden_${Date.now()}.png`;

    document.getElementById("hideResult").style.display = "block";
    showAlert("#hideAlert", "Text hidden successfully in the image.", "success");
  } catch (err) {
    showAlert("#hideAlert", err.message, "error");
  } finally {
    btn.disabled = false;
    btn.textContent = "Hide Text in Image";
  }
});

/*  Extract  */
document.getElementById("extractForm").addEventListener("submit", async (e) => {
  e.preventDefault();
  hideAlert("#extractAlert");
  document.getElementById("extractResult").style.display = "none";

  const s    = getSession();
  const file = document.getElementById("extractFile").files[0];
  const btn  = document.getElementById("extractBtn");

  if (!file) { showAlert("#extractAlert", "Please select a steg image.", "error"); return; }

  btn.disabled = true;
  btn.innerHTML = '<span class="spinner"></span> Extracting…';

  try {
    const form = new FormData();
    form.append("file",      file);
    form.append("doctor_id", s.doctor_id);

    const data = await apiUpload("/steg/extract", form);
    document.getElementById("extractOutput").textContent    = data.hidden_text;
    document.getElementById("extractResult").style.display  = "block";
    showAlert("#extractAlert", "Hidden text extracted successfully.", "success");
  } catch (err) {
    showAlert("#extractAlert", err.message, "error");
  } finally {
    btn.disabled = false;
    btn.textContent = "Extract Hidden Text";
  }
});

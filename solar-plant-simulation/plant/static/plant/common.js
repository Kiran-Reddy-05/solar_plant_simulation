// Shared API fetch logic, refresh button, and visible error messages.
async function fetchJson(url) {
  const response = await fetch(url, { cache: "no-store" });
  let payload;
  try {
    payload = await response.json();
  } catch {
    throw new Error(`Server returned invalid JSON (HTTP ${response.status})`);
  }
  if (!response.ok) {
    throw new Error(payload.error?.message || `HTTP ${response.status}`);
  }
  return payload;
}

function setupRefresh(loadData) {
  const button = document.getElementById("refresh");
  const errorBox = document.getElementById("error");
  const updated = document.getElementById("updated");
  let loading = false;

  async function refresh() {
    if (loading) return; // Avoid overlapping network requests.
    loading = true;
    button.disabled = true;
    try {
      await loadData();
      errorBox.textContent = "";
      updated.textContent = `Last refreshed: ${new Date().toLocaleTimeString()}`;
    } catch (error) {
      errorBox.textContent = `Unable to refresh: ${error.message}`;
    } finally {
      loading = false;
      button.disabled = false;
    }
  }

  button.addEventListener("click", refresh);
  refresh();
  setInterval(refresh, 3000); // Change auto refresh time here.
}

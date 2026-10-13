// Page 2: render inverter API data and allow the current readings to be downloaded as JSON.
let latestInverterPayload = null;

setupRefresh(async () => {
  const data = await fetchJson("/api/data/inverter/");
  latestInverterPayload = data;
  const tbody = document.getElementById("inverter-rows");
  tbody.replaceChildren(); // Clear old rows before displaying fresh readings.

  for (const inverter of data.inverters) {
    const row = document.createElement("tr");
    const minPower = Number(inverter.active_power_min_kw ?? 10);
    const maxPower = Number(inverter.active_power_max_kw ?? 100);
    const activePower = Number(inverter.active_power_kw);
    const isOutOfLimit = activePower < minPower || activePower > maxPower;
    const hasFault = inverter.status !== "RUNNING" || isOutOfLimit;

    // Highlight the entire inverter row when status or active power is abnormal.
    row.classList.add(hasFault ? "inverter-alert" : "inverter-normal");

    const values = [
      inverter.inverter_id, inverter.status, inverter.active_power_kw,
      inverter.voltage_v, inverter.current_a, inverter.frequency_hz,
      inverter.temperature_c,
    ];

    for (const value of values) {
      const cell = document.createElement("td");
      cell.textContent = String(value); // Use textContent rather than inserting HTML.
      row.appendChild(cell);
    }
    tbody.appendChild(row);
  }
});

// Download the latest successful API response as a formatted JSON file.
document.getElementById("download-json").addEventListener("click", () => {
  if (!latestInverterPayload) {
    document.getElementById("error").textContent =
      "Inverter data is not loaded yet. Please refresh and try again.";
    return;
  }

  const json = JSON.stringify(latestInverterPayload, null, 2);
  const blob = new Blob([json], { type: "application/json" });
  const downloadUrl = URL.createObjectURL(blob);
  const link = document.createElement("a");
  link.href = downloadUrl;
  link.download = `inverter-data-${new Date().toISOString().replace(/[:.]/g, "-")}.json`;
  document.body.appendChild(link);
  link.click();
  link.remove();
  URL.revokeObjectURL(downloadUrl);
});

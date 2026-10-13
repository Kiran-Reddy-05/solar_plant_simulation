// Page 1: call the plant overview API and render weather station values.
setupRefresh(async () => {
  const data = await fetchJson("/api/plant/overview/");
  const weather = data.weather_station;
  document.getElementById("capacity").textContent = `${data.capacity_kw} kW`;
  document.getElementById("power").textContent = `${data.total_active_power_kw} kW`;
  document.getElementById("utilization").textContent = `${data.capacity_utilization_percent}%`;
  document.getElementById("temperature").textContent = `${weather.temperature_c} °C`;
  document.getElementById("irradiance").textContent = `${weather.irradiance_w_m2} W/m²`;
  document.getElementById("wind").textContent = `${weather.wind_speed_m_s} m/s`;
  document.getElementById("humidity").textContent = `${weather.humidity_percent}%`;
});

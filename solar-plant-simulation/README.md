# Solar Plant Simulation — Django

Two-page Django application with JSON APIs and a simulated solar plant.
**No real hardware is connected.** Readings change on each API request.

## Requirements
- Python 3.10+ (Python 3.12 or 3.13 recommended)
- VS Code and an internet connection for first-time dependency installation

## Run on Windows (VS Code Terminal: Command Prompt)
1. Extract the ZIP and open the **solar-plant-django-ready** folder in VS Code.
2. Open **Terminal > New Terminal**.
3. Run the following commands **one line at a time**:

```bat
py -m venv .venv
.venv\Scripts\activate.bat
python -m pip install -r requirements.txt
python manage.py migrate
python manage.py test
python manage.py runserver
```

If VS Code terminal is PowerShell, either change the terminal to **Command Prompt**, or activate using `.venv\Scripts\Activate.ps1` (PowerShell execution policy may block it).

Open:
- Overview page: http://127.0.0.1:8000/
- Inverter page: http://127.0.0.1:8000/inverters/
- Plant API: http://127.0.0.1:8000/api/plant/overview/
- All inverters: http://127.0.0.1:8000/api/data/inverter/
- Single inverter: http://127.0.0.1:8000/api/data/inverter/?id=INV001

Stop server: `Ctrl+C`.

## API contract
All API endpoints are **GET only**. They return `application/json`.

### GET /api/plant/overview/
Example fields (numbers vary):
```json
{
  "timestamp": "2026-10-13T05:00:00+00:00",
  "plant_name": "Demo Solar Plant",
  "capacity_kw": 500.0,
  "total_active_power_kw": 278.4,
  "capacity_utilization_percent": 55.68,
  "weather_station": {
    "temperature_c": 31.4,
    "irradiance_w_m2": 600.0,
    "wind_speed_m_s": 3.2,
    "humidity_percent": 51.0
  },
  "simulation": true
}
```

### GET /api/data/inverter/
Returns `timestamp`, `count`, and `inverters` (array). Each inverter contains:
```json
{
  "inverter_id": "INV001",
  "status": "RUNNING",
  "active_power_kw": 56.4,
  "voltage_v": 412.0,
  "current_a": 80.6,
  "frequency_hz": 50.0,
  "temperature_c": 38.4
}
```

### GET /api/data/inverter/?id=INV001
Returns `timestamp` and `inverter` (single object).





## Design notes
- The simulation uses a virtual daylight cycle, not real local sunrise/sunset.
- Every request produces a new snapshot. Separate endpoint calls are **not synchronized**.
- Active power is an illustrative calculation, not a measured value.
- `capacity_utilization_percent` is instantaneous capacity utilization, not industry performance ratio.
- State is in memory and resets on restart. Use database snapshots for historical reports.
- Development settings are **not suitable for deployment**: set environment-based SECRET_KEY, DEBUG=False, secure ALLOWED_HOSTS and configure hosting before going live.
- `__pycache__`, `.venv`, and `db.sqlite3` should not be committed; see `.gitignore`.


## Inverter alerts and JSON download

- Inverter active-power limits in the demo are 10 kW (minimum) and 100 kW (maximum).
- An inverter row is highlighted red when its status is not `RUNNING` or its active power is outside these limits. Normal rows are green.
- The Inverter Data page's **Download JSON** button downloads the most recent successful inverter API response.
- The simulator occasionally injects stopped, under-limit, and over-limit states so the alert display can be demonstrated. These are simulated values, not real equipment telemetry.
- Both dashboard pages refresh every 3 seconds. The shared interval is configured in `plant/static/plant/common.js`.


import math
import random
import threading
from datetime import datetime, timezone

CAPACITY_KW = 500.0
INVERTER_CAPACITY_KW = 100.0
MIN_ACTIVE_POWER_KW = 10.0
MAX_ACTIVE_POWER_KW = INVERTER_CAPACITY_KW
INVERTER_IDS = tuple(f"INV{i:03d}" for i in range(1, 9)) # number of inverters in the plant
_lock = threading.Lock()
_tick = 0


def make_snapshot():
    """Return internally consistent weather, plant and inverter readings."""
    global _tick
    with _lock:
        _tick += 1
        tick = _tick

    # A changing virtual daylight cycle avoids permanently zero nighttime output.
    sun_factor = max(0.08, math.sin((tick % 120) / 120 * math.pi))
    irradiance = round(min(1000, 1000 * sun_factor * random.uniform(0.88, 1.0)), 2)
    ambient = round(random.uniform(24, 37), 2)
    weather = {
        "temperature_c": ambient,
        "irradiance_w_m2": irradiance,
        "wind_speed_m_s": round(random.uniform(0.5, 9.0), 2),
        "humidity_percent": round(random.uniform(30, 75), 2),
    }

    inverters = []
    for inverter_id in INVERTER_IDS:
        # Simple power model with 95% inverter conversion efficiency.
        power = round(min(INVERTER_CAPACITY_KW,
                          INVERTER_CAPACITY_KW * irradiance / 1000 * 0.95
                          * random.uniform(0.96, 1.0)), 2)

        # Inject occasional faults so it can show alert states with some error codes
        fault_roll = random.random()
        if fault_roll < 0.04:
            power = 0.0
            inverter_status = "Err_404" # inverter stopped
        elif fault_roll < 0.08:
            power = round(random.uniform(0.0, MIN_ACTIVE_POWER_KW - 0.01), 2)
            inverter_status = "Err_401" # inverter is running but below minimum power
        elif fault_roll < 0.12:
            power = round(random.uniform(MAX_ACTIVE_POWER_KW + 0.1, 110.0), 2)
            inverter_status = "Err_402" # inverter is running but above maximum power
        elif power < MIN_ACTIVE_POWER_KW:
            inverter_status = "Err_403" # inverter is running but below minimum power
        else:
            inverter_status = "RUNNING"

        voltage = round(random.uniform(400, 420), 2)
        power_factor = 0.98
        # Three-phase AC: P(W) = sqrt(3) * V * I * power_factor.
        current = round(power * 1000 / (math.sqrt(3) * voltage * power_factor), 2)
        inverters.append({
            "inverter_id": inverter_id,
            "status": inverter_status,
            "active_power_kw": power,
            "active_power_min_kw": MIN_ACTIVE_POWER_KW,
            "active_power_max_kw": MAX_ACTIVE_POWER_KW,
            "voltage_v": voltage,
            "current_a": current,
            "frequency_hz": 50.0,
            "temperature_c": round(ambient + random.uniform(4, 12), 2),
        })

    total = round(sum(item["active_power_kw"] for item in inverters), 2)
    return {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "plant_name": "Demo Solar Plant",
        "capacity_kw": CAPACITY_KW,
        "total_active_power_kw": total,
        "capacity_utilization_percent": round(total / CAPACITY_KW * 100, 2),
        "weather_station": weather,
        "inverters": inverters,
        "simulation": True,
    }

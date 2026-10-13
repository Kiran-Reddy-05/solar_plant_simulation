"""HTML pages and JSON endpoints with consistent error responses."""
import logging
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_GET
from .simulator import INVERTER_IDS, make_snapshot

logger = logging.getLogger(__name__)


def overview_page(request):
    """Display plant and weather dashboard."""
    return render(request, "plant/overview.html")


def inverters_page(request):
    """Display the dedicated inverter dashboard."""
    return render(request, "plant/inverters.html")

def about_page(request):
    """Display information about the solar plant project."""
    return render(request, "plant/about.html")    




def error_response(message, status_code):
    """Return a predictable JSON error structure."""
    return JsonResponse({"error": {"code": status_code, "message": message}}, status=status_code)


@require_GET
def plant_overview_api(request):
    """GET /api/plant/overview/ : plant summary + weather station."""
    try:
        snapshot = make_snapshot()
        # Keep this endpoint focused on the overview, not per-inverter details.
        snapshot.pop("inverters")
        return JsonResponse(snapshot)
    except Exception:
        logger.exception("Failed to generate plant overview")
        return error_response("Unable to retrieve plant overview", 500)


@require_GET
def inverter_data_api(request):
    """GET /api/data/inverter/ or ?id=INV001 : inverter telemetry."""
    inverter_id = request.GET.get("id")
    if inverter_id is not None:
        if not inverter_id.strip():
            return error_response("Parameter 'id' must not be empty", 400)
        if inverter_id not in INVERTER_IDS:
            return error_response(f"Inverter '{inverter_id}' not found", 404)

    try:
        snapshot = make_snapshot()
        if inverter_id is not None:
            inverter = next(item for item in snapshot["inverters"]
                            if item["inverter_id"] == inverter_id)
            return JsonResponse({"timestamp": snapshot["timestamp"], "inverter": inverter})
        return JsonResponse({"timestamp": snapshot["timestamp"],
                             "count": len(snapshot["inverters"]),
                             "inverters": snapshot["inverters"]})
    except Exception:
        logger.exception("Failed to generate inverter readings")
        return error_response("Unable to retrieve inverter data", 500)

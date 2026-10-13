"""Run with: python manage.py test"""
from unittest.mock import patch
from django.test import TestCase
from django.urls import reverse


class SolarPlantTests(TestCase):
    def test_pages_load(self):
        for name in ("overview_page", "inverters_page"):
            self.assertEqual(self.client.get(reverse(name)).status_code, 200)

    def test_overview_has_weather_and_power(self):
        response = self.client.get(reverse("plant_overview_api"))
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("weather_station", data)
        self.assertIn("total_active_power_kw", data)
        self.assertIn("irradiance_w_m2", data["weather_station"])

    def test_all_inverters(self):
        response = self.client.get(reverse("inverter_data_api"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()["inverters"]), 5)

    def test_one_inverter(self):
        response = self.client.get(reverse("inverter_data_api"), {"id": "INV001"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["inverter"]["inverter_id"], "INV001")

    def test_missing_inverter_returns_404(self):
        response = self.client.get(reverse("inverter_data_api"), {"id": "INV999"})
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json()["error"]["code"], 404)

    def test_empty_id_returns_400(self):
        response = self.client.get(reverse("inverter_data_api") + "?id=")
        self.assertEqual(response.status_code, 400)

    def test_post_returns_405(self):
        response = self.client.post(reverse("plant_overview_api"))
        self.assertEqual(response.status_code, 405)

    @patch("plant.views.make_snapshot", side_effect=RuntimeError("test error"))
    def test_internal_error_returns_safe_json(self, _mock):
        response = self.client.get(reverse("plant_overview_api"))
        self.assertEqual(response.status_code, 500)
        self.assertNotIn("test error", response.content.decode())
    def test_inverter_data_includes_active_power_limits(self):
        response = self.client.get(reverse("inverter_data_api"))
        self.assertEqual(response.status_code, 200)
        for inverter in response.json()["inverters"]:
            self.assertIn("active_power_min_kw", inverter)
            self.assertIn("active_power_max_kw", inverter)
            self.assertIn(inverter["status"], {
                "RUNNING", "STOPPED", "UNDER_LIMIT", "OVER_LIMIT"
            })


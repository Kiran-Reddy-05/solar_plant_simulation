
"""Public pages and API routes."""
from django.contrib import admin
from django.urls import path
from plant import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.overview_page, name="overview_page"),
    path("inverters/", views.inverters_page, name="inverters_page"),
    path("about/", views.about_page, name="about_page"),
    path("api/plant/overview/", views.plant_overview_api, name="plant_overview_api"),
    path("api/data/inverter/", views.inverter_data_api, name="inverter_data_api"),
]

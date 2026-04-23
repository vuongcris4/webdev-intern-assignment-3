"""URL patterns for the scores app."""
from django.urls import path

from . import views


urlpatterns = [
    path("", views.home, name="home"),
    path("report", views.report_page, name="report"),
    path("top10-group-a", views.top10_page, name="top10"),
    path("api/lookup", views.api_lookup, name="api_lookup"),
    path("api/report", views.api_report, name="api_report"),
    path("api/top10", views.api_top10, name="api_top10"),
]

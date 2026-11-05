from django.urls import path

from . import views

app_name = "merci"

urlpatterns = [
    path("", views.merci_home, name="home"),
    path("services/", views.services_page, name="services"),
    path("<slug:slug>/", views.landing, name="landing"),
]

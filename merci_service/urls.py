from django.urls import path

from . import views

app_name = "merci_service"

urlpatterns = [
    path("", views.merci_home, name="merci_service"),
]
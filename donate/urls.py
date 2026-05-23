from django.urls import path
from . import views

urlpatterns = [
    path("donate-paypal/", views.donate_paypal, name="donate-paypal"),
    path("donate-success/", views.donate_successful, name="donate-success"),
    path("donate-failed/", views.donate_failed, name="donate-failed"),
    path("<str:lang>/donate-paypal/", views.donate_paypal, name="donate-paypal_en"),
    path(
        "<str:lang>/donate-success/", views.donate_successful, name="donate-success_en"
    ),
    path("<str:lang>/donate-failed/", views.donate_failed, name="donate-failed_en"),
]

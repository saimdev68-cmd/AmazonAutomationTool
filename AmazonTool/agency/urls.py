from django.urls import path
from .views import (
    AccountView,
    AgencySubscriptionView,
    SettingsView,
    ContactView,
)

app_name = "agency"

urlpatterns = [
    path("account/", AccountView.as_view(), name="account"),
    path("subscription/", AgencySubscriptionView.as_view(), name="agency_subscription"),
    path("settings/", SettingsView.as_view(), name="settings"),
    path("contact/", ContactView.as_view(), name="contact"),
]
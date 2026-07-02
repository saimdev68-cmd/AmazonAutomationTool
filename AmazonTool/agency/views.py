from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin


class AccountView(LoginRequiredMixin, TemplateView):
    template_name = "account.html"


class AgencySubscriptionView(LoginRequiredMixin, TemplateView):
    template_name = "agency_subscription.html"


class SettingsView(LoginRequiredMixin, TemplateView):
    template_name = "settings.html"


class ContactView(LoginRequiredMixin, TemplateView):
    template_name = "contact.html"
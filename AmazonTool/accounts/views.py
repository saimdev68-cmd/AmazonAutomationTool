from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView , LogoutView
from  django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView


# Create your views here.


class Loginview(LoginView):
    template_name = "login.html"
    
    def get_success_url(self):
        return reverse_lazy("dashboard")
    
class Logoutview(LogoutView):
    next_page = reverse_lazy('accounts:login')


class SubscriptionView(LoginRequiredMixin,TemplateView):
    
    template_name = "subscription.html"


class SpApiView(LoginRequiredMixin,TemplateView):
    
    template_name = "sp_api.html"

class AssetsView(LoginRequiredMixin,TemplateView):
    
    template_name = "assets.html"

class ReferenceView(LoginRequiredMixin,TemplateView):
    
    template_name = "reference.html"
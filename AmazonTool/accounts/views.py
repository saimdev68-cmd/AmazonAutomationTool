from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView , LogoutView
from  django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from .forms import SellerForm , UserForm
from django.shortcuts import render , redirect
from django.views import View

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


class ProfileView(LoginRequiredMixin, View):
    template_name = "profile.html"
    
    def get(self, request):
        user_form = UserForm(instance=request.user)
        
        seller_form = SellerForm(instance=request.user.seller)

        return render(request, self.template_name, {
            "user_form": user_form,
            "seller_form": seller_form
        })
    
    def post(self, request):
        user_form = UserForm(request.POST, instance=request.user)
        seller_form = SellerForm(request.POST, instance=request.user.seller)

        if user_form.is_valid() and seller_form.is_valid():
            user_form.save()
            seller_form.save()
            return redirect(request.path_info)

        return render(request, self.template_name, {
            "user_form": user_form,
            "seller_form": seller_form
        })
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView , LogoutView
from  django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView , CreateView , FormView
from .forms import SellerForm , UserForm , RegisterForm , OtpForm , LoginForm
from django.shortcuts import render , redirect , get_object_or_404
from django.views import View
from support.utils import create_audit_log
from support.models import AuditLog
from .mixins import OtpMixin 
from django.contrib import messages
from .models import User
from django.utils import timezone 
from django.contrib.auth import login , logout , authenticate
from .models import User
from .forms import RegisterForm , OtpForm , CustomPasswordForm , EmailForm , EmailOtpForm , CustomPasswordResetForm , CustomPasswordChangeForm , NameForm
from .mixins import OtpMixin , EmailOtpMixin
from django.shortcuts import render , redirect , get_object_or_404
from django.urls import reverse_lazy
from django.views import View , generic
from django.utils import timezone
from django.contrib import messages
from django.contrib.auth import login 
from django.contrib.auth.hashers import check_password
from django.contrib.auth.views import PasswordResetView , PasswordResetDoneView , PasswordResetConfirmView , PasswordResetCompleteView , PasswordChangeView , PasswordChangeDoneView
from django.contrib.auth.mixins import LoginRequiredMixin


# Create your views here.

class SignUpView(OtpMixin,CreateView):
    template_name = "signup.html"
    form_class = RegisterForm

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = False
        user.save()
        self.send_or_resend_otp(user)
        messages.success(self.request,f"OTP sent successfully. Please verify your account.")
        self.request.session["user_id"] = user.id
        return redirect ("otp_verify")

class OtpVerifyView(FormView):

    template_name = "otp_verify.html"
    form_class = OtpForm

    def dispatch(self, request, *args, **kwargs):
        if not request.session.get("user_id"):
            return redirect ("signup")
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        user_id = self.request.session.get("user_id")
        otp = form.cleaned_data.get("otp")
        user = get_object_or_404(User,id=user_id)

        if user.otp_created_at and (timezone.now() > user.otp_created_at + timezone.timedelta(minutes=5)) :
            form.add_error(None,"Otp Expired")
            return self.form_invalid(form)
            
        if user.otp_block_time and timezone.now() < user.otp_block_time:
            remaining_seconds = int((user.otp_block_time - timezone.now()).total_seconds())
            minutes = remaining_seconds // 60
            seconds = remaining_seconds % 60
            form.add_error(None,f"You have reached maximum OTP attempts. Try again in {minutes}m {seconds}s")
            return self.form_invalid(form)
             
        if check_password(otp,user.otp):
            user.is_active = True
            user.otp = None
            user.otp_created_at = None
            user.otp_block_time = None
            user.otp_attempt = 0
            user.save()
            login(self.request,user)
            messages.success(self.request,"OTP verified successfully. You are now logged in.")
            self.request.session.pop("user_id",None)
            return redirect ("dashboard")
        
        user.otp_attempt += 1
        user.save()
        remaining_attempts = 3 - user.otp_attempt

        if user.otp_attempt >= 3:
            user.otp_block_time = timezone.now() + timezone.timedelta(minutes=3)
            user.otp_attempt = 0
            user.save()
            form.add_error(None,"Maximum attempt limit reached. Try again in 3 minutes.")
            return self.form_invalid(form)
        
        form.add_error(None,f"Incorrect OTP. You have {remaining_attempts} attempts remaining.")
        return self.form_invalid(form)
    
class ResendOtpView(OtpMixin,View):

    def post(self,request):
        user_id = request.session.get("user_id")

        if not user_id:
            return redirect ("signup")
        user = get_object_or_404(User,id=user_id)

        if user.otp_created_at:
            cooldown_time = user.otp_created_at + timezone.timedelta(minutes=1)
            if timezone.now() < cooldown_time:
                remaining_seconds = int((cooldown_time - timezone.now()).total_seconds())
                minutes = remaining_seconds // 60
                seconds = remaining_seconds % 60
                messages.error(request,f"Please wait {minutes}m {seconds}s before resending OTP")
                return redirect ("otp_verify")
            
        if user.otp_block_time and user.otp_block_time > timezone.now():
                remaining_second = int((user.otp_block_time - timezone.now()).total_seconds())
                minute = remaining_second // 60
                second = remaining_second % 60
                messages.error(request,f"Try again in {minute}m {second}s")
                return redirect ("otp_verify")

        self.send_or_resend_otp(user)
        messages.success(request, "New OTP sent successfully.")
        return redirect ("otp_verify")

class LoginView(View):

    def get(self,request):
        form = LoginForm()
        return render (request,"login.html",{"form":form})
    
    def post(self,request):
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get("email")
            password = form.cleaned_data.get("password")
            user = authenticate(
                request,
                email = email ,
                password = password,
            )
            if user:
                login(request,user)
                messages.success(request,"Login Successfully")
                return redirect ("dashboard")
            else:
                messages.error(request,"Invalid Email or Password")
                return redirect ("login")
        return render (request,"login.html",{"form":form})
    
class LogoutView(View):
    def post(self,request):
        logout(request)
        return redirect ("login")
    
class PasswordresetView(PasswordResetView):
    template_name = "password_reset.html"
    form_class = CustomPasswordResetForm
    email_template_name = "password_reset_email.txt"
    subject_template_name = "password_reset_subject.txt"
    success_url = reverse_lazy("password_reset_done")

    def form_valid(self, form):
        self.request.session["password_reset_done"] = True
        return super().form_valid(form)
    
class PasswordresetdoneView(PasswordResetDoneView):
    template_name = "password_reset_done.html"

    def dispatch(self, request, *args, **kwargs):
        if not request.session.get("password_reset_done"):
            return redirect ("password_reset")
        request.session.pop("password_reset_done",None)
        return super().dispatch(request, *args, **kwargs)
    
class PasswordresetconfirmView(PasswordResetConfirmView):
    template_name = "password_reset_confirm.html"
    form_class = CustomPasswordForm
    success_url = reverse_lazy("password_reset_complete")

    def form_valid(self, form):
        self.request.session["password_reset_confirm"] = True
        return super().form_valid(form)

class PasswordresetCompleteView(PasswordResetCompleteView):
    template_name = "password_reset_complete.html"

    def dispatch(self, request, *args, **kwargs):
        if not request.session.get("password_reset_confirm"):
            return redirect ("login")
        request.session.pop("password_reset_confirm",None)
        return super().dispatch(request, *args, **kwargs)


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
    
# Create your views here.
        
class EmailUpdateView(LoginRequiredMixin,EmailOtpMixin,View):
    template_name = "email_update.html"
    
    def get(self,request):
        form = EmailForm(instance=request.user)
        return render (request,self.template_name,{
            "form":form
        })
    
    def post(self,request):
        user = request.user
        old_email = user.email
        form = EmailForm(request.POST,instance=request.user)
        if form.is_valid():
            new_email = form.cleaned_data.get("email")
            if old_email != new_email:
                user.email = old_email
                user.pending_email = new_email
                user.save()
                self.send_or_resend_email_otp(user)
                messages.success(request,f"An email verification otp is send to {user.pending_email}")
                self.request.session["email_update"] = True
                return redirect ("email_otp_verify")
            return redirect ("user_detail")
        return render (request,self.template_name,{
            "form":form
        })

class EmailOtpVerifyView(LoginRequiredMixin,generic.FormView):
    template_name = "email_otp_verify.html"
    form_class = EmailOtpForm

    def dispatch(self, request, *args, **kwargs):
        if not request.session.get("email_update"):
            return redirect ("email_update")
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        otp = form.cleaned_data.get("otp")
        user = self.request.user

        if user.otp_created_at and (timezone.now() > user.otp_created_at + timezone.timedelta(minutes=5)) :
            form.add_error(None,"Otp Expired")
            return self.form_invalid(form)
            
        if user.otp_block_time and timezone.now() < user.otp_block_time:
            remaining_seconds = int((user.otp_block_time - timezone.now()).total_seconds())
            minutes = remaining_seconds // 60
            seconds = remaining_seconds % 60
            form.add_error(None,f"You have reached maximum OTP attempts. Try again in {minutes}m {seconds}s")
            return self.form_invalid(form)
             
        if check_password(otp,user.otp):
            user.is_active = True
            user.otp = None
            user.otp_created_at = None
            user.otp_block_time = None
            user.otp_attempt = 0
            user.email = user.pending_email
            user.pending_email = None
            user.save()
            self.request.session.pop("email_update",None)
            messages.success(self.request,"OTP verified successfully. Email is updated successfully.")
            return redirect ("user_detail")
        
        user.otp_attempt += 1
        user.save()
        remaining_attempts = 3 - user.otp_attempt

        if user.otp_attempt >= 3:
            user.otp_block_time = timezone.now() + timezone.timedelta(minutes=3)
            user.otp_attempt = 0
            user.save()
            form.add_error(None,"Maximum attempt limit reached. Try again in 3 minutes.")
            return self.form_invalid(form)
        
        form.add_error(None,f"Incorrect OTP. You have {remaining_attempts} attempts remaining.")
        return self.form_invalid(form)
    
class EmailResendOtpView(EmailOtpMixin,View):

    def post(self,request):
        user = request.user

        if user.otp_created_at:
            cooldown_time = user.otp_created_at + timezone.timedelta(minutes=1)
            if timezone.now() < cooldown_time:
                remaining_seconds = int((cooldown_time - timezone.now()).total_seconds())
                minutes = remaining_seconds // 60
                seconds = remaining_seconds % 60
                messages.error(request,f"Please wait {minutes}m {seconds}s before resending OTP")
                return redirect ("email_otp_verify")
            
        if user.otp_block_time and user.otp_block_time > timezone.now():
                remaining_second = int((user.otp_block_time - timezone.now()).total_seconds())
                minute = remaining_second // 60
                second = remaining_second % 60
                messages.error(request,f"Try again in {minute}m {second}s")
                return redirect ("email_otp_verify")

        self.send_or_resend_email_otp(user)
        messages.success(request, "New OTP sent successfully.")
        return redirect ("email_otp_verify")
    
class PasswordchangeView(LoginRequiredMixin,PasswordChangeView):
    template_name = "password_change.html"
    form_class = CustomPasswordChangeForm
    success_url = reverse_lazy("password_change_done")

    def form_valid(self, form):
        self.request.session["password_change_done"] = True
        return super().form_valid(form)
    
class PasswordchangeDoneView(LoginRequiredMixin,PasswordChangeDoneView):
    template_name = "password_change_done.html"

    def dispatch(self, request, *args, **kwargs):
        if not request.session.get("password_change_done"):
            return redirect ("password_change")
        request.session.pop("password_change_done",None)
        return super().dispatch(request, *args, **kwargs)
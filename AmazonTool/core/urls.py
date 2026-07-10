"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path , include
from django.conf import settings
from django.conf.urls.static import static
from accounts import views as accounts_views
from seller import views as seller_views
from support import views as support_views
from agency  import views as agency_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path("__debug__/",include("debug_toolbar.urls")),
    path("",include("public.urls")),
    path("signup/",accounts_views.SignUpView.as_view(),name="signup"),
    path("otp-verify/",accounts_views.OtpVerifyView.as_view(),name="otp_verify"),
    path("resend-otp/",accounts_views.ResendOtpView.as_view(),name="resend_otp"),
    path("login/",accounts_views.LoginView.as_view(),name="login"),
    path("logout/",accounts_views.LogoutView.as_view(),name="logout"),
    path("password-reset/",accounts_views.PasswordresetView.as_view(),name="password_reset"),
    path("password-reset/done/",accounts_views.PasswordresetdoneView.as_view(),name="password_reset_done"),
    path('reset/<uidb64>/<token>/',accounts_views.PasswordresetconfirmView.as_view(),name='password_reset_confirm'),
    path("reset/done/",accounts_views.PasswordresetCompleteView.as_view(),name="password_reset_complete"),
    path("email-update/",accounts_views.EmailUpdateView.as_view(),name="email_update"),
    path("email/otp-verify/",accounts_views.EmailOtpVerifyView.as_view(),name="email_otp_verify"),
    path("email/resend-otp/",accounts_views.EmailResendOtpView.as_view(),name="email_resend_otp"),
    path("password/change/",accounts_views.PasswordchangeView.as_view(),name="password_change"),
    path('password/change/done/',accounts_views.PasswordchangeDoneView.as_view(),name="password_change_done"),
    path("subscription/",accounts_views.SubscriptionView.as_view(),name="subscription"),
    path("sp-api/",accounts_views.SpApiView.as_view(),name="sp_api"),
    path("assets/",accounts_views.AssetsView.as_view(),name="assets"),
    path("reference/",accounts_views.ReferenceView.as_view(),name="reference"),
    path("profile/",accounts_views.ProfileView.as_view(),name="profile"),
    path("ppc-manager/",seller_views.PPCManagerView.as_view(),name="ppc_manager"),
    path("compaign_action_button/",seller_views.CompaignActionView.as_view(),name="compaign_action"),
    path("pre_compaign/",seller_views.PreCreateCompaignView.as_view(),name="pre_compaign"),
    path("create_compaign/",seller_views.CreateCompaignView.as_view(),name="create_compaign"),
    path("export_financial_report_csv/",seller_views.export_financial_report_csv,name="export_financial_report_csv"),
    path("dashboard/",seller_views.DashboardView.as_view(),name="dashboard"),
    path("upload-cogs/",seller_views.UploadCOGSView.as_view(),name="upload_cogs"),
    path("finance/",seller_views.FinanceView.as_view(),name="finance"),
    path("brand_compaign/",seller_views.BrandCompaignView.as_view(),name="brand_compaign"),
    path("display_compaign/",seller_views.DisplayCompaignView.as_view(),name="display_compaign"),
    path("support/", support_views.SupportTicketCreateView.as_view(), name="support_create"),
    path("guidance/",support_views.UserGuideView.as_view(),name="support_user_guide"),
    path("tutorial/",support_views.VideoTutorialView.as_view(),name="support_tutorial"),
    path("history/",support_views.HistoryView.as_view(),name="history"),
    path("account/", agency_views.AccountView.as_view(), name="account"),
    path("agency/subscription/", agency_views.AgencySubscriptionView.as_view(), name="agency_subscription"),
    path("settings/", agency_views.SettingsView.as_view(), name="settings"),
    path("contact/", agency_views.ContactView.as_view(), name="contact"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL , document_root = settings.MEDIA_ROOT)

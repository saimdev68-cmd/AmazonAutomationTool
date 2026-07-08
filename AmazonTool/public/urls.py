from django.urls import path
from . import views

urlpatterns = [
    path("",views.HomeView.as_view(),name="home"),
    path("software/ai-optimization/",views.AIOptimizationView.as_view(),name="ai-optimization"),
    path("software/campaign-studio/",views.CampaignStudioView.as_view(),name="campaign-studio"),
    path("software/dayparting/",views.DayPartingView.as_view(),name="dayparting"),
    path("software/repricer/",views.RepricerView.as_view(),name="repricer"),
    path("software/financial-reports/",views.FinancialReportsView.as_view(),name="financial-reports"),
    path("software/budget-balancing/",views.BudgetBalancingView.as_view(),name="budget-balancing"),
    path("services/individual/",views.ServicesIndividualView.as_view(),name="services_individual"),
    path("services/agency/",views.ServicesAgencyView.as_view(),name="services_agency"),
    path("services/strategic-management/",views.StrategicManagementView.as_view(),name="strategic-management"),
    path("pricing/individual/", views.PricingIndividualView.as_view(), name="pricing_individual"),
    path("pricing/agency/", views.PricingAgencyView.as_view(), name="pricing_agency"),
    path("video/", views.VideoView.as_view(), name="video"),
    path("release-note/", views.ReleaseNoteView.as_view(), name="release_note"),
    path("release-note/detail/", views.ReleaseNoteDetailView.as_view(), name="release_note_detail"),
    path("success-story/", views.SuccessStoryView.as_view(), name="success_story"),
    path("user/guide/", views.PublicUserGuideView.as_view(), name="user_guide"),
    path("about-us/", views.AboutUsView.as_view(), name="about_us"),
    path("why_profitlens/", views.WhyProfitLensView.as_view(), name="why_profitlens"),
    path("contact_us/", views.ContactUsView.as_view(), name="contact_us"),
    path("referral/",views.ReferralView.as_view(),name="referral")
]

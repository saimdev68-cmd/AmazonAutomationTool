from django.shortcuts import render
from django.views.generic import TemplateView

# Create your views here.

class HomeView(TemplateView):
    template_name = "home.html"

class AIOptimizationView(TemplateView):
    template_name = "ai-optimization.html"

class CampaignStudioView(TemplateView):
    template_name = "campaign-studio.html"

class DayPartingView(TemplateView):
    template_name = "dayparting.html"

class RepricerView(TemplateView):
    template_name = "repricer.html"

class FinancialReportsView(TemplateView):
    template_name = "financial-reports.html"

class BudgetBalancingView(TemplateView):
    template_name = "budget-balancing.html"

class ServicesIndividualView(TemplateView):
    template_name = "services_individual.html"

class ServicesAgencyView(TemplateView):
    template_name = "services_agency.html"

class StrategicManagementView(TemplateView):
    template_name = "strategic-management.html"

class PricingIndividualView(TemplateView):
    template_name = "pricing_individual.html"

class PricingAgencyView(TemplateView):
    template_name = "pricing_agency.html"

class VideoView(TemplateView):
    template_name = "video.html"

class ReleaseNoteView(TemplateView):
    template_name = "release_note.html"

class ReleaseNoteDetailView(TemplateView):
    template_name = "release_note_detail.html"

class SuccessStoryView(TemplateView):
    template_name = "success_story.html"

class PublicUserGuideView(TemplateView):
    template_name = "public_user_guide.html"

class AboutUsView(TemplateView):
    template_name = "about_us.html"

class WhyProfitLensView(TemplateView):
    template_name = "why_profitlens.html"   

class ContactUsView(TemplateView):
    template_name = "contact_us.html"   

class ReferralView(TemplateView):
    template_name = "referral.html"   
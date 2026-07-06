from django.shortcuts import render
from django.views.generic import TemplateView

# Create your views here.

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
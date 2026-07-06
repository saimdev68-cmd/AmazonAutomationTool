from django.urls import path
from . import views

urlpatterns = [
    path("ai-optimization/",views.AIOptimizationView.as_view(),name="ai-optimization"),
    path("campaign-studio/",views.CampaignStudioView.as_view(),name="campaign-studio"),
    path("dayparting/",views.DayPartingView.as_view(),name="dayparting"),
    path("repricer/",views.RepricerView.as_view(),name="repricer"),
    path("financial-reports/",views.FinancialReportsView.as_view(),name="financial-reports"),
    path("budget-balancing/",views.BudgetBalancingView.as_view(),name="budget-balancing"),
]

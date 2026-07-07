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
    path("services/strategic-management/",views.StrategicManagementView.as_view(),name="strategic-management")
]

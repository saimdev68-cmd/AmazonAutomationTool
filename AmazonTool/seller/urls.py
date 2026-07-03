from django.urls import path
from . import views

urlpatterns = [
    path("dashboard/",views.DashboardView.as_view(),name="dashboard"),
    path("ppc-manager/",views.PPCManagerView.as_view(),name="ppc_manager"),
    path("upload-cogs/",views.UploadCOGSView.as_view(),name="upload_cogs"),
    path("compaign/",views.CampaignView.as_view(),name="compaign"),
    path("compaign_action_button/",views.CompaignActionView.as_view(),name="compaign_action"),
    path("finance/",views.FinanceView.as_view(),name="finance"),
]

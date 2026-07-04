from django.urls import path
from . import views

urlpatterns = [
    path("dashboard/",views.DashboardView.as_view(),name="dashboard"),
    path("ppc-manager/",views.PPCManagerView.as_view(),name="ppc_manager"),
    path("upload-cogs/",views.UploadCOGSView.as_view(),name="upload_cogs"),
    path("compaign_action_button/",views.CompaignActionView.as_view(),name="compaign_action"),
    path("finance/",views.FinanceView.as_view(),name="finance"),
    path("pre_compaign/",views.PreCreateCompaignView.as_view(),name="pre_compaign"),
    path("create_compaign/",views.CreateCompaignView.as_view(),name="create_compaign")
]

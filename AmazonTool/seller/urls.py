from django.urls import path
from . import views

urlpatterns = [
    path("ppc-manager/",views.PPCManagerView.as_view(),name="ppc_manager"),
    path("compaign_action_button/",views.CompaignActionView.as_view(),name="compaign_action"),
    path("pre_compaign/",views.PreCreateCompaignView.as_view(),name="pre_compaign"),
    path("create_compaign/",views.CreateCompaignView.as_view(),name="create_compaign"),
    path("export_financial_report_csv/",views.export_financial_report_csv,name="export_financial_report_csv"),
    path("",views.DashboardView.as_view(),name="dashboard"),
    path("upload-cogs/",views.UploadCOGSView.as_view(),name="upload_cogs"),
    path("finance/",views.FinanceView.as_view(),name="finance"),
    path("brand_compaign/",views.BrandCompaignView.as_view(),name="brand_compaign"),
    path("display_compaign/",views.DisplayCompaignView.as_view(),name="display_compaign")
]

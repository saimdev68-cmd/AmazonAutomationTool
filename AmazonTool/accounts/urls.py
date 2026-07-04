from django.urls import path
from . import views

urlpatterns = [
    path("login/",views.Loginview.as_view(),name="login"),
    path("logout/",views.Logoutview.as_view(),name="logout"),
    path("subscription/",views.SubscriptionView.as_view(),name="subscription"),
    path("sp-api/",views.SpApiView.as_view(),name="sp_api"),
    path("assets/",views.AssetsView.as_view(),name="assets"),
    path("reference/",views.ReferenceView.as_view(),name="reference"),
    path("profile/",views.ProfileView.as_view(),name="profile")
]

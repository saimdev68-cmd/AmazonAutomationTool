from django.urls import path
from .views import (
    SupportTicketListView,
    SupportTicketCreateView,
    SupportTicketDeleteView,
    UserGuideView,
    VideoTutorialView,
    HistoryView
)

app_name = "support"

urlpatterns = [
    path("", SupportTicketListView.as_view(), name="list"),
    path("create/", SupportTicketCreateView.as_view(), name="create"),
    path("delete/<int:pk>/", SupportTicketDeleteView.as_view(), name="delete"),
    path("guidance/",UserGuideView.as_view(),name="user_guide"),
    path("tutorial/",VideoTutorialView.as_view(),name="tutorial"),
    path("history/",HistoryView.as_view(),name="history"),

]
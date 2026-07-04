from django.urls import path
from .views import (
    SupportTicketListView,
    SupportTicketCreateView,
    UserGuideView,
    VideoTutorialView,
    HistoryView
)


urlpatterns = [
    path("", SupportTicketListView.as_view(), name="support_list"),
    path("create/", SupportTicketCreateView.as_view(), name="support_create"),
    path("guidance/",UserGuideView.as_view(),name="support_user_guide"),
    path("tutorial/",VideoTutorialView.as_view(),name="support_tutorial"),
    path("history/",HistoryView.as_view(),name="history"),

]
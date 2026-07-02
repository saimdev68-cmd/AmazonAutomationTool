from django.views.generic import ListView, CreateView, DeleteView , TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .models import SupportTicket
from .forms import SupportTicketForm


# 📌 LIST VIEW
class SupportTicketListView(LoginRequiredMixin, ListView):
    model = SupportTicket
    template_name = "support_list.html"
    context_object_name = "tickets"

    def get_queryset(self):
        return SupportTicket.objects.filter(
            vendor=self.request.user.vendor
        ).order_by("-created_at")


# 📌 CREATE VIEW
class SupportTicketCreateView(LoginRequiredMixin, CreateView):
    model = SupportTicket
    form_class = SupportTicketForm
    template_name = "support_create.html"
    success_url = reverse_lazy("support:list")

    def form_valid(self, form):
        form.instance.vendor = self.request.user.vendor
        return super().form_valid(form)


# 📌 DELETE VIEW
class SupportTicketDeleteView(LoginRequiredMixin, DeleteView):
    success_url = reverse_lazy("support:list")

    def get_queryset(self):
        return SupportTicket.objects.filter(
            vendor=self.request.user.vendor
        )
    
class UserGuideView(LoginRequiredMixin,TemplateView):
    template_name = "user_guide.html"


class VideoTutorialView(LoginRequiredMixin,TemplateView):
    template_name = "video_tutorial.html"
    

class HistoryView(LoginRequiredMixin,TemplateView):
    template_name = "history.html"
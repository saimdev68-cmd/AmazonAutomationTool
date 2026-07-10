from django.views.generic import CreateView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .models import SupportTicket
from .forms import SupportTicketForm

class SupportTicketCreateView(LoginRequiredMixin, CreateView):
    model = SupportTicket
    form_class = SupportTicketForm
    template_name = "support_create.html"
    success_url = reverse_lazy("dashboard")

    def form_valid(self, form):
        form.instance.seller = self.request.user.seller
        return super().form_valid(form)
    
class UserGuideView(LoginRequiredMixin,TemplateView):
    template_name = "user_guide.html"


class VideoTutorialView(LoginRequiredMixin,TemplateView):
    template_name = "video_tutorial.html"
    

class HistoryView(LoginRequiredMixin,TemplateView):
    template_name = "history.html"
from django.views.generic import TemplateView
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from django.urls import reverse_lazy


class IndexView(TemplateView):
    template_name = 'task_manager/index.html'


class LoginUserView(LoginView):
    template_name = 'task_manager/login.html'
    next_page = reverse_lazy('index')
    
    def form_valid(self, form):
        messages.success(self.request, _('You are logged in'))
        return super().form_valid(form)


class LogoutUserView(LogoutView):
    next_page = reverse_lazy('index')
    
    def dispatch(self, request, *args, **kwargs):
        messages.info(request, _('You are logged out'))
        return super().dispatch(request, *args, **kwargs)

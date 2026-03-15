from django.contrib import messages
from django.contrib.auth.views import LoginView, LogoutView
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import TemplateView


class IndexView(TemplateView):
    template_name = 'task_manager/index.html'


class LoginUserView(LoginView):
    template_name = 'task_manager/login.html'
    next_page = reverse_lazy('index')

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, _('You are logged in'))
        return response


class LogoutUserView(LogoutView):
    next_page = reverse_lazy('index')

    def dispatch(self, request, *args, **kwargs):
        messages.info(request, _('You are logged out'))
        return super().dispatch(request, *args, **kwargs)


def trigger_error(request):
    """Тестовый view для проверки Rollbar"""
    1 / 0  # noqa: B018
    return HttpResponse("This should not appear")

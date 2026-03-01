from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.contrib import messages
from django.shortcuts import redirect
from django.db.models import ProtectedError
from task_manager.models import Status
from django import forms


class StatusForm(forms.ModelForm):
    class Meta:
        model = Status
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
        }


class StatusListView(LoginRequiredMixin, ListView):
    model = Status
    template_name = 'task_manager/statuses/list.html'
    context_object_name = 'statuses'
    login_url = reverse_lazy('login')
    
    def handle_no_permission(self):
        messages.error(self.request, _('You are not authorized! Please log in.'))
        return redirect('login')


class StatusCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Status
    form_class = StatusForm
    template_name = 'task_manager/statuses/create.html'
    success_url = reverse_lazy('statuses_list')
    success_message = _('Status successfully created')
    login_url = reverse_lazy('login')
    
    def handle_no_permission(self):
        messages.error(self.request, _('You are not authorized! Please log in.'))
        return redirect('login')


class StatusUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Status
    form_class = StatusForm
    template_name = 'task_manager/statuses/update.html'
    success_url = reverse_lazy('statuses_list')
    success_message = _('Status successfully updated')
    login_url = reverse_lazy('login')
    
    def handle_no_permission(self):
        messages.error(self.request, _('You are not authorized! Please log in.'))
        return redirect('login')


class StatusDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Status
    template_name = 'task_manager/statuses/delete.html'
    success_url = reverse_lazy('statuses_list')
    success_message = _('Status successfully deleted')
    login_url = reverse_lazy('login')
    
    def handle_no_permission(self):
        messages.error(self.request, _('You are not authorized! Please log in.'))
        return redirect('login')
    
    def form_valid(self, form):
        try:
            self.object.delete()
            messages.success(self.request, self.success_message)
        except ProtectedError:
            messages.error(
                self.request,
                _('Cannot delete status because it is in use')
            )
            return redirect('statuses_list')
        return redirect(self.success_url)

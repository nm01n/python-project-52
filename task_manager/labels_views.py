from django import forms
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from task_manager.models import Label


class LabelForm(forms.ModelForm):
    class Meta:
        model = Label
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
        }


class LabelListView(LoginRequiredMixin, ListView):
    model = Label
    template_name = 'task_manager/labels/list.html'
    context_object_name = 'labels'
    login_url = reverse_lazy('login')

    def handle_no_permission(self):
        messages.error(self.request, _('You are not authorized! Please log in.'))
        return redirect('login')


class LabelCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Label
    form_class = LabelForm
    template_name = 'task_manager/labels/create.html'
    success_url = reverse_lazy('labels_list')
    success_message = _('Label successfully created')
    login_url = reverse_lazy('login')

    def handle_no_permission(self):
        messages.error(self.request, _('You are not authorized! Please log in.'))
        return redirect('login')


class LabelUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Label
    form_class = LabelForm
    template_name = 'task_manager/labels/update.html'
    success_url = reverse_lazy('labels_list')
    success_message = _('Label successfully updated')
    login_url = reverse_lazy('login')

    def handle_no_permission(self):
        messages.error(self.request, _('You are not authorized! Please log in.'))
        return redirect('login')


class LabelDeleteView(LoginRequiredMixin, DeleteView):
    model = Label
    template_name = 'task_manager/labels/delete.html'
    success_url = reverse_lazy('labels_list')
    login_url = reverse_lazy('login')

    def handle_no_permission(self):
        messages.error(self.request, _('You are not authorized! Please log in.'))
        return redirect('login')

    def form_valid(self, form):
        label = self.get_object()
        # Проверяем используется ли метка в задачах
        if label.tasks.exists():
            messages.error(
                self.request,
                _('Cannot delete label because it is in use')
            )
            return redirect(self.success_url)

        messages.success(self.request, _('Label successfully deleted'))
        return super().form_valid(form)

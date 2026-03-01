from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.contrib import messages
from django.shortcuts import redirect
from django.db.models import ProtectedError
from task_manager.models import Label
from django import forms


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


class LabelDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Label
    template_name = 'task_manager/labels/delete.html'
    success_url = reverse_lazy('labels_list')
    success_message = _('Label successfully deleted')
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
                _('Cannot delete label because it is in use')
            )
        return redirect(self.success_url)

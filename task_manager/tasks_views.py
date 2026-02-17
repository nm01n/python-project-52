from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.contrib import messages
from django.shortcuts import redirect
from task_manager.models import Task
from django import forms


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['name', 'description', 'status', 'executor']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'executor': forms.Select(attrs={'class': 'form-select'}),
        }


class TaskListView(LoginRequiredMixin, ListView):
    model = Task
    template_name = 'task_manager/tasks/list.html'
    context_object_name = 'tasks'
    login_url = reverse_lazy('login')

    def handle_no_permission(self):
        messages.error(self.request, _('You are not authorized! Please log in.'))
        return redirect('login')


class TaskDetailView(LoginRequiredMixin, DetailView):
    model = Task
    template_name = 'task_manager/tasks/detail.html'
    context_object_name = 'task'
    login_url = reverse_lazy('login')

    def handle_no_permission(self):
        messages.error(self.request, _('You are not authorized! Please log in.'))
        return redirect('login')


class TaskCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Task
    form_class = TaskForm
    template_name = 'task_manager/tasks/create.html'
    success_url = reverse_lazy('tasks_list')
    success_message = _('Task successfully created')
    login_url = reverse_lazy('login')

    def handle_no_permission(self):
        messages.error(self.request, _('You are not authorized! Please log in.'))
        return redirect('login')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class TaskUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Task
    form_class = TaskForm
    template_name = 'task_manager/tasks/update.html'
    success_url = reverse_lazy('tasks_list')
    success_message = _('Task successfully updated')
    login_url = reverse_lazy('login')

    def handle_no_permission(self):
        messages.error(self.request, _('You are not authorized! Please log in.'))
        return redirect('login')


class TaskDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Task
    template_name = 'task_manager/tasks/delete.html'
    success_url = reverse_lazy('tasks_list')
    success_message = _('Task successfully deleted')
    login_url = reverse_lazy('login')

    def handle_no_permission(self):
        messages.error(self.request, _('You are not authorized! Please log in.'))
        return redirect('login')

    def dispatch(self, request, *args, **kwargs):
        task = self.get_object()
        if task.author != request.user:
            messages.error(
                request,
                _('A task can only be deleted by its author')
            )
            return redirect('tasks_list')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        messages.success(self.request, self.success_message)
        return super().form_valid(form)

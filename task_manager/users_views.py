from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.contrib import messages
from django.shortcuts import redirect
from django import forms


class UserForm(UserCreationForm):
    first_name = forms.CharField(max_length=150, required=True, label=_('First name'))
    last_name = forms.CharField(max_length=150, required=True, label=_('Last name'))
    
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'password1', 'password2')


class UserListView(ListView):
    model = User
    template_name = 'task_manager/users/list.html'
    context_object_name = 'users'
    ordering = ['id']


class UserCreateView(SuccessMessageMixin, CreateView):
    model = User
    form_class = UserForm
    template_name = 'task_manager/users/create.html'
    success_url = reverse_lazy('login')
    success_message = _('User successfully registered')


class UserUpdateView(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, UpdateView):
    model = User
    form_class = UserForm
    template_name = 'task_manager/users/update.html'
    success_url = reverse_lazy('users_list')
    success_message = _('User successfully updated')
    login_url = reverse_lazy('login')
    
    def test_func(self):
        return self.get_object() == self.request.user
    
    def handle_no_permission(self):
        messages.error(self.request, _('You do not have permission to modify another user'))
        return redirect('users_list')


class UserDeleteView(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, DeleteView):
    model = User
    template_name = 'task_manager/users/delete.html'
    success_url = reverse_lazy('users_list')
    success_message = _('User successfully deleted')
    login_url = reverse_lazy('login')
    
    def test_func(self):
        return self.get_object() == self.request.user
    
    def handle_no_permission(self):
        messages.error(self.request, _('You do not have permission to delete another user'))
        return redirect('users_list')
    
    def form_valid(self, form):
        messages.success(self.request, self.success_message)
        return super().form_valid(form)

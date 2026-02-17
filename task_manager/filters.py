import django_filters
from django import forms
from django.utils.translation import gettext_lazy as _
from task_manager.models import Task, Label
from django.contrib.auth.models import User


class TaskFilter(django_filters.FilterSet):
    label = django_filters.ModelChoiceFilter(
        queryset=Label.objects.all(),
        label=_('Label'),
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    
    executor = django_filters.ModelChoiceFilter(
        queryset=User.objects.all(),
        label=_('Executor'),
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    
    self_tasks = django_filters.BooleanFilter(
        method='filter_self_tasks',
        label=_('Only my tasks'),
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )

    class Meta:
        model = Task
        fields = ['status', 'executor', 'label', 'self_tasks']
        widgets = {
            'status': forms.Select(attrs={'class': 'form-select'}),
        }

    def filter_self_tasks(self, queryset, name, value):
        if value:
            user = self.request.user
            return queryset.filter(author=user)
        return queryset

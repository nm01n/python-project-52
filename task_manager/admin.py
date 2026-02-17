from django.contrib import admin
from task_manager.models import Status, Task, Label


@admin.register(Status)
class StatusAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'created_at')
    search_fields = ('name',)


@admin.register(Label)
class LabelAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'created_at')
    search_fields = ('name',)


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'status', 'author', 'executor', 'created_at')
    search_fields = ('name',)
    list_filter = ('status', 'labels')
    filter_horizontal = ('labels',)

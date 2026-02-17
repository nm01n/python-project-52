from django.contrib import admin
from task_manager.models import Status, Task


@admin.register(Status)
class StatusAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'created_at')
    search_fields = ('name',)


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'status', 'author', 'executor', 'created_at')
    search_fields = ('name',)
    list_filter = ('status',)

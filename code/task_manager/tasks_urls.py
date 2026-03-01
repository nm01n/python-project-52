from django.urls import path
from task_manager import tasks_views

urlpatterns = [
    path('', tasks_views.TaskListView.as_view(), name='tasks_list'),
    path('create/', tasks_views.TaskCreateView.as_view(), name='task_create'),
    path('<int:pk>/', tasks_views.TaskDetailView.as_view(), name='task_detail'),
    path('<int:pk>/update/', tasks_views.TaskUpdateView.as_view(), name='task_update'),
    path('<int:pk>/delete/', tasks_views.TaskDeleteView.as_view(), name='task_delete'),
]

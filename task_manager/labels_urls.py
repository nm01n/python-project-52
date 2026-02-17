from django.urls import path
from task_manager import labels_views

urlpatterns = [
    path('', labels_views.LabelListView.as_view(), name='labels_list'),
    path('create/', labels_views.LabelCreateView.as_view(), name='label_create'),
    path('<int:pk>/update/', labels_views.LabelUpdateView.as_view(), name='label_update'),
    path('<int:pk>/delete/', labels_views.LabelDeleteView.as_view(), name='label_delete'),
]

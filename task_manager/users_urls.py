from django.urls import path
from task_manager import users_views

urlpatterns = [
    path('', users_views.UserListView.as_view(), name='users_list'),
    path('create/', users_views.UserCreateView.as_view(), name='user_create'),
    path('<int:pk>/update/', users_views.UserUpdateView.as_view(), name='user_update'),
    path('<int:pk>/delete/', users_views.UserDeleteView.as_view(), name='user_delete'),
]

from django.contrib import admin
from django.urls import path, include
from task_manager import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.IndexView.as_view(), name='index'),
    path('users/', include('task_manager.users_urls')),
    path('statuses/', include('task_manager.statuses_urls')),
    path('login/', views.LoginUserView.as_view(), name='login'),
    path('logout/', views.LogoutUserView.as_view(), name='logout'),
]

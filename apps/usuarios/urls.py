from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView

from apps.usuarios import views


urlpatterns = [
    path('add/', views.usuarios, name='usuarios'),
    path('edit/<int:pk>/', views.usuarios, name='edit_usuarios'),
    path('delete/', views.delete_usuarios, name='delete_usuarios'),
    path('change/password/', views.change_password, name='change_password'),

    path('login/', views.login, name='login-form'),
    path('login-validation/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
]

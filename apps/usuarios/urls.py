from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView

from apps.usuarios import views


urlpatterns = [
    path('login/', views.login, name='login-form'),
    path('cadastro_usuarios/', views.cadastro_usuarios, name='cadastro_usuarios'),

    path('login-validation/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
]

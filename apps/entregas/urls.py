from django.urls import path

from apps.entregas import views


urlpatterns = [
    path('entregadores', views.entregadores, name='entregadores'),
    path('entregas', views.entregas, name='entregas'),
]

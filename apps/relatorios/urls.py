from django.urls import path

from apps.relatorios import views


urlpatterns = [
    path('', views.index, name='index'),
    path('create', views.gerar, name='gerar'),
]

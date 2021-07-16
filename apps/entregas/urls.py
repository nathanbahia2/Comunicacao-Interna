from django.urls import path

from apps.entregas import views


urlpatterns = [
    path('entregadores', views.entregadores, name='entregadores'),
    path('entregadores/edit/<int:pk>/', views.entregadores, name='edit_entregadores'),
    path('entregas', views.entregas, name='entregas'),
    path('entregas/info', views.info_entregas, name='info_entregas'),
    path('entregas/edit/<int:pk>/', views.entregas, name='edit_entregas'),
    path('finalizar/', views.finaliza_entrega, name='finaliza_entrega'),
    path('consulta', views.consulta_entregas, name='consulta_entregas'),
]

from django.urls import path

from apps.core import views


urlpatterns = [
    path('', views.index, name='index'),
    path('cargos', views.cargos, name='cargos'),
    path('filiais', views.filiais, name='filiais'),
    path('funcionarios', views.funcionarios, name='funcionarios'),
    path('motivos', views.motivos, name='motivos'),
    path('ocorrencias', views.ocorrencias, name='ocorrencias'),
    path('ocorrencias/consulta', views.consulta_ocorrencias, name='consulta_ocorrencias'),
    path('ocorrencias/info', views.info_ocorrencias, name='info_ocorrencias'),
    path('ocorrencias/delete/', views.delete_ocorrencias, name='delete_ocorrencias'),
    path('elogios', views.elogios, name='elogios'),
    path('elogios/consulta', views.consulta_elogios, name='consulta_elogios'),
    path('elogios/info', views.info_elogios, name='info_elogios'),
    path('elogios/delete/', views.delete_elogios, name='delete_elogios'),
]

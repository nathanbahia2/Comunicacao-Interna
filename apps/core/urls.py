from django.urls import path

from apps.core import views


urlpatterns = [
    path('', views.index, name='index'),

    path('cargos', views.cargos, name='cargos'),
    path('cargos/edit/<int:pk>/', views.cargos, name='edit_cargos'),

    path('filiais', views.filiais, name='filiais'),

    path('motivos', views.motivos, name='motivos'),
    path('motivos/edit/<int:pk>/', views.motivos, name='edit_motivos'),

    path('funcionarios', views.funcionarios, name='funcionarios'),
    path('funcionarios/edit/<int:pk>/', views.funcionarios, name='edit_funcionarios'),

    path('ocorrencias', views.ocorrencias, name='ocorrencias'),
    path('ocorrencias/consulta', views.consulta_ocorrencias, name='consulta_ocorrencias'),
    path('ocorrencias/info', views.info_ocorrencias, name='info_ocorrencias'),
    path('ocorrencias/edit/<int:pk>/', views.ocorrencias, name='edit_ocorrencias'),

    path('elogios', views.elogios, name='elogios'),
    path('elogios/consulta', views.consulta_elogios, name='consulta_elogios'),
    path('elogios/info', views.info_elogios, name='info_elogios'),
    path('elogios/edit/<int:pk>/', views.elogios, name='edit_elogios'),

    path('delete/obj/', views.delete_model_object),

    path('change/filial/', views.altera_filial, name='altera_filial'),
]

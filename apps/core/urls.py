from django.urls import path

from apps.core import views


urlpatterns = [
    path('', views.index, name='index'),
    path('sobre', views.sobre, name='sobre'),

    path('cargos', views.cargos, name='cargos'),
    path('cargos/edit/<int:pk>/', views.cargos, name='edit_cargos'),

    path('filiais', views.filiais, name='filiais'),

    path('emails', views.emails, name='emails'),
    path('emails/edit/<int:pk>/', views.emails, name='edit_emails'),

    path('motivos', views.motivos, name='motivos'),
    path('motivos/edit/<int:pk>/', views.motivos, name='edit_motivos'),

    path('funcionarios', views.funcionarios, name='funcionarios'),
    path('funcionarios/edit/<int:pk>/', views.funcionarios, name='edit_funcionarios'),
    path('funcionarios/cargo/<int:pk>/', views.funcionarios_cargo, name='funcionarios_cargo'),

    path('ocorrencias', views.ocorrencias, name='ocorrencias'),
    path('ocorrencias/consulta', views.consulta_ocorrencias, name='consulta_ocorrencias'),
    path('ocorrencias/info', views.info_ocorrencias, name='info_ocorrencias'),
    path('ocorrencias/edit/<int:pk>/', views.ocorrencias, name='edit_ocorrencias'),
    path('ocorrencias/funcionario/<int:pk>/', views.ocorrencias_funcionario, name='ocorrencias_funcionario'),

    path('elogios', views.elogios, name='elogios'),
    path('elogios/consulta', views.consulta_elogios, name='consulta_elogios'),
    path('elogios/info', views.info_elogios, name='info_elogios'),
    path('elogios/edit/<int:pk>/', views.elogios, name='edit_elogios'),
    path('elogios/funcionario/<int:pk>/', views.elogios_funcionario, name='elogios_funcionario'),

    path('delete/obj/', views.delete_model_object),

    path('change/filial/', views.altera_filial, name='altera_filial'),
]

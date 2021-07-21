from django.contrib import admin

from apps.core import models


@admin.register(models.Ocorrencia)
class OcorrenciaAdmin(admin.ModelAdmin):
    list_display = ['data', 'funcionario', 'filial', 'motivo', 'ativo']
    list_editable = ['ativo']

    def filial(self, object):
        return object.funcionario.filial


@admin.register(models.Elogio)
class ElogioAdmin(admin.ModelAdmin):
    list_display = ['data', 'funcionario', 'filial', 'ativo']
    list_editable = ['ativo']

    def filial(self, object):
        return object.funcionario.filial


@admin.register(models.Cargo)
class CargoAdmin(admin.ModelAdmin):
    list_display = ['nome', 'filial', 'ativo']
    list_editable = ['ativo']


@admin.register(models.Funcionario)
class FuncionarioAdmin(admin.ModelAdmin):
    list_display = ['nome', 'cargo', 'filial', 'ativo']
    list_editable = ['ativo']


admin.site.register(models.Filial)
admin.site.register(models.Motivo)
admin.site.register(models.EmailResponsaveis)
admin.site.register(models.EmailNaoEntregue)

from django.contrib import admin

from apps.core import models


@admin.register(models.Ocorrencia)
class OcorrenciaAdmin(admin.ModelAdmin):
    list_display = ['data', 'funcionario', 'filial', 'motivo', 'ativo']
    list_editable = ['ativo']

    def filial(self, object):
        return object.funcionario.filial


admin.site.register(models.Filial)
admin.site.register(models.Cargo)
admin.site.register(models.Funcionario)
admin.site.register(models.Motivo)
admin.site.register(models.Elogio)
admin.site.register(models.EmailResponsaveis)
admin.site.register(models.EmailNaoEntregue)

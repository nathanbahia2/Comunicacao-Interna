import csv

from django.contrib import admin
from django.http import HttpResponse

from apps.core import models


def export_as_csv(self, request, queryset):

    meta = self.model._meta
    field_names = [field.name for field in meta.fields]

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename={}.csv'.format(meta)
    writer = csv.writer(response)

    writer.writerow(field_names)
    for obj in queryset:
        row = writer.writerow([getattr(obj, field) for field in field_names])

    return response


@admin.register(models.Ocorrencia)
class OcorrenciaAdmin(admin.ModelAdmin):
    list_display = ['data', 'funcionario', 'motivo', 'ativo']
    list_editable = ['ativo']
    actions = [export_as_csv]


@admin.register(models.Elogio)
class ElogioAdmin(admin.ModelAdmin):
    list_display = ['data', 'funcionario', 'ativo']
    list_editable = ['ativo']
    actions = [export_as_csv]


@admin.register(models.Cargo)
class CargoAdmin(admin.ModelAdmin):
    list_display = ['nome', 'ativo']
    list_editable = ['ativo']
    actions = [export_as_csv]


@admin.register(models.Funcionario)
class FuncionarioAdmin(admin.ModelAdmin):
    list_display = ['nome', 'cargo', 'ativo']
    list_editable = ['ativo']
    actions = [export_as_csv]


admin.site.register(models.Filial)
admin.site.register(models.Motivo)
admin.site.register(models.EmailResponsaveis)
admin.site.register(models.EmailNaoEntregue)

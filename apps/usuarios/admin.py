from django.contrib import admin

from apps.usuarios import models


@admin.register(models.Perfil)
class PerfilAdmin(admin.ModelAdmin):
    list_display = ['usuario', 'filial', 'tipo', 'ativo']

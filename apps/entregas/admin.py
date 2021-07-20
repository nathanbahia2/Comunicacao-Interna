from django.contrib import admin

from apps.entregas import models


@admin.register(models.Entrega)
class EntregaAdmin(admin.ModelAdmin):
    list_display = ['saida_pedido', 'recebimento_pedido', 'numero_pedido', 'valor_pedido', 'filial_pedido', 'ativo']
    list_editable = ['ativo']


admin.site.register(models.Entregador)

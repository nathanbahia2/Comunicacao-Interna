from django.contrib import admin

from apps.entregas import models


admin.site.register(models.Entregador)
admin.site.register(models.Entrega)

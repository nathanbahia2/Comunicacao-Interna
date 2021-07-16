from django.contrib import admin

from apps.core import models


admin.site.register(models.Filial)
admin.site.register(models.Cargo)
admin.site.register(models.Funcionario)
admin.site.register(models.Ocorrencia)
admin.site.register(models.Motivo)
admin.site.register(models.Elogio)
admin.site.register(models.EmailResponsaveis)
admin.site.register(models.EmailNaoEntregue)

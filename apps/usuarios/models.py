from django.db import models
from django.contrib.auth import get_user_model

from apps.core.models import Filial
from apps.usuarios import choices


class Perfil(models.Model):
    usuario = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    filial = models.ForeignKey(Filial, on_delete=models.CASCADE)
    tipo = models.CharField(max_length=3, choices=choices.TIPO_USUARIO, default='1')

    def __str__(self) -> str:
        return self.usuario.first_name

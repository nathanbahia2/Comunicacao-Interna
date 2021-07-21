from django.contrib.auth.models import User
from django.db import models

from apps.core.models import Base


class Entregador(Base):
    nome = models.CharField(max_length=255)
    filial = models.ForeignKey('core.Filial', on_delete=models.CASCADE)
    telefone = models.CharField(max_length=20, blank=True, null=True)
    veiculo = models.CharField(max_length=255, blank=True, null=True)
    placa = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return self.nome

    class Meta:
        ordering = ['nome']
        verbose_name = 'Entregador'
        verbose_name_plural = 'Entregadores'


class Entrega(Base):
    nome_cliente = models.CharField(max_length=255)
    endereco_cliente = models.CharField(max_length=255)
    numero_pedido = models.CharField(max_length=255)
    valor_pedido = models.DecimalField(max_digits=10, decimal_places=2)
    saida_pedido = models.DateTimeField()
    filial_pedido = models.ForeignKey('core.Filial', on_delete=models.CASCADE)
    recebimento_pedido = models.DateTimeField(blank=True, null=True)
    detalhes_pedido = models.TextField(blank=True, null=True)
    observacao_final = models.TextField(blank=True, null=True)
    usuario_recebimento = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, related_name='usuario_recebimento')
    entregador = models.ForeignKey(Entregador, on_delete=models.SET_NULL, null=True)

    class Meta:
        ordering = ['saida_pedido']

    @property
    def recebida(self):
        if self.usuario_recebimento:
            return True
        return False

    @property
    def recebimento(self):
        if self.usuario_recebimento:
            if self.recebimento_pedido:
                return f'{self.usuario_recebimento.get_full_name()} em {self.recebimento_pedido.strftime("%d/%m/%Y %H:%M")}'
            return self.usuario_recebimento.get_full_name()
        else:
            if self.recebimento_pedido:
                return self.recebimento_pedido.strftime("%d/%m/%Y %H:%M")
        return 'Pendente'

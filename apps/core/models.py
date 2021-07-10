from django.db import models
from django.contrib.auth import get_user_model


class Base(models.Model):
    usuario = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, null=True)
    criacao = models.DateTimeField(auto_now_add=True)
    alteracao = models.DateTimeField(auto_now=True)
    ativo = models.BooleanField(default=True)

    class Meta:
        abstract = True

    @property
    def cadastro(self):
        if self.usuario:
            return f"{self.usuario.get_full_name()} em {self.criacao.strftime('%d/%m/%Y')}"
        return f"Usuário excluído em {self.criacao.strftime('%d/%m/%Y')}"


class Filial(Base):
    nome = models.CharField(max_length=255)
    cidade = models.CharField(max_length=255)

    def __str__(self):
        return f'{self.nome} - {self.cidade}'

    class Meta:
        ordering = ['nome', 'cidade']


class Cargo(Base):
    nome = models.CharField(max_length=255)
    filial = models.ForeignKey(Filial, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.nome} - {self.filial}'

    class Meta:
        ordering = ['nome']


class Funcionario(Base):
    nome = models.CharField(max_length=255)
    admissao = models.DateField(blank=True, null=True)
    cargo = models.ForeignKey(Cargo, on_delete=models.SET_NULL, null=True, related_name='funcionarios')
    filial = models.ForeignKey(Filial, on_delete=models.CASCADE, related_name='funcionarios')

    def __str__(self):
        return f'{self.nome} - {self.cargo} - {self.filial}'

    class Meta:
        ordering = ['nome']


class Motivo(Base):
    nome = models.CharField(max_length=255)
    filial = models.ForeignKey(Filial, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.nome} - {self.filial}'

    class Meta:
        ordering = ['nome']


class Ocorrencia(Base):
    funcionario = models.ForeignKey(Funcionario, on_delete=models.CASCADE, related_name='ocorrencias')
    motivo = models.ForeignKey(Motivo, on_delete=models.SET_NULL, null=True)
    data = models.DateField()
    observacao = models.TextField()

    def __str__(self):
        return self.observacao or '---------'

    class Meta:
        ordering = ['data']

    @property
    def get_motivo_display(self):
        if self.motivo:
            return self.motivo.nome
        return 'Motivo excluído'

    @property
    def get_usuario_display(self):
        if self.usuario:
            return self.usuario.get_full_name()
        return 'Usuário excluído'


class Elogio(Base):
    funcionario = models.ForeignKey(Funcionario, on_delete=models.CASCADE, related_name='elogios')
    data = models.DateField()
    observacao = models.TextField()

    def __str__(self):
        return self.funcionario.nome

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
            return f"{self.usuario.get_full_name()} em {self.criacao.strftime('%d/%m/%Y %H:%M')}"
        return f"Usuário excluído em {self.criacao.strftime('%d/%m/%Y')}"

    @property
    def get_usuario_display(self):
        if self.usuario:
            return self.usuario.get_full_name()
        return 'Usuário excluído'


class Filial(Base):
    nome = models.CharField(max_length=255)
    cidade = models.CharField(max_length=255)

    def __str__(self):
        return f'{self.nome} - {self.cidade}'

    class Meta:
        verbose_name = 'Filial'
        verbose_name_plural = 'Filiais'
        ordering = ['nome', 'cidade']


class Cargo(Base):
    nome = models.CharField(max_length=255)
    filial = models.ForeignKey(Filial, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.nome}'

    class Meta:
        verbose_name = 'Cargo'
        verbose_name_plural = 'Cargos'
        ordering = ['nome']


class Funcionario(Base):
    nome = models.CharField(max_length=255)
    admissao = models.DateField(blank=True, null=True)
    cargo = models.ForeignKey(Cargo, on_delete=models.SET_NULL, null=True, related_name='funcionarios')
    filial = models.ForeignKey(Filial, on_delete=models.CASCADE, related_name='funcionarios')

    def __str__(self):
        return f'{self.nome} - {self.cargo}'

    class Meta:
        verbose_name = 'Funcionário'
        verbose_name_plural = 'Funcionários'
        ordering = ['nome']


class Motivo(Base):
    nome = models.CharField(max_length=255)
    filial = models.ForeignKey(Filial, on_delete=models.CASCADE)

    def __str__(self):
        return self.nome

    class Meta:
        verbose_name = 'Motivo'
        verbose_name_plural = 'Motivos'
        ordering = ['nome']


class Ocorrencia(Base):
    funcionario = models.ForeignKey(Funcionario, on_delete=models.CASCADE, related_name='ocorrencias')
    motivo = models.ForeignKey(Motivo, on_delete=models.SET_NULL, null=True)
    data = models.DateField()
    observacao = models.TextField()

    def __str__(self):
        return self.observacao or '---------'

    class Meta:
        verbose_name = 'Ocorrência'
        verbose_name_plural = 'Ocorrências'
        ordering = ['-data'] 

    @property
    def get_motivo_display(self):
        if self.motivo:
            return self.motivo.nome
        return 'Motivo excluído'


class Elogio(Base):
    funcionario = models.ForeignKey(Funcionario, on_delete=models.CASCADE, related_name='elogios')
    data = models.DateField()
    observacao = models.TextField()

    def __str__(self):
        return self.funcionario.nome

    class Meta:
        verbose_name = 'Elogio'
        verbose_name_plural = 'Elogios'
        ordering = ['-data']        


class EmailResponsaveis(Base):
    nome = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    filiais = models.ManyToManyField(Filial)

    def __str__(self):
        return self.nome

    class Meta:
        verbose_name = 'Cadastro de e-mail dos responsáveis'
        verbose_name_plural = 'Cadastro de e-mail dos responsáveis'
        ordering = ['nome']


class EmailNaoEntregue(models.Model):
    data = models.DateTimeField(auto_now_add=True)
    filial = models.ForeignKey(Filial, on_delete=models.CASCADE)
    tipo = models.CharField(max_length=20)
    assunto = models.CharField(max_length=255)
    mensagem = models.TextField()
    retorno = models.TextField()
    ativo = models.BooleanField(default=True)

    def __str__(self):
        return self.assunto

    class Meta:
        verbose_name = 'E-mail não entregue'
        verbose_name_plural = 'E-mails não entregues'
        ordering = ['-data']

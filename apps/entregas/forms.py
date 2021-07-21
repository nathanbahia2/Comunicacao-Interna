from django import forms

from apps.core.models import Filial
from apps.entregas import models


class EntregadorForm(forms.ModelForm):
    nome = forms.CharField(
        label='Nome do entregador',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'required': True
            }
        )
    )

    telefone = forms.CharField(
        label='Telefone do entregador',
        required=False,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'required': False
            }
        )
    )

    veiculo = forms.CharField(
        label='Veículo utilizado para entregas',
        required=False,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'required': False
            }
        )
    )

    placa = forms.CharField(
        label='Placa do veículo',
        required=False,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'required': False
            }
        )
    )

    filial = forms.ModelChoiceField(
        label='Filial',
        queryset=Filial.objects.all(),
        widget=forms.Select(
            attrs={
                'class': 'form-control',
                'required': True
            }
        )
    )

    class Meta:
        model = models.Entregador
        fields = ['nome', 'telefone', 'veiculo', 'placa', 'filial']

    def __init__(self, usuario, *args, **kwargs):
        super(EntregadorForm, self).__init__(*args, **kwargs)

        self.fields['filial'].queryset = Filial.objects.filter(id=usuario.filial.id)
        self.fields['filial'].initial = usuario.filial


class EntregaForm(forms.ModelForm):
    nome_cliente = forms.CharField(
        label='Nome do cliente',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'required': True
            }
        )
    )

    endereco_cliente = forms.CharField(
        label='Endereço do cliente',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'required': True
            }
        )
    )

    numero_pedido = forms.CharField(
        label='Número do pedido',
        required=False,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
            }
        )
    )

    valor_pedido = forms.DecimalField(
        label='Valor do pedido',
        widget=forms.NumberInput(
            attrs={
                'class': 'form-control',
                'step': 'any',
                'required': True
            }
        )
    )

    saida_pedido = forms.DateTimeField(
        label='Data e hora de saída do pedido para entrega',
        widget=forms.DateInput(
            attrs={
                'type': 'datetime-local',
                'class': 'form-control'
            }
        )
    )

    detalhes_pedido = forms.CharField(
        label='Detalhes do pedido',
        required=False,
        widget=forms.Textarea(
            attrs={
                'class': 'form-control',
                'rows': 3,
                'required': False
            }
        )
    )

    filial_pedido = forms.ModelChoiceField(
        label='Filial',
        queryset=Filial.objects.all(),
        widget=forms.Select(
            attrs={
                'class': 'form-control',
                'required': True
            }
        )
    )

    entregador = forms.ModelChoiceField(
        label='Entregador',
        queryset=models.Entregador.objects.all(),
        widget=forms.Select(
            attrs={
                'class': 'form-control',
                'required': True
            }
        )
    )

    class Meta:
        model = models.Entrega
        fields = ['nome_cliente', 'endereco_cliente', 'numero_pedido', 'valor_pedido', 'saida_pedido',
                  'detalhes_pedido', 'entregador', 'filial_pedido']

    def __init__(self, usuario, *args, **kwargs):
        super(EntregaForm, self).__init__(*args, **kwargs)

        self.fields['filial_pedido'].queryset = Filial.objects.filter(id=usuario.filial.id)
        self.fields['filial_pedido'].initial = usuario.filial
        self.fields['entregador'].queryset = models.Entregador.objects.filter(filial=usuario.filial)


class ConsultaEntregaForm(forms.Form):
    data_inicial = forms.DateField(
        label='Data inicial',
        required=True,
        widget=forms.DateInput(
            attrs={
                'class': 'form-control',
                'type': 'date'
            }
        )
    )

    data_final = forms.DateField(
        label='Data final',
        required=True,
        widget=forms.DateInput(
            attrs={
                'class': 'form-control',
                'type': 'date'
            }
        )
    )

    entregador = forms.ModelChoiceField(
        label='Entregador',
        queryset=models.Entregador.objects.all(),
        required=False,
        widget=forms.Select(
            attrs={
                'class': 'form-control',
            }
        )
    )

    pedido = forms.CharField(
        label='Número do pedido',
        required=False,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
            }
        )
    )

    cliente = forms.CharField(
        label='Nome do cliente',
        required=False,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
            }
        )
    )

    status = forms.CharField(
        label='Status do recebimento',
        required=False,
        widget=forms.Select(
            choices=[
                (u'0', 'Todos'),
                (u'1', 'Pendente'),
                (u'2', 'Recebido'),
            ],
            attrs={
                'class': 'form-control',
            }
        )
    )

    def __init__(self, usuario, *args, **kwargs):
        super(ConsultaEntregaForm, self).__init__(*args, **kwargs)

        self.fields['entregador'].queryset = models.Entregador.objects.filter(filial_id=usuario.filial.id)

from django import forms
from apps.core import models


class FilialForm(forms.ModelForm):
    nome = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Nome da filial',
                'required': True
            }
        )
    )
    cidade = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Cidade da filial',
                'required': True
            }
        )
    )

    class Meta:
        model = models.Filial
        fields = ['nome', 'cidade']


class CargoForm(forms.ModelForm):
    nome = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Nome do cargo',
                'required': True
            }
        )
    )

    filial = forms.ModelChoiceField(
        queryset=models.Filial.objects.all(),
        widget=forms.Select(
            attrs={
                'class': 'form-control',
                'required': True
            }
        )
    )

    class Meta:
        model = models.Cargo
        fields = ['nome', 'filial']

    def __init__(self, usuario, *args, **kwargs):
        super(CargoForm, self).__init__(*args, **kwargs)

        if usuario.tipo == '1':
            self.fields['filial'].queryset = models.Filial.objects.filter(id=usuario.filial.id)
            self.fields['filial'].initial = usuario.filial


class FuncionarioForm(forms.ModelForm):
    nome = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Nome do funcionário',
                'required': True
            }
        )
    )
    admissao = forms.DateField(
        label='Admissão',
        widget=forms.DateInput(
            attrs={
                'class': 'form-control',
                'type': 'date',
                'required': True
            }
        )
    )
    cargo = forms.ModelChoiceField(
        queryset=models.Cargo.objects.all(),
        widget=forms.Select(
            attrs={
                'class': 'form-control',
                'required': True
            }
        )
    ) 
    filial = forms.ModelChoiceField(
        queryset=models.Filial.objects.all(),
        widget=forms.Select(
            attrs={
                'class': 'form-control',
                'required': True
            }
        )
    )

    class Meta:
        model = models.Funcionario
        fields = ['nome', 'admissao', 'cargo', 'filial']

    def __init__(self, usuario, *args, **kwargs):
        super(FuncionarioForm, self).__init__(*args, **kwargs)

        if usuario.tipo == '1':
            self.fields['cargo'].queryset = models.Cargo.objects.filter(filial_id=usuario.filial.id)
            self.fields['filial'].queryset = models.Filial.objects.filter(id=usuario.filial.id)
            self.fields['filial'].initial = usuario.filial


class MotivoForm(forms.ModelForm):
    nome = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Nome do motivo',
                'required': True
            }
        )
    )

    filial = forms.ModelChoiceField(
        queryset=models.Filial.objects.all(),
        widget=forms.Select(
            attrs={
                'class': 'form-control',
                'required': True
            }
        )
    )

    class Meta:
        model = models.Motivo
        fields = ['nome', 'filial']

    def __init__(self, usuario, *args, **kwargs):
        super(MotivoForm, self).__init__(*args, **kwargs)

        if usuario.tipo == '1':
            self.fields['filial'].queryset = models.Filial.objects.filter(id=usuario.filial.id)
            self.fields['filial'].initial = usuario.filial


class OcorrenciaForm(forms.ModelForm):
    data = forms.DateField(
        label='Data da ocorrência',
        widget=forms.DateInput(
            attrs={
                'class': 'form-control',
                'type': 'date',
                'required': True
            }
        )
    )
    funcionario = forms.ModelChoiceField(
        label='Funcionário',
        queryset=models.Funcionario.objects.all(),
        widget=forms.Select(
            attrs={
                'class': 'form-control',
                'required': True
            }
        )
    )
    motivo = forms.ModelChoiceField(
        label='Motivo',
        queryset=models.Motivo.objects.all(),
        widget=forms.Select(
            attrs={
                'class': 'form-control',
                'rows': 5,
                'required': True
            }
        )
    )
    observacao = forms.CharField(
        label='Descrição',
        widget=forms.Textarea(
            attrs={
                'class': 'form-control',
                'rows': 5,
                'required': True
            }
        )
    )

    class Meta:
        model = models.Ocorrencia
        fields = ['data', 'motivo', 'funcionario', 'observacao']

    def __init__(self, usuario, *args, **kwargs):
        super(OcorrenciaForm, self).__init__(*args, **kwargs)

        if usuario.tipo == '1':
            self.fields['motivo'].queryset = models.Motivo.objects.filter(filial_id=usuario.filial.id)
            self.fields['funcionario'].queryset = models.Funcionario.objects.filter(filial_id=usuario.filial.id)


class ConsultaOcorrenciaForm(forms.Form):
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

    funcionario = forms.ModelChoiceField(
        label='Funcionário',
        queryset=models.Funcionario.objects.all(),
        required=False,
        widget=forms.Select(
            attrs={
                'class': 'form-control',
            }
        )
    )

    cargo = forms.ModelChoiceField(
        label='Cargo',
        queryset=models.Cargo.objects.all(),
        required=False,
        widget=forms.Select(
            attrs={
                'class': 'form-control',
            }
        )
    )

    motivo = forms.ModelChoiceField(
        label='Motivo',
        queryset=models.Motivo.objects.all(),
        required=False,
        widget=forms.Select(
            attrs={
                'class': 'form-control'
            }
        )
    )

    filial = forms.ModelChoiceField(
        queryset=models.Filial.objects.all(),
        required=False,
        widget=forms.Select(
            attrs={
                'class': 'form-control',
            }
        )
    )

    def __init__(self, usuario, *args, **kwargs):
        super(ConsultaOcorrenciaForm, self).__init__(*args, **kwargs)

        if usuario.tipo == '1':
            self.fields['funcionario'].queryset = models.Funcionario.objects.filter(filial_id=usuario.filial.id)
            self.fields['cargo'].queryset = models.Cargo.objects.filter(filial_id=usuario.filial.id)
            self.fields['motivo'].queryset = models.Motivo.objects.filter(filial_id=usuario.filial.id)

            del self.fields['filial']


class ElogioForm(forms.ModelForm):
    data = forms.DateField(
        label='Data da ocorrência',
        widget=forms.DateInput(
            attrs={
                'class': 'form-control',
                'type': 'date',
                'required': True
            }
        )
    )
    funcionario = forms.ModelChoiceField(
        label='Funcionário',
        queryset=models.Funcionario.objects.all(),
        widget=forms.Select(
            attrs={
                'class': 'form-control',
                'required': True
            }
        )
    )
    observacao = forms.CharField(
        label='Descrição',
        widget=forms.Textarea(
            attrs={
                'class': 'form-control',
                'rows': 5,
                'required': True
            }
        )
    )

    class Meta:
        model = models.Elogio
        fields = ['data', 'funcionario', 'observacao']

    def __init__(self, usuario, *args, **kwargs):
        super(ElogioForm, self).__init__(*args, **kwargs)

        if usuario.tipo == '1':
            self.fields['funcionario'].queryset = models.Funcionario.objects.filter(filial_id=usuario.filial.id)


class ConsultaElogioForm(forms.Form):
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

    funcionario = forms.ModelChoiceField(
        label='Funcionário',
        queryset=models.Funcionario.objects.all(),
        required=False,
        widget=forms.Select(
            attrs={
                'class': 'form-control',
            }
        )
    )

    cargo = forms.ModelChoiceField(
        label='Cargo',
        queryset=models.Cargo.objects.all(),
        required=False,
        widget=forms.Select(
            attrs={
                'class': 'form-control',
            }
        )
    )

    filial = forms.ModelChoiceField(
        queryset=models.Filial.objects.all(),
        required=False,
        widget=forms.Select(
            attrs={
                'class': 'form-control',
            }
        )
    )

    def __init__(self, usuario, *args, **kwargs):
        super(ConsultaElogioForm, self).__init__(*args, **kwargs)

        if usuario.tipo == '1':
            self.fields['funcionario'].queryset = models.Funcionario.objects.filter(filial_id=usuario.filial.id)
            self.fields['cargo'].queryset = models.Cargo.objects.filter(filial_id=usuario.filial.id)

            del self.fields['filial']

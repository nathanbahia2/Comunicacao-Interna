from django import forms
from django.contrib.auth.models import User

from apps.core import models
from apps.usuarios import choices


class LoginForm(forms.Form):
    username = forms.CharField(
        label='Usuário',
        required=True,
        widget=forms.TextInput(
            attrs={
                'required': True,
                'class': 'form-control'
            }
        )
    )

    password = forms.CharField(
        label='Senha',
        required=True,
        widget=forms.PasswordInput(
            attrs={
                'required': True,
                'class': 'form-control'
            }
        )
    )


class UsuarioForm(forms.ModelForm):
    first_name = forms.CharField(
        label='Nome',
        required=True,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control'
            }
        )
    )

    last_name = forms.CharField(
        label='Sobrenome',
        required=True,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control'
            }
        )
    )

    username = forms.CharField(
        label='Usuário de acesso',
        required=True,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control'
            }
        )
    )

    email = forms.EmailField(
        widget=forms.HiddenInput(),
        initial='casadoscereais@email.com'
    )

    filial = forms.ModelChoiceField(
        label='Selecione a filial do usuário',
        queryset=models.Filial.objects.all(),
        widget=forms.Select(
            attrs={
                'class': 'form-control'
            }
        )
    )

    tipo = forms.CharField(
        label='Tipo de usuário',
        required=True,
        widget=forms.Select(
            choices=choices.TIPO_USUARIO,
            attrs={
                'class': 'form-control'
            }
        )
    )

    password = forms.CharField(
        label='Senha',
        required=True,
        widget=forms.PasswordInput(
            attrs={
                'required': True,
                'class': 'form-control'
            }
        )
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'filial', 'tipo', 'password']

    def __init__(self, *args, **kwargs):
        super(UsuarioForm, self).__init__(*args, **kwargs)
        if kwargs.get('instance'):
            del self.fields['password']


class UsuarioEditForm(forms.ModelForm):
    first_name = forms.CharField(
        label='Nome',
        required=True,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control'
            }
        )
    )

    last_name = forms.CharField(
        label='Sobrenome',
        required=True,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control'
            }
        )
    )

    filial = forms.ModelChoiceField(
        label='Selecione a filial do usuário',
        queryset=models.Filial.objects.all(),
        widget=forms.Select(
            attrs={
                'class': 'form-control'
            }
        )
    )

    tipo = forms.CharField(
        label='Tipo de usuário',
        required=True,
        widget=forms.Select(
            choices=choices.TIPO_USUARIO,
            attrs={
                'class': 'form-control'
            }
        )
    )

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'filial', 'tipo']

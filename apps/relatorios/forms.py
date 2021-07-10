from django import forms

from apps.relatorios import choices


class RelatorioForm(forms.Form):
    data_inicial = forms.DateField(
        label='Data inicial',
        widget=forms.DateInput(
            attrs={
                'class': 'form-control',
                'type': 'date'
            }
        )
    )

    data_final = forms.DateField(
        label='Data final',
        widget=forms.DateInput(
            attrs={
                'class': 'form-control',
                'type': 'date'
            }
        )
    )

    tipo = forms.ChoiceField(
        choices=choices.TIPO_RELATORIO,
        widget=forms.Select(
            attrs={
                'class': 'form-control',
            }
        )
    )

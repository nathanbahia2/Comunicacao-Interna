from django.shortcuts import render
from django.contrib.auth.views import login_required
from django.views.decorators.http import require_POST

from apps.core import models
from apps.relatorios import forms


@login_required
def index(request):
    usuario = request.user.perfil.latest('id')

    if usuario.tipo == '1':
        funcionarios_count = models.Funcionario.objects.filter(filial=usuario.filial).count()
        elogios_count = models.Elogio.objects.filter(funcionario__filial=usuario.filial).count()
        ocorrencias_count = models.Ocorrencia.objects.filter(funcionario__filial=usuario.filial).count()
    else:
        funcionarios_count = models.Funcionario.objects.filter(filial=usuario.filial).count()
        elogios_count = models.Elogio.objects.filter(funcionario__filial=usuario.filial).count()
        ocorrencias_count = models.Ocorrencia.objects.filter(funcionario__filial=usuario.filial).count()

    form = forms.RelatorioForm()

    context = {
        'funcionarios_count': funcionarios_count,
        'elogios_count': elogios_count,
        'ocorrencias_count': ocorrencias_count,
        'form': form
    }
    return render(request, 'relatorios/index.html', context)


@login_required
def gerar(request):
    usuario = request.user.perfil.latest('id')
    form = forms.RelatorioForm(data=request.POST)

    data_inicial = None
    data_final = None
    tipo_relatorio = None
    tipo = None
    query = None

    if form.is_valid():
        data_inicial = form.cleaned_data.get('data_inicial')
        data_final = form.cleaned_data.get('data_final')
        tipo_relatorio = form.cleaned_data.get('tipo')

        filtros = {
            'data__range': [data_inicial, data_final],
            'funcionario__filial': usuario.filial
        }

        if tipo_relatorio == '3':
            query = models.Funcionario.objects.filter(filial=usuario.filial)
            tipo = 'Funcionários'

        else:
            if data_inicial and data_final:
                if tipo_relatorio == '1':
                    query = models.Ocorrencia.objects.filter(**filtros)

                elif tipo_relatorio == '2':
                    query = models.Elogio.objects.filter(**filtros)
                    tipo = 'Elogios'

    context = {
        'data_inicial': data_inicial,
        'data_final': data_final,
        'tipo_relatorio': tipo_relatorio,
        'tipo': tipo,
        'query': query
    }

    print(context)

    return render(request, 'relatorios/resultado.html', context)

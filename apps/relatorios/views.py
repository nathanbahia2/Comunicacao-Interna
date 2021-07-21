from django.shortcuts import render
from django.contrib.auth.views import login_required

from apps.core import models, utils
from apps.entregas.models import Entrega
from apps.relatorios import forms


@login_required
def index(request):
    usuario = request.user.perfil

    funcionarios_count = models.Funcionario.objects.filter(filial=usuario.filial, ativo=True).count()
    elogios_count = models.Elogio.objects.filter(funcionario__filial=usuario.filial, ativo=True).count()
    ocorrencias_count = models.Ocorrencia.objects.filter(funcionario__filial=usuario.filial, ativo=True).count()
    entregas_count = Entrega.objects.filter(filial_pedido=usuario.filial, ativo=True).count()

    form = forms.RelatorioForm()

    context = {
        'funcionarios_count': funcionarios_count,
        'elogios_count': elogios_count,
        'ocorrencias_count': ocorrencias_count,
        'entregas_count': entregas_count,
        'form': form
    }
    return render(request, 'relatorios/index.html', context)


@login_required
def gerar(request):
    usuario = request.user.perfil
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
                    tipo = 'Ocorrências'

                elif tipo_relatorio == '2':
                    query = models.Elogio.objects.filter(**filtros)
                    tipo = 'Elogios'

                elif tipo_relatorio == '4':
                    filtros = {
                        'saida_pedido__range': [
                            utils.convert_date_to_datetime(data_inicial),
                            utils.convert_date_to_datetime(data_final, inicio=False)
                        ]
                    }
                    query = Entrega.objects.filter(**filtros)
                    tipo = 'Entregas'

    context = {
        'data_inicial': data_inicial,
        'data_final': data_final,
        'tipo_relatorio': tipo_relatorio,
        'tipo': tipo,
        'query': query
    }

    print(context)

    return render(request, 'relatorios/resultado.html', context)

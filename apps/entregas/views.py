from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt

from apps.core import utils
from apps.entregas import forms, models


@login_required
def entregadores(request, pk=None):
    usuario = request.user.perfil.latest('id')

    instance = None
    msg_sucesso = 'Entregador cadastrado com sucesso'
    msg_erro = 'Falha ao cadastrar entregador'

    if pk:
        instance = models.Entregador.is_active.get(pk=pk)
        msg_sucesso = 'Entregador editado com sucesso'
        msg_erro = 'Falha ao editar entregador'

    form = forms.EntregadorForm(
        usuario=usuario,
        instance=instance
    )

    if request.method == 'POST':
        form = forms.EntregadorForm(
            usuario=usuario,
            instance=instance,
            data=request.POST
        )
        if form.is_valid():
            entregador = form.save(commit=False)
            entregador.usuario = request.user
            entregador.save()

            messages.success(request, msg_sucesso)
            return redirect('entregas:entregadores')

        else:
            messages.error(request, msg_erro)

    query = None
    if not instance:
        query = models.Entregador.is_active.filter(filial=usuario.filial)

    context = {
        'form': form,
        'instance': instance,
        'entregadores': query
    }
    return render(request, 'entregas/entregadores.html', context)


@login_required
def entregas(request, pk=None):
    usuario = request.user.perfil.latest('id')

    instance = None
    msg_sucesso = 'Entrega cadastrado com sucesso'
    msg_erro = 'Falha ao cadastrar entrega'

    if pk:
        instance = models.Entrega.is_active.get(pk=pk)
        msg_sucesso = 'Entrega editado com sucesso'
        msg_erro = 'Falha ao editar entrega'

    form = forms.EntregaForm(
        usuario=usuario,
        instance=instance
    )

    if request.method == 'POST':
        form = forms.EntregaForm(
            usuario=usuario,
            instance=instance,
            data=request.POST
        )

        if form.is_valid():
            entrega = form.save(commit=False)
            entrega.usuario = request.user
            entrega.filial_pedido = usuario.filial
            entrega.save()

            messages.success(request, msg_sucesso)
            return redirect('entregas:entregas')

        else:
            messages.error(request, msg_erro)

    context = {
        'form': form,
        'instance': instance,
    }
    return render(request, 'entregas/entregas.html', context)


@login_required
def consulta_entregas(request):
    usuario = request.user.perfil.latest('id')

    consulta = False

    dias = 30 if request.GET.get('dias') not in ['30', '60', '90', '120'] else request.GET.get('dias')
    data_range = utils.get_data_range(dias)

    filtros = {
        'saida_pedido__range': data_range,
        'filial_pedido': usuario.filial
    }

    query = models.Entrega.is_active.filter(**filtros).order_by('-criacao')

    form = forms.ConsultaEntregaForm(
        usuario=usuario,
        data=request.GET
    )

    if form.is_valid():
        data_inicial = form.cleaned_data.get('data_inicial')
        data_final = form.cleaned_data.get('data_final')
        entregador = form.cleaned_data.get('entregador')
        pedido = form.cleaned_data.get('pedido')
        cliente = form.cleaned_data.get('cliente')

        if data_final and data_inicial:
            dias = None
            filtros['saida_pedido__range'] = [
                utils.convert_date_to_datetime(data_inicial),
                utils.convert_date_to_datetime(data_final, inicio=False)
            ]

        if entregador:
            filtros['entregador'] = entregador

        if pedido:
            filtros['numero_pedido__icontains'] = pedido

        if cliente:
            filtros['nome_cliente__icontains'] = cliente

        consulta = True
        query = models.Entrega.is_active.filter(**filtros)

        print(filtros)

    context = {
        'form': form,
        'dias': dias,
        'consulta': consulta,
        'filtros': filtros,
        'entregas': query
    }
    return render(request, 'entregas/consultas.html', context)


@login_required
def info_entregas(request):
    entrega_id = request.GET.get('entrega')
    entrega = models.Entrega.is_active.get(pk=entrega_id)

    json_entrega = {
        'cliente': entrega.nome_cliente,
        'endereco': entrega.endereco_cliente,
        'entregador': entrega.entregador.nome,
        'pedido': entrega.numero_pedido,
        'valor': entrega.valor_pedido,
        'saida': entrega.saida_pedido.strftime("%d/%m/%Y %H:%M") if entrega.saida_pedido else "",
        'recebimento': entrega.recebimento,
        'cadastro': entrega.cadastro,
        'detalhes': entrega.detalhes_pedido if entrega.detalhes_pedido else "",
        'observacao': entrega.observacao_final if entrega.observacao_final else ""
    }
    return JsonResponse(json_entrega, safe=False)


@login_required
@csrf_exempt
def finaliza_entrega(request):
    entrega_id = request.POST.get('entrega')
    recebimento_pedido = request.POST.get('recebimento_pedido')
    observacao_final = request.POST.get('observacao_final')

    entrega = models.Entrega.is_active.get(pk=entrega_id)

    entrega.recebimento_pedido = recebimento_pedido
    entrega.observacao_final = observacao_final
    entrega.usuario_recebimento = request.user
    entrega.save()

    return JsonResponse(True, safe=False)

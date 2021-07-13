from datetime import datetime

from django.contrib import messages
from django.shortcuts import render, redirect

from apps.entregas import forms, models


def entregadores(request, pk=None):
    usuario = request.user.perfil.latest('id')

    instance = None
    msg_sucesso = 'Entregador cadastrado com sucesso'
    msg_erro = 'Falha ao cadastrar entregador'

    if pk:
        instance = models.Entregador.objects.get(pk=pk)
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
        query = models.Entregador.objects.filter(filial=usuario.filial)

    context = {
        'form': form,
        'instance': instance,
        'entregadores': query
    }
    return render(request, 'entregas/entregadores.html', context)


def entregas(request, pk=None):
    usuario = request.user.perfil.latest('id')

    instance = None
    msg_sucesso = 'Entrega cadastrado com sucesso'
    msg_erro = 'Falha ao cadastrar entrega'

    if pk:
        instance = models.Entregador.objects.get(pk=pk)
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

    query = None
    if not instance:
        query = models.Entrega.objects.all()

    context = {
        'form': form,
        'instance': instance,
        'entregas': query
    }
    return render(request, 'entregas/entregas.html', context)

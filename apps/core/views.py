from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.http.response import JsonResponse
from django.contrib import messages
from django.core import serializers

from apps.core import forms, utils
from apps.core import models


@login_required
def index(request):
    return render(request, 'core/index/index.html')


@login_required
def cargos(request, pk=None):
    usuario = request.user.perfil.latest('id')

    instance = None
    msg_sucesso = 'Cargo cadastrado com sucesso'
    msg_erro = 'Falha ao cadastrar cargo'

    if pk:
        instance = models.Cargo.objects.get(pk=pk)
        msg_sucesso = 'Cargo editado com sucesso'
        msg_erro = 'Falha ao editar cargo'

    form = forms.CargoForm(
        usuario=usuario,
        instance=instance
    )

    if request.method == 'POST':
        form = forms.CargoForm(
            usuario=usuario,
            data=request.POST,
            instance=instance
        )

        if form.is_valid():
            instance = form.save(commit=False)
            instance.usuario = request.user
            instance.save()

            messages.success(request, msg_sucesso)
            return redirect('core:cargos')

        else:
            messages.success(request, msg_erro)

    query = None
    if not instance:
        query = models.Cargo.objects.filter(filial=usuario.filial)

    context = {
        'form': form,
        'instance': instance,
        'cargos': query
    }
    return render(request, 'core/funcionarios/cargos.html', context)


@login_required
def filiais(request):
    usuario = request.user.perfil.latest('id')
    if not usuario.tipo == '2':
        return redirect('core:index')

    form = forms.FilialForm()

    if request.method == 'POST':
        form = forms.FilialForm(data=request.POST)
        instance = form.save(commit=False)
        instance.usuario = request.user
        instance.save()

        messages.success(request, 'Filial cadastrada com sucesso')
        return redirect('core:filiais')

    context = {
        'form': form,
        'filiais': models.Filial.objects.order_by('nome'),
    }
    return render(request, 'core/filiais/filiais.html', context)   


@login_required
def funcionarios(request, pk=None):
    usuario = request.user.perfil.latest('id')

    instance = None
    msg_sucesso = 'Funcionário cadastrado com sucesso'
    msg_erro = 'Falha ao cadastrar funcionário'

    if pk:
        instance = models.Funcionario.objects.get(pk=pk)
        msg_sucesso = 'Funcionário editado com sucesso'
        msg_erro = 'Falha ao editar funcionário'

    form = forms.FuncionarioForm(
        usuario=usuario,
        instance=instance
    )

    if request.method == 'POST':
        form = forms.FuncionarioForm(
            usuario=usuario,
            data=request.POST,
            instance=instance
        )

        if form.is_valid():
            obj = form.save(commit=False)
            obj.usuario = request.user
            obj.save()

            messages.success(request, msg_sucesso)
            return redirect('core:funcionarios')

        else:
            messages.error(request, msg_erro)

            print(form.errors)

    query = None
    if not instance:
        query = models.Funcionario.objects.filter(filial=usuario.filial)

    context = {
        'form': form,
        'instance': instance,
        'funcionarios': query,
    }
    return render(request, 'core/funcionarios/funcionarios.html', context)


@login_required
def motivos(request, pk=None):
    usuario = request.user.perfil.latest('id')

    instance = None
    msg_sucesso = 'Motivo cadastrado com sucesso'
    msg_erro = 'Falha ao cadastrar motivo'

    if pk:
        instance = models.Motivo.objects.get(pk=pk)
        msg_sucesso = 'Motivo editado com sucesso'
        msg_erro = 'Falha ao editar motivo'

    form = forms.MotivoForm(
        usuario=usuario,
        instance=instance
    )

    if request.method == 'POST':
        form = forms.MotivoForm(
            filial=usuario.filial,
            usuario=usuario,
            data=request.POST,
            instance=instance
        )
        if form.is_valid():
            instance = form.save(commit=False)
            instance.usuario = request.user
            instance.save()

            messages.success(request, msg_sucesso)
            return redirect('core:motivos')

        else:
            messages.error(request, msg_erro)

    query = None
    if not instance:
        query = models.Motivo.objects.filter(filial=usuario.filial)

    context = {
        'form': form,
        'instance': instance,
        'query': query,
        'motivos': query
    }
    return render(request, 'core/ocorrencias/motivos.html', context)


@login_required
def ocorrencias(request, pk=None):
    usuario = request.user.perfil.latest('id')

    instance = None
    msg_sucesso = 'Ocorrência cadastrada com sucesso'
    msg_erro = 'Falha ao cadastrar ocorrência'

    if pk:
        instance = models.Ocorrencia.objects.get(pk=pk)
        msg_sucesso = 'Ocorrência editada com sucesso'
        msg_erro = 'Falha ao editar ocorrência'

    form = forms.OcorrenciaForm(
        usuario=usuario,
        instance=instance
    )

    if request.method == 'POST':
        form = forms.OcorrenciaForm(
            usuario=usuario,
            data=request.POST,
            instance=instance
        )

        if form.is_valid():
            obj = form.save(commit=False)
            obj.usuario = request.user
            obj.save()

            messages.success(request, msg_sucesso)

            if not instance:
                return redirect('core:ocorrencias')

            else:
                return redirect('core:edit_ocorrencias', pk)

        else:
            messages.error(request, msg_erro)

    query = None
    if not instance:
        query = models.Ocorrencia.objects.filter(funcionario__filial=usuario.filial)

    context = {
        'form': form,
        'instance': instance,
        'ocorrencias': query
    }
    return render(request, 'core/ocorrencias/ocorrencias.html', context)


@login_required
def consulta_ocorrencias(request):
    usuario = request.user.perfil.latest('id')

    consulta = False

    dias = 30 if request.GET.get('dias') not in ['30', '60', '90', '120'] else request.GET.get('dias')
    data_range = utils.get_data_range(dias)

    filtros = {
        'data__range': data_range,
        'funcionario__filial': usuario.filial
    }

    query = models.Ocorrencia.objects.filter(**filtros).order_by('funcionario')

    form = forms.ConsultaOcorrenciaForm(
        usuario=usuario,
        data=request.GET
    )

    if form.is_valid():
        data_inicial = form.cleaned_data.get('data_inicial')
        data_final = form.cleaned_data.get('data_final')
        funcionario = form.cleaned_data.get('funcionario')
        cargo = form.cleaned_data.get('cargo')
        motivo = form.cleaned_data.get('motivo')

        if data_final and data_inicial:
            dias = None
            filtros['data__range'] = [data_inicial, data_final]

        if funcionario:
            filtros['funcionario'] = funcionario

        if cargo:
            filtros['funcionario__cargo'] = cargo

        if motivo:
            filtros['motivo'] = motivo

        consulta = True
        query = models.Ocorrencia.objects.filter(**filtros)

    context = {
        'form': form,
        'dias': dias,
        'consulta': consulta,
        'filtros': filtros,
        'ocorrencias': query
    }
    return render(request, 'core/ocorrencias/consultas.html', context)


@login_required
def info_ocorrencias(request):
    ocorrencia_id = request.GET.get('ocorrencia')
    ocorrencia = models.Ocorrencia.objects.get(pk=ocorrencia_id)

    json_ocorrencia = {
        'criacao': ocorrencia.criacao.isoformat(),
        'usuario': ocorrencia.get_usuario_display,
        'funcionario': ocorrencia.funcionario.nome,
        'cargo': ocorrencia.funcionario.cargo.nome,
        'data': ocorrencia.data.strftime("%d/%m/%Y"),
        'motivo': ocorrencia.get_motivo_display,
        'observacao': ocorrencia.observacao
    }
    return JsonResponse(json_ocorrencia, safe=False)


@login_required
def elogios(request, pk=None):
    usuario = request.user.perfil.latest('id')

    instance = None
    msg_sucesso = 'Elogio cadastrado com sucesso'
    msg_erro = 'Falha ao cadastrar elogio'

    if pk:
        instance = models.Elogio.objects.get(pk=pk)
        msg_sucesso = 'Elogio editado com sucesso'
        msg_erro = 'Falha ao editar elogio'

    form = forms.ElogioForm(
        usuario=usuario,
        instance=instance
    )

    if request.method == 'POST':
        form = forms.ElogioForm(
            usuario=usuario,
            data=request.POST,
            instance=instance
        )

        if form.is_valid():
            obj = form.save(commit=False)
            obj.usuario = request.user
            obj.save()

            messages.success(request, msg_sucesso)

            if not instance:
                return redirect('core:elogios')

            else:
                return redirect('core:edit_elogios', pk)

        else:
            messages.error(request, msg_erro)

    query = None
    if not instance:
        query = models.Elogio.objects.filter(funcionario__filial=usuario.filial)

    context = {
        'form': form,
        'instance': instance,
        'ocorrencias': query,
    }
    return render(request, 'core/elogios/elogios.html', context)


@login_required
def consulta_elogios(request):
    usuario = request.user.perfil.latest('id')

    consulta = False

    dias = 30 if request.GET.get('dias') not in ['30', '60', '90', '120'] else request.GET.get('dias')
    data_range = utils.get_data_range(dias)

    filtros = {
        'data__range': data_range,
        'funcionario__filial': usuario.filial
    }

    query = models.Elogio.objects.filter(**filtros).order_by('funcionario')

    form = forms.ConsultaElogioForm(
        usuario=usuario,
        data=request.GET
    )

    if form.is_valid():
        data_inicial = form.cleaned_data.get('data_inicial')
        data_final = form.cleaned_data.get('data_final')
        funcionario = form.cleaned_data.get('funcionario')
        cargo = form.cleaned_data.get('cargo')
        filial = form.cleaned_data.get('filial')

        if data_final and data_inicial:
            dias = None
            filtros['data__range'] = [data_inicial, data_final]

        if funcionario:
            filtros['funcionario'] = funcionario

        if filial:
            filtros['funcionario__filial'] = filial

        if cargo:
            filtros['funcionario__cargo'] = cargo

        consulta = True
        query = models.Elogio.objects.filter(**filtros)

    context = {
        'form': form,
        'elogios': query,
        'consulta': consulta,
        'dias': dias,
        'filtros': filtros
    }
    return render(request, 'core/elogios/consultas.html', context)


@login_required
def info_elogios(request):
    elogio_id = request.GET.get('elogio')
    elogio = models.Elogio.objects.get(pk=elogio_id)
    json_elogio = {
        'criacao': elogio.criacao.isoformat(),
        'usuario': elogio.usuario.get_full_name(),
        'funcionario': elogio.funcionario.nome,
        'cargo': elogio.funcionario.cargo.nome,
        'data': elogio.data.strftime("%d/%m/%Y"),
        'observacao': elogio.observacao
    }
    return JsonResponse(json_elogio, safe=False)


@login_required
@require_POST
@csrf_exempt
def delete_model_object(request):
    response = False
    msg_sucesso = request.POST.get('msg_sucesso')
    msg_erro = request.POST.get('msg_erro')

    try:
        obj_id = request.POST.get('data')
        model_name = request.POST.get('model')

        model = {
            'elogios': models.Elogio,
            'ocorrencias': models.Ocorrencia,
            'funcionarios': models.Funcionario,
            'cargos': models.Cargo,
            'motivos': models.Motivo,
            'usuarios': User
        }[model_name]

        obj = model.objects.get(pk=obj_id)
        obj.delete()

        response = True

        messages.success(
            request,
            msg_sucesso
        )

    except Exception as e:
        messages.error(
            request,
            f'{msg_erro}: {e}')

    return JsonResponse(response, safe=False)


@login_required
def altera_filial(request):
    filial_id = request.POST.get('filial')
    path = request.POST.get('path')

    usuario = request.user.perfil.latest('id')
    usuario.filial_id = filial_id
    usuario.save()

    return redirect(path)

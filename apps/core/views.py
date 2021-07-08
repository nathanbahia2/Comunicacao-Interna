from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http.response import JsonResponse
from django.contrib import messages
from django.core import serializers

from apps.core import forms, utils
from apps.core import models


@login_required
def index(request):
    return render(request, 'core/index/index.html')


@login_required
def cargos(request):
    usuario = request.user.perfil_set.last()
    if not usuario.tipo == '2':
        return redirect('core:index')

    form = forms.CargoForm(filial=usuario.filial)

    if request.method == 'POST':
        form = forms.CargoForm(filial=usuario.filial, data=request.POST)
        instance = form.save(commit=False)
        instance.usuario = request.user
        instance.save()

        messages.success(request, 'Cargo cadastrado com sucesso')
        return redirect('core:cargos')

    context = {
        'form': form,
        'cargos': models.Cargo.objects.filter(filial=usuario.filial).order_by('nome'),
    }
    return render(request, 'core/funcionarios/cargos.html', context)


@login_required
def filiais(request):
    usuario = request.user.perfil_set.last()
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
def funcionarios(request):
    usuario = request.user.perfil_set.last()
    form = forms.FuncionarioForm(filial=usuario.filial)

    if request.method == 'POST':
        form = forms.FuncionarioForm(filial=usuario.filial, data=request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.usuario = request.user
            instance.save()

            messages.success(request, 'Funcionário cadastrado com sucesso')
            return redirect('core:funcionarios')

        else:
            messages.error(request, 'Falha ao cadastrar funcionário')

            print(form.errors)

    context = {
        'form': form,
        'funcionarios': models.Funcionario.objects.filter(filial=usuario.filial).order_by('nome'),
    }
    return render(request, 'core/funcionarios/funcionarios.html', context)  


@login_required
def motivos(request):
    usuario = request.user.perfil_set.last()
    if not usuario.tipo == '2':
        return redirect('core:index')

    form = forms.MotivoForm(filial=usuario.filial)

    if request.method == 'POST':
        form = forms.MotivoForm(filial=usuario.filial, data=request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.usuario = request.user
            instance.save()

            messages.success(request, 'Motivo cadastrado com sucesso')
            return redirect('core:motivos')
        else:
            messages.error(request, 'Falha ao cadastrar motivo')

    context = {
        'form': form,
        'motivos': models.Motivo.objects.filter(filial=usuario.filial).order_by('nome'),
    }
    return render(request, 'core/ocorrencias/motivos.html', context)


@login_required
def ocorrencias(request):
    usuario = request.user.perfil_set.last()
    form = forms.OcorrenciaForm(filial=usuario.filial)

    if request.method == 'POST':
        form = forms.OcorrenciaForm(filial=usuario.filial, data=request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.usuario = request.user
            instance.save()
            messages.success(request, 'Ocorrência cadastrada com sucesso')

            return redirect('core:ocorrencias')

    context = {
        'form': form,
        'ocorrencias': models.Ocorrencia.objects.filter(funcionario__filial=usuario.filial).order_by('funcionario'),
    }
    return render(request, 'core/ocorrencias/ocorrencias.html', context)


@login_required
def consulta_ocorrencias(request):
    usuario = request.user.perfil_set.last()

    dias = request.GET.get('dias', 30)
    data_range = utils.get_data_range(dias)

    filtros = {
        'funcionario__filial': usuario.filial,
        'data__range': data_range,
        'ativo': True
    }

    form = forms.ConsultaOcorrenciaForm(
        filial=usuario.filial,
        data=request.GET
    )

    query = models.Ocorrencia.objects.filter(**filtros).order_by('funcionario')

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
            filtros['cargo'] = cargo

        if motivo:
            filtros['motivo'] = motivo

        query = models.Ocorrencia.objects.filter(**filtros)

    context = {
        'form': form,
        'dias': dias,
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
        'usuario': ocorrencia.usuario.get_full_name(),
        'funcionario': ocorrencia.funcionario.nome,
        'cargo': ocorrencia.funcionario.cargo.nome,
        'data': ocorrencia.data.strftime("%d/%m/%Y"),
        'motivo': ocorrencia.motivo.nome,
        'observacao': ocorrencia.observacao
    }
    return JsonResponse(json_ocorrencia, safe=False)


@login_required
@csrf_exempt
def delete_ocorrencias(request):
    ocorrencia_id = request.POST.get('ocorrencia')
    ocorrencia = models.Ocorrencia.objects.get(pk=ocorrencia_id)
    ocorrencia.delete()
    return JsonResponse(True, safe=False)


@login_required
def elogios(request):
    usuario = request.user.perfil_set.last()
    form = forms.ElogioForm(filial=usuario.filial)

    if request.method == 'POST':
        form = forms.ElogioForm(filial=usuario.filial, data=request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.usuario = request.user
            instance.save()

            messages.success(request, 'Elogio cadastrado com sucesso')
            return redirect('core:ocorrencias')

        else:
            messages.error(request, 'Falha ao cadastrar elogios')

    context = {
        'form': form,
        'ocorrencias': models.Elogio.objects.filter(funcionario__filial=usuario.filial).order_by('funcionario'),
    }
    return render(request, 'core/elogios/elogios.html', context)


@login_required
def consulta_elogios(request):
    usuario = request.user.perfil_set.last()

    form = forms.ConsultaElogioForm(
        filial=usuario.filial,
        data=request.GET
    )

    dias = request.GET.get('dias', 30)
    data_range = utils.get_data_range(dias)

    filtros = {
        'funcionario__filial': usuario.filial,
        'data__range': data_range,
        'ativo': True
    }

    query = models.Elogio.objects.filter(**filtros).order_by('funcionario')

    if form.is_valid():
        data_inicial = form.cleaned_data.get('data_inicial')
        data_final = form.cleaned_data.get('data_final')
        funcionario = form.cleaned_data.get('funcionario')
        cargo = form.cleaned_data.get('cargo')

        filtros = {'funcionario__filial': usuario.filial}

        if data_final and data_inicial:
            dias = None
            filtros['data__range'] = [data_final, data_inicial]

        if funcionario:
            filtros['funcionario'] = funcionario

        if cargo:
            filtros['funcionario__cargo'] = cargo

        query = models.Elogio.objects.filter(**filtros)

    context = {
        'form': form,
        'elogios': query,
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
@csrf_exempt
def delete_elogios(request):
    elogio_id = request.POST.get('elogio')
    elogio = models.Elogio.objects.get(pk=elogio_id)
    elogio.delete()
    return JsonResponse(True, safe=False)

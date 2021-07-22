from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.http.response import JsonResponse
from django.contrib import messages

from apps.usuarios import forms, models


def login(request):
    form = forms.LoginForm()
    context = {
        'form': form
    }
    return render(request, 'registration/login.html', context)


@login_required
def usuarios(request, pk=None):
    usuario = request.user.perfil.latest('id')

    if not usuario.tipo == '2':
        return redirect('core:site')

    instance = None
    perfil = None
    msg_sucesso = 'Usuário cadastrado com sucesso'
    msg_erro = 'Falha ao cadastrar usuário'

    if pk:
        instance = User.objects.get(pk=pk)
        perfil = instance.perfil.latest('id')
        msg_sucesso = 'Usuário editado com sucesso'
        msg_erro = 'Falha ao editar usuário'

    form = forms.UsuarioForm()

    if instance:
        form = forms.UsuarioEditForm(
            instance=instance,
            initial={
                'filial': perfil.filial,
                'tipo': perfil.tipo,
            }
        )

    if request.method == 'POST':
        if instance:
            form = forms.UsuarioEditForm(
                instance=instance,
                data=request.POST
            )
        else:
            form = forms.UsuarioForm(
                data=request.POST
            )

        if form.is_valid():
            if instance:
                form.save()
                perfil.filial = form.cleaned_data.get('filial')
                perfil.tipo = form.cleaned_data.get('tipo')
                perfil.save()
                messages.success(request, msg_sucesso)

            else:
                obj = form.save(commit=False)
                obj.set_password(form.cleaned_data.get('password'))
                obj.save()
                models.Perfil.objects.create(
                    usuario=obj,
                    filial=form.cleaned_data.get('filial'),
                    tipo=form.cleaned_data.get('tipo')
                )
                messages.success(request, msg_sucesso)

                return redirect('usuarios:usuarios')

        else:
            messages.error(request, msg_erro)

    query = None
    if not instance:
        query = models.Perfil.objects.filter(
            filial=usuario.filial,
            ativo=True,
            tipo='1'
        )

    context = {
        'form': form,
        'instance': instance,
        'usuarios': query
    }
    return render(request, 'registration/cadastro.html', context)


@login_required
@csrf_exempt
def change_password(request):
    try:
        usuario_id = request.POST.get('usuario')
        usuario = User.objects.get(pk=usuario_id)
        password = request.POST.get('password')

        usuario.set_password(password)
        usuario.save()

        response = True

    except Exception as e:
        print(e)
        response = False

    return JsonResponse(response, safe=False)

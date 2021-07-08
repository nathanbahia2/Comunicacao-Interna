from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from apps.usuarios import forms, models


def login(request):
    form = forms.LoginForm()
    context = {
        'form': form
    }
    return render(request, 'registration/login.html', context)


@login_required
def cadastro_usuarios(request):
    form = forms.UsuarioForm()
    if request.method == 'POST':
        form = forms.UsuarioForm(data=request.POST)
        if form.is_valid():
            usuario = form.save(commit=False)
            usuario.set_password(form.cleaned_data.get('password'))
            usuario.save()
            if usuario:
                models.Perfil.objects.create(
                    usuario=usuario,
                    filial=form.cleaned_data.get('filial'),
                    tipo=form.cleaned_data.get('tipo')
                )
            messages.success(request, 'Usuário cadastrado com sucesso')
            return redirect('usuarios:cadastro_usuarios')
        else:
            messages.error(request, 'Falha ao cadastrar usuário')

            print(form.errors)

    context = {
        'form': form,
        'usuarios': models.Perfil.objects.order_by('usuario__first_name')
    }
    return render(request, 'registration/cadastro.html', context)

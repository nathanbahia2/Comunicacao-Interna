from apps.core import models


def usuario(request):
    if not request.user.is_authenticated:
        return {}

    perfil = request.user.perfil.latest('id')
    context = {'usuario': {}}

    if perfil:
        context['usuario']['filial'] = perfil.filial
        context['usuario']['filiais'] = models.Filial.objects.all()

        if perfil.tipo == '2':
            context['usuario']['administrador'] = True

    return context


from apps.core import models


def usuario(request):
    if not request.user.is_authenticated:
        return {}

    context = {'usuario': {}}
    perfil = request.user.perfil.order_by('id').last()

    if perfil:
        context['usuario']['filial'] = perfil.filial
        context['usuario']['filiais'] = models.Filial.objects.all()

        if perfil.tipo == '2':
            context['usuario']['administrador'] = True

    return context


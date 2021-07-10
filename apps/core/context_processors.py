def usuario(request):
    if not request.user.is_authenticated:
        return {}

    perfil = request.user.perfil.latest('id')
    context = {'usuario': {}}

    if perfil:
        context['usuario']['filial'] = perfil.filial
        if perfil.tipo == '2':
            context['usuario']['administrador'] = True

    return context

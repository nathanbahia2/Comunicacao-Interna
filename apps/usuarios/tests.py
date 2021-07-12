from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse

from apps.usuarios import forms, models
from apps.core.models import Filial


class UsuariosTest(TestCase):
    def setUp(self):
        usuario = User.objects.create(
            username='Nathan Bahia',
            email='nathan@mail.com'
        )
        filial = Filial.objects.create(
            nome='Filial A',
            cidade='Cidade A'
        )
        models.Perfil.objects.create(
            usuario=usuario,
            filial=filial
        )

    def test_formulario_cadastro_usuario(self):
        form = forms.UsuarioForm()
        self.assertIn('password', form.fields)

        usuario = User.objects.latest('id')
        form = forms.UsuarioForm(instance=usuario)
        self.assertNotIn('password', form.fields)

    def test_str_perfil(self):
        perfil = models.Perfil.objects.latest('id')
        self.assertEqual(perfil.usuario.first_name, str(perfil))

    def test_response_login_view(self):
        response = self.client.get(reverse('usuarios:login'))
        self.assertEqual(200, response.status_code)

        self.assertTemplateUsed(response, 'registration/login.html')
        self.assertIn('form', response.context)

from django.test import TestCase
from django.urls import reverse


class EntregadoresTestCase(TestCase):
    def test_response_entregadores_view(self):
        response = self.client.get(reverse('entregas:entregadores'))
        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed(response, 'entregas/entregadores.html')


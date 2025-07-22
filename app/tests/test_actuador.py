# tests.py
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from .models import Actuador, ControlWebActuador

class ActuadorAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = '/api/actuadores/'
        self.actuador_data = {
            "nombre": "Motor A",  # usa los campos reales de tu modelo
            "tipo": "Motor",      # cambia según tu modelo
            "descripcion": "Actuador de prueba"
        }

    def test_get_actuadores(self):
        # Crear un actuador antes
        Actuador.objects.create(**self.actuador_data)

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.data) >= 1)  # o verifica contenido específico

    def test_post_actuador(self):
        response = self.client.post(self.url, self.actuador_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('actuador', response.data)
        self.assertIn('control_web_actuador', response.data)

        # Verifica que se hayan creado en la base de datos
        self.assertEqual(Actuador.objects.count(), 1)
        self.assertEqual(ControlWebActuador.objects.count(), 1)

"""Regression checks for a fresh presentation setup and real login tokens."""
from io import StringIO
from unittest.mock import patch
from django.test import TestCase, override_settings
from django.core.management import call_command
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from knox.models import AuthToken
from field.models import FieldData, FieldLog
from field.utils import fetchEEData
from finance.models import CostEntry


@override_settings(DEMO_MODE=True, DEBUG=True)
class PresentationTests(TestCase):
    def setUp(self):
        call_command('seed_demo', stdout=StringIO())
        self.client = APIClient()

    def login(self):
        response = self.client.post('/api/v1/auth/login', {
            'username': 'demo_farmer', 'password': 'DemoFarmer@2026'}, format='json')
        self.assertEqual(response.status_code, 200)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + response.data['token'])
        return response.data['token']

    def test_login_access_and_logout_revocation(self):
        token = self.login()
        self.assertEqual(self.client.get('/api/v1/auth/test-token').status_code, 200)
        response = self.client.get('/field/data')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(self.client.post('/api/v1/auth/logout').status_code, 200)
        self.assertEqual(self.client.get('/field/data').status_code, 401)

    def test_expired_knox_token_rejected(self):
        from django.utils import timezone
        from datetime import timedelta
        self.login()
        AuthToken.objects.update(expiry=timezone.now()-timedelta(seconds=1))
        self.assertEqual(self.client.get('/field/data').status_code, 401)

    def test_seed_is_idempotent(self):
        before = (FieldData.objects.count(), FieldLog.objects.count(), CostEntry.objects.count())
        call_command('seed_demo', stdout=StringIO())
        self.assertEqual(before, (FieldData.objects.count(), FieldLog.objects.count(), CostEntry.objects.count()))

    def test_demo_uses_no_external_weather_or_ai(self):
        self.login()
        with patch('field.views.weather.requests.get', side_effect=AssertionError('network')), patch('chat.views.genai.GenerativeModel', side_effect=AssertionError('AI network')):
            self.assertEqual(self.client.get('/field/weather?lat=30.9&lon=75.85').data['source'], 'demo')
            reply = self.client.post('/api/chat', {'question': 'How to irrigate?'}, format='json')
            self.assertEqual(reply.status_code, 200)
            self.assertEqual(reply.data['source'], 'demo')

    def test_satellite_internal_field_instance_and_user_isolation(self):
        field = FieldData.objects.first()
        self.assertEqual(fetchEEData(field_instance=field)['source'], 'demo')
        other = User.objects.create_user(username='another', password='SomethingSecure!26')
        self.assertIn('error', fetchEEData(user=other, field_instance=field))
        from django.http import Http404
        with self.assertRaises(Http404):
            fetchEEData(user=other, field_id=field.pk)

    def test_live_mode_does_not_return_demo_weather(self):
        self.login()
        with override_settings(DEMO_MODE=False), patch.dict('os.environ', {'OPENWEATHER_API_KEY': ''}):
            self.assertEqual(self.client.get('/field/weather?lat=30.9&lon=75.85').status_code, 503)

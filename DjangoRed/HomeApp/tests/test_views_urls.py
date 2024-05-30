from django.test import TestCase, Client
from django.urls import reverse

class HomeAppTestCase(TestCase):
    def setUp(self):
        self.client = Client()

    def test_home_view_with_test_ids_in_session(self):
        response = self.client.get(reverse('HomeApp:home'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')


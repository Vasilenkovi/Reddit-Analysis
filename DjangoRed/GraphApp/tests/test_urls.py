from django.test import SimpleTestCase
from django.urls import reverse, resolve
from GraphApp.views import base_graph_view

class TestGraphAppUrls(SimpleTestCase):

    def test_base_graph_url_resolves(self):
        url = reverse('GraphApp:base_graph')
        self.assertEqual(resolve(url).func, base_graph_view)

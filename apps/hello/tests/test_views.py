from django.test import TestCase
from django.core.urlresolvers import reverse


class HelloAppTestCase(TestCase):
    fixtures = ['initial_data.json']

    def test_default_view(self):
        url = reverse('default')
        response = self.client.get(url)
        self.assertRedirects(response, reverse('index'), status_code=301, target_status_code=200)

    def test_index_view(self):
        url = reverse('index')
        response = self.client.get(url)
        self.assertTrue('person' in response.context)
        self.assertTrue(response.context['person'].user.first_name == 'Serhij')
        self.assertIn('<h1>42 Coffee Cups Test Assignment</h1>', response.content)


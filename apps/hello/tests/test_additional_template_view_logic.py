from django.test import TestCase
from django.core.urlresolvers import reverse


class HelloAppTestCase(TestCase):
    def test_context_processor(self):
        url = reverse('index')
        response = self.client.get(url)
        self.assertIn('settings', response.context)
        url = reverse('requests')
        response = self.client.get(url)
        self.assertIn('settings', response.context)


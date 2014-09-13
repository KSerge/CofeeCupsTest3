from django.test import TestCase
from django.core.urlresolvers import reverse
from ..models import IncomingRequest


class HelloAppTestCase(TestCase):
    def test_request_is_stored_to_db(self):
        url = reverse('index')
        response = self.client.get(url)
        url = reverse('requests')
        response = self.client.get(url)
        requests = IncomingRequest.objects.filter(path=reverse('index'))
        self.assertTrue(requests.count() == 1)
        requests = IncomingRequest.objects.filter(path=reverse('requests'))
        self.assertTrue(requests.count() == 1)

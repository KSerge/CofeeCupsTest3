from django.test import TestCase
from django.core.urlresolvers import reverse
from ..models import Person, IncomingRequest, ModelObjectsTracker
from ..models import CREATE_ACTION_NAME, EDIT_ACTION_NAME, DELETE_ACTION_NAME


class RequestsTrackingTestCase(TestCase):
    def test_request_is_stored_to_db(self):
        url = reverse('index')
        response = self.client.get(url)
        url = reverse('requests')
        response = self.client.get(url)
        requests = IncomingRequest.objects.filter(path=reverse('index'))
        self.assertTrue(requests.count() == 1)
        requests = IncomingRequest.objects.filter(path=reverse('requests'))
        self.assertTrue(requests.count() == 1)


class SignalProcessingTestCase(TestCase):
    def test_insert_model_signal(self):
        tracking_objects = ModelObjectsTracker.objects.filter(
            model_name=Person.__name__,
            type_of_event=CREATE_ACTION_NAME)
        self.assertEqual(tracking_objects.count(), 1)

    def test_edit_model_signal(self):
        person = Person.objects.get(pk=1)
        person.skype = 'Skype Account'
        person.save()
        self.assertEqual(Person.objects.all().count(), 1)
        tracking_objects = ModelObjectsTracker.objects.filter(
            model_name=Person.__name__,
            type_of_event=EDIT_ACTION_NAME)

    def test_delete_model_signal(self):
        person = Person.objects.get(pk=1)
        person.delete()
        tracking_objects = ModelObjectsTracker.objects.filter(
            model_name=Person.__name__,
            type_of_event=DELETE_ACTION_NAME)
        self.assertEqual(tracking_objects.count(), 1)

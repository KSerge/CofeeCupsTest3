from django.test import TestCase
from django.core.urlresolvers import reverse
from ..models import IncomingRequest, Person
from django.conf import settings
import os
from ..views import SAVE_FORM_ERRORS_MESSAGE, INVALID_LOGIN_MESSAGE

TEST_SKYPE_NAME = 'New Skype Name'
TEST_USERNAME = 'Username'
TEST_PASSWORD = 'password'


class HelloAppTestCase(TestCase):
    fixtures = ['initial_data.json']

    def test_default_view(self):
        url = reverse('default')
        response = self.client.get(url)
        self.assertRedirects(response,
                             reverse('index'),
                             status_code=301,
                             target_status_code=200)

    def test_index_view(self):
        url = reverse('index')
        response = self.client.get(url)
        self.assertTrue('person' in response.context)
        self.assertTrue(response.context['person'].user.first_name == 'Serhij')
        self.assertIn('<h1>42 Coffee Cups Test Assignment</h1>', response.content)
        self.assertIn('Serhij', response.content)
        self.assertIn('Krasovskyy', response.content)

    def test_index_view(self):
        person = Person.objects.get(pk=1)
        person.delete()
        url = reverse('index')
        response = self.client.get(url)
        self.assertIn('There is no Person data in system yet', response.content)

    def test_view_request_view(self):
        url = reverse('index')
        for x in range(0, 15):
            response = self.client.get(url)
        url = reverse('requests')
        response = self.client.get(url)
        self.assertIn('requests', response.context)
        self.assertTrue(IncomingRequest.objects.all().count() > 10)
        self.assertTrue(response.context['requests'].count() == 10)
        self.assertIn('<h4>Requests:</h4>', response.content)

    def test_edit_view_valid_data(self):
        file_path = os.path.join(settings.BASE_DIR, 'apps', 'hello', 'tests', 'test_image.png')
        f = open(file_path, 'r')
        post_data = {'profile_image': f, 'skype': TEST_SKYPE_NAME}
        url = reverse('edit')
        response = self.client.post(url, post_data)
        self.assertRedirects(response,
                             reverse('index'),
                             status_code=302,
                             target_status_code=200,
                             )
        self.assertTrue(Person.objects.get(pk=1).skype == TEST_SKYPE_NAME)
        f.close()
        uploaded_file_path = os.path.join(settings.BASE_DIR,
                                          'uploads',
                                          'profile',
                                          'test_image.png')
        self.assertTrue(os.path.isfile(uploaded_file_path))
        os.remove(uploaded_file_path)

    def test_edit_view_not_valid_data(self):
        url = reverse('edit')
        response = self.client.post(url, {'date_of_birth': True})
        self.assertIn(SAVE_FORM_ERRORS_MESSAGE, response.content)

    def test_login_view_valid_data(self):
        url = reverse('login')
        response = self.client.post(url, {'username': 'Serge', 'password': '11111'})
        self.assertRedirects(response,
                             reverse('index'),
                             status_code=302,
                             target_status_code=200,
                             )

    def test_login_view_not_valid_data(self):
        url = reverse('login')
        response = self.client.post(url, {'username': TEST_USERNAME, 'password': TEST_PASSWORD})
        self.assertIn(INVALID_LOGIN_MESSAGE, response.content)

    def test_records_retrieving_view(self):
        for i in range(1, 20):
            request = IncomingRequest()
            request.url = 'test' + str(i)
            request.priority = i
            request.save()

        records_expected = []
        for record in IncomingRequest.objects.order_by('-visiting_date')[0:10]:
            records_expected.append(record.pk)

        url = reverse('requests')
        response = self.client.get(url)
        self.assertTrue(IncomingRequest.objects.all().count() == 20)

        records_retrieved = []
        for record in response.context['requests']:
            records_retrieved.append(record.pk)

        self.assertListEqual(records_expected, records_retrieved)

    def test_records_ordering_in_request_view(self):
        for i in range(1, 3):
            request = IncomingRequest()
            request.url = 'test' + str(i)
            request.priority = i
            request.save()
        url = reverse('requests')
        response = self.client.get(url)
        self.assertTrue(IncomingRequest.objects.all().count() == 3)
        self.assertEqual(response.context['requests'][0].priority, 2)
        self.assertEqual(response.context['requests'][1].priority, 1)
        self.assertEqual(response.context['requests'][2].priority, 0)




from django.test import TestCase
from django.core.urlresolvers import reverse
from ..models import Person
from django.template import Template, Context


class AdditionalTemplateLogicTestCase(TestCase):
    def test_context_processor(self):
        url = reverse('index')
        response = self.client.get(url)
        self.assertIn('settings', response.context)
        url = reverse('requests')
        response = self.client.get(url)
        self.assertIn('settings', response.context)

    def test_edit_link_template_tag(self):
        person = Person.objects.get(pk=1)
        c = Context({'person': person})
        test_template = Template("{% load hello_templatetags %} {% edit_link person %}")
        rendered = test_template.render(c)
        self.assertIn('<a href="/admin/hello/person/1/">(admin)</a>', rendered)

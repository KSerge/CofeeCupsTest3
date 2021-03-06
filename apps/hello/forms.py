from django.forms import ModelForm, Textarea, PasswordInput
from .models import Person
from django.contrib.auth.models import User
from .widgets import CalendarWidget


class PersonForm(ModelForm):
    class Meta:
        model = Person
        fields = ('bio', 'other_contacts', 'date_of_birth', 'jabber', 'skype', 'profile_image')
        widgets = {
            'bio': Textarea(attrs={'cols': 50, 'rows': 5, 'maxlength': 250}),
            'other_contacts': Textarea(attrs={'cols': 50, 'rows': 5, 'maxlength': 250}),
            'date_of_birth': CalendarWidget(attrs={'class': 'datepicker'}),
        }


class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')


class UserLoginForm(ModelForm):
    class Meta:
        model = User
        fields = ('username', 'password')
        widgets = {
            'password': PasswordInput()
        }
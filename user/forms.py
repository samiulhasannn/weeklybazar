from django import forms
from .models import CustomerProfile
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class LoginForm(UserCreationForm):
    mobile_number = forms.CharField(max_length=20, required=True)

    class Meta:
        model = User
        fields = ['mobile_number']

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        del self.fields['password1']
        del self.fields['password2']

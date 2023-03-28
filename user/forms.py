from django import forms
from .models import CustomerProfile


class LoginForm(forms.ModelForm):
    class Meta:
        model = CustomerProfile
        fields = ['customerMobile']


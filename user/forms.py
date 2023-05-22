from django import forms
from .models import CustomerProfile, Item
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class LoginForm(UserCreationForm):
    mobile_number = forms.CharField(max_length=20, required=True, widget=forms.TextInput(attrs={'value': '+88 '}))

    class Meta:
        model = User
        fields = ['mobile_number']

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        del self.fields['password1']
        del self.fields['password2']


class ProfileUpdateForm(forms.ModelForm):

    class Meta:
        model = CustomerProfile
        fields = ['customerName', 'customerEmail', 'customerAddress', 'customerImage']


# class ItemForm(forms.ModelForm):
#
#     class Meta:
#         model = Item
#         fields = ['itemName', 'itemType', 'itemPrice', 'itemQuantity', 'itemDescription', 'itemImage']

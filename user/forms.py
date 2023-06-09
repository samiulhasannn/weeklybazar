from django import forms
from .models import CustomerProfile, Item
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import formset_factory


class LoginForm(UserCreationForm):
    mobile_number = forms.CharField(max_length=11, required=True)

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


class OrderForm(forms.Form):
    field = forms.IntegerField(min_value=1)


OrderFormSet = formset_factory(OrderForm, extra=1)



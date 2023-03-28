from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from .forms import LoginForm


# Create your views here.
def login(request):
    form = LoginForm()
    return render(request, 'user/login.html', {'form': form})

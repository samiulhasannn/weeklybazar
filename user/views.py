from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from .forms import LoginForm
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect


# Create your views here.
def login_form(request):
    form = LoginForm()
    return render(request, 'user/login.html', {'form': form})


def homepage(request):
    if request.method == "POST":
        mobile_number = request.POST['customerMobile']
        try:
            user = User.objects.get(username=mobile_number)
            user = authenticate(request, username=mobile_number)
            login(request, user)
        except User.DoesNotExist:
            user = User.objects.create_user(username=mobile_number, password='none')
            user.save()
            user = authenticate(request, username=mobile_number, password='none')
            login(request, user)

        return HttpResponseRedirect('/home')

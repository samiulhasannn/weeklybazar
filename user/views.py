import pyotp
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from .forms import LoginForm
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from .utils import send_otp
from datetime import datetime


def homepage(request):
    return render(request, 'user/homepage.html')


# Create your views here.
def login_page(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            # form.save()
            mobile_number = form.cleaned_data.get('mobile_number')
            request.session['username'] = mobile_number
            try:
                user = User.objects.get(username=mobile_number)
                user = authenticate(request, username=mobile_number)
                send_otp(request)
                return redirect('otp')
            except User.DoesNotExist:
                user = User.objects.create_user(username=mobile_number, password='none')
                user.save()
                user = authenticate(request, username=mobile_number, password='none')
                send_otp(request)
                return redirect('otp')
    else:
        form = LoginForm()

    return render(request, 'user/login.html', {'form': form})


def otp_view(request):
    if request.method == 'POST':
        otp = request.POST['otp']
        username = request.session['username']
        print(username)

        otp_secret_key = request.session['otp_secret_key']
        otp_valid_date = request.session['otp_valid_date']

        if otp_secret_key and otp_valid_date is not None:
            valid_until = datetime.fromisoformat(otp_valid_date)

            if valid_until > datetime.now():
                totp = pyotp.TOTP(otp_secret_key, interval=60)
                if totp.verify(otp):
                    user = get_object_or_404(User, username=username)
                    login(request, user)
                    if request.user.is_authenticated:
                        print("Logged in successfully")

                    del request.session['otp_secret_key']
                    del request.session['otp_valid_date']

                    return redirect('home')
                else:
                    print("OTP is wrong")
                    return redirect('login')
            else:
                print("OTP expired")
                return redirect('login')
        else:
            print("Something went wrong")
            return redirect('login')

    return render(request, 'user/otp.html', {})


def logout_view(request):
    logout(request)

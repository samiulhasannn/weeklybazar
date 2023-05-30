import pyotp
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from .forms import LoginForm, OrderFormSet
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .utils import send_otp
from datetime import datetime
from .models import CustomerProfile, Item, Cart, Order, QuantifiedItem
from .forms import ProfileUpdateForm
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.utils.datastructures import MultiValueDictKeyError


def homepage(request):
    items = Item.objects.all()
    return render(request, 'user/homepage.html', {'items': items})


# Create your views here.
def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            # form.save()
            mobile_number = form.cleaned_data.get('mobile_number')

            if mobile_number.isnumeric() and len(mobile_number) == 11:
                request.session['username'] = mobile_number
                try:
                    user = User.objects.get(username=mobile_number)
                    user = authenticate(request, username=mobile_number)
                    send_otp(request)
                    return redirect('otp')
                except User.DoesNotExist:
                    user = User.objects.create_user(username=mobile_number, password='none')
                    user.save()

                    CustomerProfile.objects.create(user=user)
                    Cart.objects.create(user=user)

                    user = authenticate(request, username=mobile_number, password='none')
                    send_otp(request)
                    return redirect('otp')
            else:
                form = LoginForm()
                return render(request, 'user/login.html', {'form': form})

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

                    return redirect('homepage')
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


@login_required
def logout_view(request):
    logout(request)


@login_required
def profile_view(request):
    if request.method == "POST":
        form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.customerprofile)

        if form.is_valid():
            form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect("homepage")
    else:
        form = ProfileUpdateForm(instance=request.user.customerprofile)

    return render(request, 'user/profile.html', {'form': form})


@login_required
def cart_view(request):
    if request.method == "GET":
        try:
            if request.GET['action'] == 'submit_cart':
                for key in request.GET:
                    if key == 'item_id':
                        item_ids = request.GET.getlist(key)
                    if key == 'submit':
                        item_count = request.GET.getlist(key)

                user = User.objects.get(username=request.user.username)
                order = Order(user=user)
                order.save()
                for item_id, count in zip(item_ids, item_count):
                    item = Item.objects.get(itemID=item_id)
                    quantified_item = QuantifiedItem(item=item, quantity=count)
                    quantified_item.save()

                    order.items.add(QuantifiedItem.objects.filter(item=item, quantity=count).first())
                    order.save()

                request.user.cart.items.clear()
                print(order.__repr__())
                return render(request, 'user/order_success.html', {"values": order.__dict__})
        except MultiValueDictKeyError:
            pass

    product_id = request.GET.get('product')
    user = request.user

    try:
        user.cart.items.add(Item.objects.get(itemID=product_id))
    except Item.DoesNotExist:
        pass

    user.cart.save()
    return render(request, 'user/cart.html', {'user': user})


@login_required
def clear_cart(request):
    request.user.cart.items.clear()
    return render(request, 'user/cart.html')


@login_required
def remove_item(request):
    product_id = request.GET.get('product')
    user = request.user

    user.cart.items.remove(Item.objects.get(itemID=product_id))
    user.cart.save()

    return render(request, 'user/cart.html')

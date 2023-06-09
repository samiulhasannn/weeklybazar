"""weekly_bazar URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from user import views as user_views
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('accounts/', include('phone_auth.urls')),
    path('', user_views.homepage, name='homepage'),
    path('accounts/login/', user_views.login_view, name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page=settings.LOGOUT_REDIRECT_URL), name='logout'),
    path('home/', auth_views.LoginView.as_view(template_name='user/homepage.html'), name='home'),
    path('otp/', user_views.otp_view, name='otp'),
    path('profile/', user_views.profile_view, name='profile'),
    re_path(r'cart/$', user_views.cart_view, name='cart'),
    re_path(r'clear_cart/$', user_views.clear_cart, name='clear_cart'),
    re_path(r'remove_item/$', user_views.remove_item, name='remove_item'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

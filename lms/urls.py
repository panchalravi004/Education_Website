"""lms URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from django.urls import path,include
from lms import views, user_login

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.HOME,name='home'),
    path('base/', views.BASE,name='base'),
    path('single/course/', views.SINGLE_COURSE,name='single_course'),
    path('contact/', views.CONTACT,name='contact_us'),
    path('about/', views.ABOUT,name='about_us'),
    path('accounts/',include('django.contrib.auth.urls')),
    path('accounts/register/',user_login.REGISTER,name='register'),
    path('dologin/',user_login.LOGIN,name='dologin')
]

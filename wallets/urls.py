"""wallets URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from django.conf.urls import url

from core import views as core_views

# TODO(steve): the default for Django 2.0 was
# set to from django.urls import path and paths
# were used instead of urls that I am using now.
# which should we use??
urlpatterns = [
    #path('admin/', admin.site.urls),
    url('^$', core_views.home_page, name='home')
]

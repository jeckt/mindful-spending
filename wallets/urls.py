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
from django.conf.urls import include, url
from django.contrib.staticfiles.storage import staticfiles_storage
from django.views.generic.base import RedirectView

from core import views as core_views
from core import urls as core_urls

# TODO(steve): the default for Django 2.0 was
# set to from django.urls import path and paths
# were used instead of urls that I am using now.
# which should we use??
urlpatterns = [
    #path('admin/', admin.site.urls),
    url(r'^$', core_views.home_page, name='home'),
    url(r'^expenses/', include(core_urls)),

    url(r'^favicon.ico$',
        RedirectView.as_view(
            url=staticfiles_storage.url('img/favicon.ico'),
        ),
        name='favicon'
    ),
]

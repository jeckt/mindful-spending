from django.conf.urls import url
from core import views

urlpatterns = [
    url(r'^new$', views.new_expense, name='new_expense'),
]

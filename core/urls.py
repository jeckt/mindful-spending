from django.conf.urls import url
from core import views

urlpatterns = [
    url(r'^new$', views.new_expense, name='new_expense'),
    url(r'^(\d+)/delete$', views.delete_expense, name='delete_expense'),
    url(r'^edit$', views.edit_expenses, name='edit_expenses'),
]

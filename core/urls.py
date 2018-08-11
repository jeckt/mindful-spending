from django.conf.urls import url
from core import views

# TODO(steve): should we update the route to make it clearer?
# right now it is being used to edit and delete expenses.
# maybe change it to update???
urlpatterns = [
    url(r'^new$', views.new_expense, name='new_expense'),
    url(r'^(\d+)/delete$', views.delete_expense, name='delete_expense'),
    url(r'^edit$', views.edit_expenses, name='edit_expenses'),
    url(r'^edit/(\d+)$', views.edit_expense, name='edit_expense'),
]

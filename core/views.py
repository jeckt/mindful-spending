from django.shortcuts import render, redirect
from django.db.models import Sum
from django.core.exceptions import ValidationError

from core.models import Expense
from core.forms import ExpenseForm

from decimal import Decimal, InvalidOperation
from datetime import date

# TODO(steve): look at condensing down the render arguments.
# can we not just access these variables through the template?
def home_page(request):
    expense_total = Expense.objects.aggregate(Sum('amount'))['amount__sum']
    return render(request, 'home.html', {
        'form': ExpenseForm(),
        'expenses': Expense.objects.all(),
        'total_expenses': expense_total
    })

def new_expense(request):
    form = ExpenseForm(data=request.POST)
    if form.is_valid():
        form.save()
        return redirect('/')

    expense_total = Expense.objects.aggregate(Sum('amount'))['amount__sum']
    return render(request, 'home.html', {
        'form': form,
        'expenses': Expense.objects.all(),
        'total_expenses': expense_total
    })

def delete_expense(request, expense_id):
    try:
        expense = Expense.objects.get(pk=expense_id)
        expense.delete()
        return redirect('/')
    except:
        expense_total = Expense.objects.aggregate(Sum('amount'))['amount__sum']
        return render(request, 'home.html', {
            'expenses': Expense.objects.all(),
            'total_expenses': expense_total
        })

from django.shortcuts import render, redirect
from django.core.exceptions import ValidationError

from core.models import Expense, total_expenses
from core.forms import ExpenseForm

from decimal import Decimal, InvalidOperation
from datetime import date

# TODO(steve): look at condensing down the render arguments.
# can we not just access these variables through the template?
def home_page(request):
    return render(request, 'home.html', {
        'form': ExpenseForm(),
        'expenses': Expense.objects.all(),
        'total_expenses': total_expenses()
    })

def new_expense(request):
    form = ExpenseForm(data=request.POST)
    if form.is_valid():
        form.save()
        return redirect('/')

    return render(request, 'home.html', {
        'form': form,
        'expenses': Expense.objects.all(),
        'total_expenses': total_expenses()
    })

def delete_expense(request, expense_id):
    try:
        expense = Expense.objects.get(pk=expense_id)
        expense.delete()
        return redirect('/expenses/edit')
    except:
        return render(request, 'home.html', {
            'expenses': Expense.objects.all(),
            'total_expenses': total_expenses()
        })

def edit_expenses(request):
    return render(request, 'edit.html', {
        'expenses': Expense.objects.all(),
        'total_expenses': total_expenses()
    })

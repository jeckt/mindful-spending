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

# TODO(steve): this logic is slightly messy. Is there a better way??
# TODO(steve): we pass the expense date for now because it expense date is
# not editable when first released. We shall change this but for now this
# will fix the broken delete tests.
def edit_expenses(request):
    expense_forms = [ (expense.id, expense.date, ExpenseForm(instance=expense)) for expense in
                     Expense.objects.all() ]
    return render(request, 'edit.html', {
        'expense_forms': expense_forms,
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

def edit_expense(request, expense_id):
    form = ExpenseForm(data=request.POST)
    if form.is_valid():
        expense = Expense.objects.get(pk=expense_id)
        form = ExpenseForm(data=request.POST, instance = expense)
        form.save()

    return redirect('/expenses/edit')

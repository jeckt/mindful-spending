from django.shortcuts import render, redirect
from django.db.models import Sum
from django.core.exceptions import ValidationError

from core.models import Expense
from core.forms import ExpenseForm

from decimal import Decimal, InvalidOperation

def home_page(request):
    expenses = Expense.objects.all()
    expense_total = Expense.objects.aggregate(Sum('amount'))['amount__sum']
    return render(request, 'home.html', {
        'form': ExpenseForm(),
        'expenses': expenses,
        'total_expenses': expense_total
    })

def new_expense(request):
    form = ExpenseForm(data=request.POST)
    if form.is_valid():
        form.save()
        return redirect('/')

    expenses = Expense.objects.all()
    expense_total = Expense.objects.aggregate(Sum('amount'))['amount__sum']
    return render(request, 'home.html', {
        'form': form,
        'expenses': expenses,
        'total_expenses': expense_total
    })


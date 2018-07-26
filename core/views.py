from django.shortcuts import render, redirect
from django.db.models import Sum

from core.models import Expense

def home_page(request):
    expenses = Expense.objects.all()
    expense_total = Expense.objects.aggregate(Sum('amount'))['amount__sum']
    return render(request, 'home.html', {
        'expenses': expenses,
        'total_expenses': expense_total
    })

def new_expense(request):
    expense = Expense.objects.create(
        description=request.POST['description'],
        amount=request.POST['amount']
    )
    expense.save()
    expense.full_clean()
    return redirect('/')

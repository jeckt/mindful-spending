from django.shortcuts import render, redirect

from core.models import Expense

def home_page(request):
    expenses = Expense.objects.all()
    return render(request, 'home.html', {'expenses': expenses})

def new_expense(request):
    expense = Expense.objects.create(
        description=request.POST['description'],
        amount=request.POST['amount']
    )
    expense.save()
    expense.full_clean()
    return redirect('/')

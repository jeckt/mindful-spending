from django.shortcuts import render, redirect

from core.models import Expense

def home_page(request):
    return render(request, 'home.html')

def new_expense(request):
    expense = Expense.objects.create(
        description=request.POST['description'],
        amount=request.POST['amount']
    )
    expense.save()
    expense.full_clean()
    return redirect('/')

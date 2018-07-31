from django.shortcuts import render, redirect
from django.db.models import Sum
from django.core.exceptions import ValidationError

from core.models import Expense

from decimal import Decimal, InvalidOperation

EMPTY_DESCRIPTION_ERROR = 'Expense must have a description'
EMPTY_AMOUNT_ERROR = 'Expense must have an amount'
NEGATIVE_AMOUNT_ERROR = 'Expense must have positive amount'

def home_page(request):
    expenses = Expense.objects.all()
    expense_total = Expense.objects.aggregate(Sum('amount'))['amount__sum']
    return render(request, 'home.html', {
        'expenses': expenses,
        'total_expenses': expense_total
    })

# TODO(steve): we really need to refactor this!
# very complicated and can benefit from using forms!
def new_expense(request):
    try:
        amount = Decimal(request.POST['amount'])
        expense = Expense.objects.create(
            description=request.POST['description'],
            amount=amount
        )

        try:
            expense.full_clean()
            return redirect('/')
        except ValidationError as e:
            expense.delete()
            if 'description' in e.message_dict:
                error = EMPTY_DESCRIPTION_ERROR
            else:
                error = NEGATIVE_AMOUNT_ERROR

    except InvalidOperation:
        error = EMPTY_AMOUNT_ERROR

    return render(request, 'home.html', {'error': error})

from django.db import models
from django.db.models import Sum
from django.core.validators import MinValueValidator

from decimal import Decimal
from datetime import date

# TODO(steve): should be encapsulated in an object
# this will happen when we attach expenses to user
def total_expenses():
    return Expense.objects.aggregate(Sum('amount'))['amount__sum']

class Expense(models.Model):
    description = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2,
                    default=0, validators=[MinValueValidator(Decimal('0.01'))]
    )
    date = models.DateField(default=date.today)

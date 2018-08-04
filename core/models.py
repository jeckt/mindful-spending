from django.db import models
from django.core.validators import MinValueValidator

from decimal import Decimal
from datetime import date

class Expense(models.Model):
    description = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2,
                    default=0, validators=[MinValueValidator(Decimal('0.01'))]
    )
    date = models.DateField(default=date.today)

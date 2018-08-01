from django import forms

from core.models import Expense
from core.views import (
    EMPTY_DESCRIPTION_ERROR, EMPTY_AMOUNT_ERROR, NEGATIVE_AMOUNT_ERROR
)

# TODO(steve): move the error messages definition to forms.py
class ExpenseForm(forms.models.ModelForm):

    class Meta:
        model = Expense
        fields = ('description', 'amount',)
        widgets = {
            'description': forms.fields.TextInput(attrs={
                'placeholder': 'Enter a short description of the expense',
                'class': 'form-control'
            }),
            'amount': forms.fields.NumberInput(attrs={
                'placeholder': '$0.00',
                'class': 'form-control',
                'min': '0.01'
            }),
        }
        error_messages = {
            'description': {'required': EMPTY_DESCRIPTION_ERROR},
            'amount': {
                'required': EMPTY_AMOUNT_ERROR,
                'min_value': NEGATIVE_AMOUNT_ERROR
            }
        }

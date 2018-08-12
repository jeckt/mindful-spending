from django import forms

from core.models import Expense

EMPTY_DESCRIPTION_ERROR = 'Expense must have a description'
EMPTY_AMOUNT_ERROR = 'Expense must have an amount'
NEGATIVE_AMOUNT_ERROR = 'Expense must have positive amount'

class ExpenseForm(forms.models.ModelForm):

    class Meta:
        model = Expense
        fields = ('description', 'amount', 'date',)
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
            'date': forms.HiddenInput(),
        }
        error_messages = {
            'description': {'required': EMPTY_DESCRIPTION_ERROR},
            'amount': {
                'required': EMPTY_AMOUNT_ERROR,
                'min_value': NEGATIVE_AMOUNT_ERROR
            }
        }

class EditExpenseForm(ExpenseForm):

    class Meta(ExpenseForm.Meta):
        widgets = {
            'date': forms.fields.DateInput(format=('%Y-%m-%d'),
               attrs={'class': 'form-control'}
            ),
        }

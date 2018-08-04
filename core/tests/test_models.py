from django.test import TestCase
from django.core.exceptions import ValidationError

from core.models import Expense

from decimal import Decimal
from datetime import date

class ExpenseModelTest(TestCase):

    def test_default_expense(self):
        expense = Expense()
        self.assertEqual(expense.description, '')
        self.assertEqual(expense.amount, Decimal('0'))
        self.assertEqual(expense.date, date.today())

    def test_cannot_save_expense_with_no_description(self):
        expense = Expense.objects.create(description='',
                        amount=Decimal('5.5')
        )
        with self.assertRaises(ValidationError):
            expense.save()
            expense.full_clean()

    def test_cannot_save_expense_with_zero_amount(self):
        expense = Expense.objects.create(description='expense',
                        amount=Decimal('0')
        )
        with self.assertRaises(ValidationError):
            expense.save()
            expense.full_clean()

    def test_cannot_save_expense_with_negative_amount(self):
        expense = Expense.objects.create(description='expense',
                        amount=Decimal('-0.01')
        )
        with self.assertRaises(ValidationError):
            expense.save()
            expense.full_clean()

    def test_can_save_expense_with_positive_amount(self):
        expense = Expense.objects.create(description='expense',
                        amount=Decimal('0.01')
        )
        expense.save()
        expense.full_clean() # should not raise

    def test_cannot_save_expense_with_no_date(self):
        with self.assertRaises(ValidationError):
            expense = Expense.objects.create(
                description='expense',
                amount=Decimal('1'),
                date=''
            )
            expense.save()
            expense.full_clean()

from django.test import TestCase

from core.forms import ExpenseForm
from core.views import (
    EMPTY_DESCRIPTION_ERROR, EMPTY_AMOUNT_ERROR, NEGATIVE_AMOUNT_ERROR
)

import re

class ExpenseFormTest(TestCase):

    def test_form_renders_description_input(self):
        form = ExpenseForm()

        description_html = form.as_p()
        match = re.search(r'<input(.+?)name="description"(.+?)/>'
                          , description_html)
        if match:
            description_html = match.group(0)

        self.assertIn(
            'placeholder="Enter a short description of the expense"',
            description_html
        )
        self.assertIn('class="form-control"', description_html)

    def test_form_renders_amount_input(self):
        form = ExpenseForm()

        amount_html = form.as_p()
        match = re.search(r'<input(.+?)name="amount"(.+?)/>'
                          , amount_html)
        if match:
            amount_html = match.group(0)

        self.assertIn(
            'placeholder="$0.00"',
            amount_html
        )
        self.assertIn('class="form-control"', amount_html)
        self.assertIn('min="0.01"', amount_html)

    def test_form_validation_for_empty_description(self):
        form = ExpenseForm(data={
            'description': '',
            'amount': 5.25
        })
        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors['description'],
            [EMPTY_DESCRIPTION_ERROR]
        )

    def test_form_validation_for_empty_amount(self):
        form = ExpenseForm(data={
            'description': 'No amount',
            'amount': ''
        })
        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors['amount'],
            [EMPTY_AMOUNT_ERROR]
        )

    def test_form_validation_for_negative_amount(self):
        form = ExpenseForm(data={
            'description': 'Negative amount',
            'amount': '-0.4'
        })
        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors['amount'],
            [NEGATIVE_AMOUNT_ERROR]
        )

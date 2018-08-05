from django.test import TestCase

from core.forms import ExpenseForm
from core.forms import (
    EMPTY_DESCRIPTION_ERROR, EMPTY_AMOUNT_ERROR, NEGATIVE_AMOUNT_ERROR
)

import re
from datetime import date

class ExpenseFormTest(TestCase):

    def setUp(self):
        self.date_string = date.today().strftime('%Y-%m-%d')

    def get_input_html(self, name):
        form = ExpenseForm()
        html = form.as_p()
        match = re.search(r'<input(.+?)name="%s"(.+?)/>' % (name,), html)
        if match:
            html = match.group(0)

        return html

    def test_form_renders_description_input(self):
        description_html = self.get_input_html('description')

        self.assertIn(
            'placeholder="Enter a short description of the expense"',
            description_html
        )
        self.assertIn('class="form-control"', description_html)

    def test_form_renders_amount_input(self):
        amount_html = self.get_input_html('amount')

        self.assertIn(
            'placeholder="$0.00"',
            amount_html
        )
        self.assertIn('class="form-control"', amount_html)
        self.assertIn('min="0.01"', amount_html)

    def test_form_renders_hidden_date_input(self):
        date_html = self.get_input_html('date')
        self.assertIn('type="hidden"', date_html)
        self.assertIn(f'value="{self.date_string}"', date_html)

    def test_form_validation_for_empty_description(self):
        form = ExpenseForm(data={
            'description': '',
            'amount': 5.25,
            'date': self.date_string
        })
        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors['description'],
            [EMPTY_DESCRIPTION_ERROR]
        )

    def test_form_validation_for_empty_amount(self):
        form = ExpenseForm(data={
            'description': 'No amount',
            'amount': '',
            'date': self.date_string
        })
        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors['amount'],
            [EMPTY_AMOUNT_ERROR]
        )

    def test_form_validation_for_negative_amount(self):
        form = ExpenseForm(data={
            'description': 'Negative amount',
            'amount': '-0.4',
            'date': self.date_string
        })
        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors['amount'],
            [NEGATIVE_AMOUNT_ERROR]
        )

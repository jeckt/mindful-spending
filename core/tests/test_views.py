from django.test import TestCase
from django.utils.html import escape

from core.models import Expense
from core.forms import (
    EMPTY_DESCRIPTION_ERROR, EMPTY_AMOUNT_ERROR, NEGATIVE_AMOUNT_ERROR
)

class HomePageTest(TestCase):

    def test_uses_home_template(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'home.html')

    # TODO(steve): should we name the app core or expenses?!?
    def test_can_save_POST_request(self):
        self.client.post('/expenses/new', data={
            'description': 'new expense',
            'amount': 6.5
        })

        self.assertEqual(Expense.objects.count(), 1)
        new_expense = Expense.objects.first()
        self.assertEqual(new_expense.description, 'new expense')
        self.assertEqual(new_expense.amount, 6.5)

    def test_POST_redirects_to_home_page(self):
        response = self.client.post('/expenses/new', data={
            'description': 'new expense',
            'amount': 6.5
        })
        self.assertRedirects(response, '/')

    def test_expenses_displayed_on_home_page(self):
        Expense.objects.create(description='expense 1',
                               amount=5.25
        )
        Expense.objects.create(description='expense 2',
                               amount=2.5
        )

        response = self.client.get('/')

        self.assertContains(response, 'expense 1')
        self.assertContains(response, 'expense 2')
        self.assertContains(response, '5.25')
        self.assertContains(response, '2.5')

    def test_total_expenses_displayed_on_home_page(self):
        Expense.objects.create(description='expense 1',
                               amount=5.25
        )
        Expense.objects.create(description='expense 2',
                               amount=2.5
        )

        response = self.client.get('/')

        self.assertContains(response, '7.75')

    def test_invalid_input_doesnt_clear_previous_expenses(self):
        Expense.objects.create(description='expense 1',
                               amount=5.25
        )
        Expense.objects.create(description='expense 2',
                               amount=2.5
        )
        response = self.client.post('/expenses/new', data={
            'description': '',
            'amount': 6.5
        })

        self.assertContains(response, 'expense 1')
        self.assertContains(response, 'expense 2')
        self.assertContains(response, '5.25')
        self.assertContains(response, '2.5')

        self.assertContains(response, '7.75') # total expenses

    # TODO(steve): should we move this into separate test cases?!
    def test_for_invalid_input_nothing_saved_to_db(self):
        self.client.post('/expenses/new', data={
            'description': '',
            'amount': 5.25
        })
        self.assertEqual(Expense.objects.count(), 0)

        self.client.post('/expenses/new', data={
            'description': '',
            'amount': ''
        })
        self.assertEqual(Expense.objects.count(), 0)

        self.client.post('/expenses/new', data={
            'description': 'No amount',
            'amount': ''
        })
        self.assertEqual(Expense.objects.count(), 0)

        self.client.post('/expenses/new', data={
            'description': 'Negative amount',
            'amount': -0.4
        })
        self.assertEqual(Expense.objects.count(), 0)

    def test_empty_description_shows_errors(self):
        response = self.client.post('/expenses/new', data={
            'description': '',
            'amount': 5.25
        })

        expected_error = escape(EMPTY_DESCRIPTION_ERROR)
        self.assertContains(response, expected_error)
        self.assertTemplateUsed(response, 'home.html')

    def test_empty_amount_shows_errors(self):
        response = self.client.post('/expenses/new', data={
            'description': 'No amount',
            'amount': ''
        })

        expected_error = escape(EMPTY_AMOUNT_ERROR)
        self.assertContains(response, expected_error)
        self.assertTemplateUsed(response, 'home.html')

    def test_negative_amount_shows_errors(self):
        response = self.client.post('/expenses/new', data={
            'description': 'Negative amount',
            'amount': -0.4
        })

        expected_error = escape(NEGATIVE_AMOUNT_ERROR)
        self.assertContains(response, expected_error)
        self.assertTemplateUsed(response, 'home.html')


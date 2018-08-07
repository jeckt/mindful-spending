from django.test import TestCase
from django.utils.html import escape

from core.models import Expense
from core.forms import (
    ExpenseForm, EMPTY_DESCRIPTION_ERROR,
    EMPTY_AMOUNT_ERROR, NEGATIVE_AMOUNT_ERROR
)

from datetime import date

today = date.today()
today_display = today.strftime('%d-%b-%Y')
today_input = today.strftime('%Y-%m-%d')

def create_two_expense_objects():
    Expense.objects.create(description='expense 1',
                           amount=5.25,
                           date=today
    )
    Expense.objects.create(description='expense 2',
                           amount=2.5,
                           date=today
    )

# TODO(steve): should we name the app core or expenses?!?
class HomePageTest(TestCase):

    def test_uses_home_template(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'home.html')

    def test_home_page_uses_expense_form(self):
        response = self.client.get('/')
        self.assertIsInstance(response.context['form'], ExpenseForm)

    def test_can_save_POST_request(self):
        response = self.client.post('/expenses/new', data={
            'description': 'new expense',
            'amount': 6.5,
            'date': today_input
        })
        self.assertRedirects(response, '/')
        self.assertEqual(Expense.objects.count(), 1)
        new_expense = Expense.objects.first()
        self.assertEqual(new_expense.description, 'new expense')
        self.assertEqual(new_expense.amount, 6.5)

    def test_POST_redirects_to_home_page(self):
        response = self.client.post('/expenses/new', data={
            'description': 'new expense',
            'amount': 6.5,
            'date': today_input
        })
        self.assertRedirects(response, '/')

    def test_expenses_displayed_on_home_page(self):
        create_two_expense_objects()

        response = self.client.get('/')

        self.assertContains(response, 'expense 1')
        self.assertContains(response, 'expense 2')
        self.assertContains(response, '5.25')
        self.assertContains(response, '2.5')
        self.assertEqual(response.content.decode().count(today_display), 2)

    def test_total_expenses_displayed_on_home_page(self):
        create_two_expense_objects()
        response = self.client.get('/')
        self.assertContains(response, '7.75')

class ExpenseValidationViewTest(TestCase):

    def post_expense_with_empty_description(self):
        return self.client.post('/expenses/new', data={
            'description': '',
            'amount': 5.25,
            'date': today_input
        })

    def test_invalid_input_doesnt_clear_previous_expenses(self):
        create_two_expense_objects()
        response = self.post_expense_with_empty_description()
        self.assertContains(response, 'expense 1')
        self.assertContains(response, 'expense 2')
        self.assertContains(response, '5.25')
        self.assertContains(response, '2.5')
        self.assertEqual(response.content.decode().count(today_display), 2)

        self.assertContains(response, '7.75') # total expenses

    def test_for_invalid_input_passes_form_to_template(self):
        response = self.post_expense_with_empty_description()
        self.assertIsInstance(response.context['form'], ExpenseForm)

    # TODO(steve): should we move this into separate test cases?!
    def test_for_invalid_input_nothing_saved_to_db(self):
        self.post_expense_with_empty_description()
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
        response = self.post_expense_with_empty_description()
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

class ExpenseDeletionTest(TestCase):

    def test_can_delete_POST_request(self):
        expense = Expense.objects.create()
        self.assertEqual(Expense.objects.count(), 1)
        self.client.post(f'/expenses/{expense.id}/delete')
        self.assertEqual(Expense.objects.count(), 0)

    def test_delete_POST_redirects_to_edit_page(self):
        expense = Expense.objects.create()
        response = self.client.post(f'/expenses/{expense.id}/delete')
        self.assertRedirects(response, '/expenses/edit')

class ExpenseEditViewTest(TestCase):

    def test_uses_edit_template(self):
        response = self.client.get('/expenses/edit')
        self.assertTemplateUsed(response, 'edit.html')

    def test_expenses_displayed_on_home_page(self):
        create_two_expense_objects()

        response = self.client.get('/expenses/edit')

        self.assertContains(response, 'expense 1')
        self.assertContains(response, 'expense 2')
        self.assertContains(response, '5.25')
        self.assertContains(response, '2.5')
        self.assertEqual(response.content.decode().count(today_display), 2)

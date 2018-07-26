from django.test import TestCase

from core.models import Expense

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

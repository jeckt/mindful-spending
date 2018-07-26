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

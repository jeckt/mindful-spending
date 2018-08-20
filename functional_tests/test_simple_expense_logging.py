from .base import FunctionalTest
from .page import HomePage

from datetime import date

class NewVistorTest(FunctionalTest):

    def test_vistor_can_log_expenses_and_view_total(self):
        # Harold hears about a cool new web app that allows
        # him to log expenses. He goes to the homepage to
        # check it out
        self.browser.get(self.live_server_url)
        home_page = HomePage(self)
        expense_date = date.today()

        # He notices the page title and header contains
        # the name of the web app
        self.assertIn('Mindful Spending', home_page.get_title())
        self.assertIn('Mindful Spending', home_page.get_header())

        # He sees that there are two input boxes where
        # he is invited to enter a short description
        # of the expense and the amount
        description_box = home_page.get_description_input_box()
        self.assertEqual(
            description_box.get_attribute('placeholder'),
            'Enter a short description of the expense'
        )

        amount_box = home_page.get_amount_input_box()
        self.assertEqual(
            amount_box.get_attribute('placeholder'),
            '$0.00'
        )

        # Remembering that he bought some smashed avocado for
        # breakfast he decides to put that in to give the app
        # a go.
        description_box.send_keys('Smashed Avo for brekkie')
        home_page.get_amount_input_box().clear()
        home_page.get_amount_input_box().send_keys("6.50")
        home_page.get_submit_input_button().click()

        # After hitting enter, the page refreshes and he
        # can see the smashed avo expense in the log
        home_page.wait_for_row_in_list_table(
            'Smashed Avo for brekkie',
            '6.50',
            expense_date
        )

        # After entering the breakfast in the app he decides
        # to take a break and grab a coffee with a work friend,
        # where he tells his friend about the cool new app!
        # Coming back from coffee and logs that into the app
        home_page.get_description_input_box().send_keys('Moonbucks Mocha')
        home_page.get_amount_input_box().clear()
        home_page.get_amount_input_box().send_keys("2.75")
        home_page.get_submit_input_button().click()

        # The page updates and shows both expenses with
        # how much each item cost.
        home_page.wait_for_row_in_list_table(
            'Smashed Avo for brekkie',
            '6.50',
            expense_date
        )
        home_page.wait_for_row_in_list_table(
            'Moonbucks Mocha',
            '2.75',
            expense_date
        )

        # It shows him the total amount he has spent. Neat!
        rows = home_page.get_total_expenses()
        self.assertIn('$9.25', [row.text for row in rows])

        # Before getting too carried away - he gets back to work!

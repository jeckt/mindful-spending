from .base import FunctionalTest

from datetime import datetime

class NewVistorTest(FunctionalTest):

    def test_vistor_can_log_expenses_and_view_total(self):
        # Harold hears about a cool new web app that allows
        # him to log expenses. He goes to the homepage to
        # check it out
        self.browser.get(self.live_server_url)
        today = datetime.today()

        # He notices the page title and header contains
        # the name of the web app
        self.assertIn('Mindful Spending', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('Mindful Spending', header_text)

        # He sees that there are two input boxes where
        # he is invited to enter a short description
        # of the expense and the amount
        description_box = self.get_description_input_box()
        self.assertEqual(
            description_box.get_attribute('placeholder'),
            'Enter a short description of the expense'
        )

        amount_box = self.get_amount_input_box()
        self.assertEqual(
            amount_box.get_attribute('placeholder'),
            '$0.00'
        )

        # Remembering that he bought some smashed avocado for
        # breakfast he decides to put that in to give the app
        # a go.
        description_box.send_keys('Smashed Avo for brekkie')
        self.get_amount_input_box().clear()
        self.get_amount_input_box().send_keys("6.50")
        self.get_submit_input_button().click()

        # After hitting enter, the page refreshes and he
        # can see the smashed avo expense in the log
        self.wait_for_row_in_list_table('Smashed Avo for brekkie',
                                        '$6.50',
                                        today)

        # After entering the breakfast in the app he decides
        # to take a break and grab a coffee with a work friend,
        # where he tells his friend about the cool new app!
        # Coming back from coffee and logs that into the app
        self.get_description_input_box().send_keys('Moonbucks Mocha')
        self.get_amount_input_box().clear()
        self.get_amount_input_box().send_keys("2.75")
        self.get_submit_input_button().click()

        # The page updates and shows both expenses with
        # how much each item cost.
        self.wait_for_row_in_list_table('Smashed Avo for brekkie',
                                        '$6.50',
                                        today)
        self.wait_for_row_in_list_table('Moonbucks Mocha',
                                        '$2.75',
                                        today)

        # It shows him the total amount he has spent. Neat!
        rows = self.browser.find_elements_by_id('id_total_expense')
        self.assertIn('$9.25', [row.text for row in rows])

        # Before getting too carried away - he gets back to work!

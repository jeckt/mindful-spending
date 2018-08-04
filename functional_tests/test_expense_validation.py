from .base import FunctionalTest

from datetime import datetime

class ExpenseValidationTest(FunctionalTest):

    # TODO(steve): is this test too long?!
    # Should we test the edge cases or should the unit test?
    def test_cannot_add_empty_expense_amount_or_description(self):
        # Harold goes to the home page and accidentally
        # clicks the log button before even adding an amount
        # to his burger for lunch!
        self.browser.get(self.live_server_url)
        today = datetime.today().date().strftime('%d-%b-%Y')
        self.get_description_input_box().send_keys('Burger for lunch')
        self.get_submit_input_button().click()

        # The browser intercepts the request, and does not
        # add the empty expense to the list and provides
        # him with a warning.
        self.wait_for(lambda: self.browser.find_element_by_css_selector(
            '#id_amount:invalid'
        ))

        # He then starts entering an amount for the new item
        # But forgets he doesn't need to put a minus to show
        # that it is an expense!
        self.get_amount_input_box().clear()
        self.get_amount_input_box().send_keys("-8.35")
        self.get_submit_input_button().click()
        self.wait_for(lambda: self.browser.find_element_by_css_selector(
            '#id_amount:invalid'
        ))

        # He removes the minus in the amount and tries again.
        self.get_amount_input_box().clear()
        self.get_amount_input_box().send_keys("8.35")
        self.wait_for(lambda: self.browser.find_element_by_css_selector(
            '#id_amount:valid'
        ))

        # This time it works!
        self.get_submit_input_button().click()
        self.wait_for_row_in_list_table('Burger for lunch',
                                        '$8.35',
                                        today)

        # That was difficult! On the drive home from work
        # he decided to buy a Maccas Large Soda and this
        # time remembers to input the amount!
        self.get_amount_input_box().send_keys("1.09")
        self.get_submit_input_button().click()

        # Unfortunately he forgot to put the description
        # and gets another error!
        self.wait_for(lambda: self.browser.find_element_by_css_selector(
            '#id_description:invalid'
        ))

        # He starts typing the description and the error
        # disappears
        self.get_description_input_box().send_keys('Maccas Large Soda')
        self.wait_for(lambda: self.browser.find_element_by_css_selector(
            '#id_amount:valid'
        ))

        # He now can log the second expense!
        self.get_submit_input_button().click()
        self.wait_for_row_in_list_table('Burger for lunch',
                                        '$8.35',
                                        today)
        self.wait_for_row_in_list_table('Maccas Large Soda',
                                        '$1.09',
                                        today)

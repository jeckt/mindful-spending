from .base import FunctionalTest

class ExpenseValidationTest(FunctionalTest):

    # TODO(steve): is this test too long?!
    # Should we test the edge cases or should the unit test?
    def test_cannot_add_empty_expense_amount_or_description(self):
        # Harold goes to the home page and accidentally
        # clicks the log button before even adding an amount
        # to his burger for lunch!
        self.browser.get(self.live_server_url)
        description_box = self.browser.find_element_by_id('id_desc_text')
        description_box.send_keys('Burger for lunch')
        self.browser.find_element_by_id('id_submit').click()

        # The browser intercepts the request, and does not
        # add the empty expense to the list and provides
        # him with a warning.
        self.wait_for(lambda: self.browser.find_element_by_css_selector(
            '#id_amount:invalid'
        ))

        # He then starts entering an amount for the new item
        amount_box = self.browser.find_element_by_id('id_amount')
        amount_box.send_keys("-8.35")
        self.wait_for(lambda: self.browser.find_element_by_css_selector(
            '#id_amount:valid'
        ))

        # But forgets he doesn't need to put a minus to show
        # that it is an expense!
        self.browser.find_element_by_id('id_submit').click()
        self.wait_for(lambda: self.browser.find_element_by_css_selector(
            '#id_amount:invalid'
        ))

        # He removes the minus in the amount and tries again.
        self.browser.find_element_by_id('id_amount').clear()
        amount_box = self.browser.find_element_by_id('id_amount')
        amount_box.send_keys("8.35")
        self.wait_for(lambda: self.browser.find_element_by_css_selector(
            '#id_amount:valid'
        ))

        # This time it works!
        self.browser.find_element_by_id('id_submit').click()
        self.wait_for_row_in_list_table('Burger for lunch',
                                        '$8.35')

        # That was difficult! On the drive home from work
        # he decided to buy a Maccas Large Soda and this
        # time remembers to input the amount!
        amount_box = self.browser.find_element_by_id('id_amount')
        amount_box.send_keys("1.09")
        self.browser.find_element_by_id('id_submit').click()

        # Unfortunately he forgot to put the description
        # and gets another error!
        self.wait_for(lambda: self.browser.find_element_by_css_selector(
            '#id_desc_text:invalid'
        ))

        # He starts typing the description and the error
        # disappears
        description_box = self.browser.find_element_by_id('id_desc_text')
        description_box.send_keys('Maccas Large Soda')
        self.wait_for(lambda: self.browser.find_element_by_css_selector(
            '#id_amount:valid'
        ))

        # He now can log the second expense!
        self.browser.find_element_by_id('id_submit').click()
        self.wait_for_row_in_list_table('Burger for lunch',
                                        '$8.35')
        self.wait_for_row_in_list_table('Maccas Large Soda',
                                        '$1.09')

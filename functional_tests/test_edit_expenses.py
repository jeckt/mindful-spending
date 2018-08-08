from .base import FunctionalTest

from datetime import date, timedelta

class ExpenseEditTest(FunctionalTest):

    def test_visitor_can_edit_an_expense(self):
        # Harold told Maggie about this new web app
        # to track expenses and she decides to check
        # it out.
        self.browser.get(self.live_server_url)

        # She logs her first expense. She normally doesn't
        # have breakfast and today was no exception, so
        # she logs last night's team drinks.
        expense_date = date.today() + timedelta(days=-1)
        date_string = expense_date.strftime('%d-%b-%Y')
        self.get_description_input_box().send_keys('Beers after work')
        self.get_amount_input_box().send_keys('37.10')
        self.get_submit_input_button().click()

        # She sees the expense in the list!
        self.wait_for_row_in_list_table('Beers after work',
                                        '$37.10',
                                        self.expense_date)

        # Unfortunately it doesn't have the right date!
        # She proceeds to the edit page.
        self.browser.find_element_by_id('id_edit').click()

        # Here she sees that she is able to change the
        # date of the expense and does so.
        self.wait_for_row_in_list_table('Beers after work',
                                        '$37.10',
                                        self.expense_date)
        date_input = self.browser.find_elements_by_tag_name('td')[0]
        date_input.clear()
        date_input.send_keys(date_string)
        self.wait_for(lambda:
                      self.browser.find_element_by_id('id_edit_1').click())

        # The page refreshes and she sees the expense date
        # has updated to what she expected
        self.wait_for_row_in_list_table('Beers after work',
                                        '$37.10',
                                        date_string)

        # Thinking again she forgot about the tip! So
        # she goes ahead and updates that as well.
        amount_input = self.browser.find_elements_by_tag_name('td')[2]
        amount_input.clear()
        amount_input.send_keys('47.10')
        self.wait_for(lambda:
                      self.browser.find_element_by_id('id_edit_1').click())

        # Again she sees that has updated...
        self.wait_for_row_in_list_table('Beers after work',
                                        '$47.10',
                                        date_string)

        # Satisfied she returns to the home page
        # and see the changes have persisted.
        self.browser.find_element_by_id('id_home').click()
        self.wait_for_row_in_list_table('Beers after work',
                                        '$47.10',
                                        date_string)

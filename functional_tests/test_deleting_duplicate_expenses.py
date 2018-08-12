from .base import FunctionalTest
from .base import wait

from datetime import date, timedelta

class ExpenseDeletionTest(FunctionalTest):

    # TODO(steve): surely this test can be made more readible!
    @wait
    def wait_for_multiple_rows_in_list_table(self, description, amount,
                                             expense_date, count):
        rows = self.browser.find_elements_by_tag_name('td')
        rows_text = [row.text for row in rows]
        self.assertEqual(len([text for text in rows_text if text ==
                              description]), count)
        self.assertEqual(len([text for text in rows_text if text ==
                              f'${amount}']), count)
        self.assertEqual(len([text for text in rows_text if text ==
                              expense_date]), count)

    def test_visitor_can_delete_an_expense(self):
        # Harold is now in the swing of things and is loving the
        # web app. He starts using it religiously. He just got
        # out of the petrol station and decides to logs it.
        self.browser.get(self.live_server_url)

        description = 'Gas for car'
        amount = '62.18'
        expense_date = date.today().strftime('%Y-%m-%d')

        self.get_description_input_box().send_keys(description)
        self.get_amount_input_box().send_keys(amount)
        self.get_submit_input_button().click()

        # He sees that the expense has been recorded in the app
        self.wait_for_row_in_list_table(description,
                                        f'${amount}',
                                        self.expense_date)

        # Nice, unfortunately he accidentally logs the expense
        # twice!
        self.get_description_input_box().send_keys(description)
        self.get_amount_input_box().send_keys(amount)
        self.get_submit_input_button().click()

        # He notices now that there are two entries...
        self.wait_for_multiple_rows_in_list_table(description, amount,
                                                  self.expense_date, 2)

        # To fix this clicks on the edit button to edit the expenses...
        self.browser.find_element_by_id('id_edit').click()

        # He sees the duplicate entry and the ability to delete it
        # with a delete button. So he does!
        self.wait_for_multiple_rows_in_edit_table(description, amount,
                                                  expense_date, 2)
        self.wait_for(lambda:
                      self.browser.find_element_by_id('id_delete_2').click())

        # The screen refreshs and he only sees one entry!
        self.wait_for_multiple_rows_in_edit_table(description, amount,
                                                  expense_date, 1)

        # Satisified he returns to the home page where he can
        # continue adding expenses!
        self.browser.find_element_by_id('id_home').click()
        self.wait_for_multiple_rows_in_list_table(description, amount,
                                                  self.expense_date, 1)

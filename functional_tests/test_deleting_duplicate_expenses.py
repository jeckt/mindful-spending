from .base import FunctionalTest
from .page import HomePage, EditPage

from datetime import date, timedelta

class ExpenseDeletionTest(FunctionalTest):

    def test_visitor_can_delete_an_expense(self):
        # Harold is now in the swing of things and is loving the
        # web app. He starts using it religiously. He just got
        # out of the petrol station and decides to logs it.
        self.browser.get(self.live_server_url)
        home_page = HomePage(self)

        description = 'Gas for car'
        amount = '62.18'
        expense_date = date.today()

        home_page.get_description_input_box().send_keys(description)
        home_page.get_amount_input_box().send_keys(amount)
        home_page.get_submit_input_button().click()

        # He sees that the expense has been recorded in the app
        home_page.wait_for_row_in_list_table(
            description,
            amount,
            expense_date
        )

        # Nice, unfortunately he accidentally logs the expense
        # twice!
        home_page.get_description_input_box().send_keys(description)
        home_page.get_amount_input_box().send_keys(amount)
        home_page.get_submit_input_button().click()

        # He notices now that there are two entries...
        home_page.wait_for_multiple_rows_in_list_table(
            description,
            amount,
            expense_date,
            2
        )

        # To fix this clicks on the edit button to edit the expenses...
        edit_page = home_page.go_to_edit_page()

        # He sees the duplicate entry and the ability to delete it
        # with a delete button. So he does!
        edit_page.wait_for_multiple_rows_in_table(
            description,
            amount,
            expense_date,
            2
        )
        edit_page.delete_expense(2)

        # The screen refreshs and he only sees one entry!
        edit_page.wait_for_multiple_rows_in_table(
            description,
            amount,
            expense_date,
            1
        )

        # Satisified he returns to the home page where he can
        # continue adding expenses!
        home_page = edit_page.go_to_home_page()
        home_page.wait_for_multiple_rows_in_list_table(
            description,
            amount,
            expense_date,
            1
        )

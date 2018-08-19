from .base import FunctionalTest
from .page import HomePage, EditPage

from datetime import date, timedelta

class ExpenseEditTest(FunctionalTest):

    def test_visitor_can_edit_an_expense(self):
        # Harold told Maggie about this new web app
        # to track expenses and she decides to check
        # it out.
        self.browser.get(self.live_server_url)
        home_page = HomePage(self)

        description = 'Beers after work'
        amount = '37.10'
        amount_with_tip = '47.10'
        expense_date = date.today()
        new_expense_date = expense_date + timedelta(days=-1)

        # She logs her first expense. She normally doesn't
        # have breakfast and today was no exception, so
        # she logs last night's team drinks.
        home_page.get_description_input_box().send_keys(description)
        home_page.get_amount_input_box().send_keys(amount)
        home_page.get_submit_input_button().click()

        # She sees the expense in the list!
        home_page.wait_for_row_in_list_table(
            description,
            amount,
            expense_date
        )

        # Unfortunately it doesn't have the right date!
        # She proceeds to the edit page.
        edit_page = home_page.go_to_edit_page()

        # Here she sees that she is able to change the
        # date of the expense and does so.
        edit_page.wait_for_multiple_rows_in_table(
            description,
            amount,
            expense_date,
            1
        )

        new_expense_date = date.today() + timedelta(days=-1)
        edit_page.update_date(new_expense_date)
        edit_page.update_expense()

        # The page refreshes and she sees the expense date
        # has updated to what she expected
        edit_page.wait_for_multiple_rows_in_table(
            description,
            amount,
            new_expense_date,
            1
        )

        # Thinking again she forgot about the tip! So
        # she goes ahead and updates that as well.
        edit_page.update_amount(amount_with_tip)
        edit_page.update_expense()

        # Again she sees that has updated...
        edit_page.wait_for_multiple_rows_in_table(
            description,
            amount_with_tip,
            new_expense_date,
            1
        )

        # Satisfied she returns to the home page
        # and see the changes have persisted.
        edit_page.go_to_home_page()
        home_page.wait_for_row_in_list_table(
            description,
            amount_with_tip,
            new_expense_date
        )

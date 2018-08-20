from .base import wait

class Page(object):

    def __init__(self, test):
        self.test = test

class HomePage(Page):

    def go_to_edit_page(self):
        self.test.browser.find_element_by_id('id_edit').click()
        return EditPage(self.test)

    def get_description_input_box(self):
        return self.test.browser.find_element_by_id('id_description')

    def get_amount_input_box(self):
        return self.test.browser.find_element_by_id('id_amount')

    def get_submit_input_button(self):
        return self.test.browser.find_element_by_id('id_submit')

    def get_title(self):
        return self.test.browser.title

    def get_header(self):
        return self.test.browser.find_element_by_tag_name('h1').text

    def get_total_expenses(self):
        return self.test.browser.find_elements_by_id('id_total_expense')

    @wait
    def wait_for_row_in_list_table(self, description, amount, expense_date):
        rows = self.test.browser.find_elements_by_tag_name('td')
        self.test.assertIn(description, [row.text for row in rows])
        self.test.assertIn(f'${amount}', [row.text for row in rows])
        self.test.assertIn(expense_date.strftime('%d-%b-%Y'), [row.text for row in rows])

    # TODO(steve): surely this test can be made more readible!
    @wait
    def wait_for_multiple_rows_in_list_table(self, description, amount,
                                             expense_date, count):
        rows = self.test.browser.find_elements_by_tag_name('td')
        rows_text = [row.text for row in rows]
        self.test.assertEqual(
            len([text for text in rows_text if text == description]),
            count
        )
        self.test.assertEqual(
            len([text for text in rows_text if text == f'${amount}']),
            count
        )
        self.test.assertEqual(
            len([text for text in rows_text if text ==
                 expense_date.strftime('%d-%b-%Y')]),
            count
        )

class EditPage(Page):

    def update_date(self, new_date):
        input_ = self.test.browser.find_element_by_xpath(
            "//input[@name='date']"
        )
        input_.clear()
        input_.send_keys(new_date.strftime('%Y-%m-%d'))

    def update_amount(self, new_amount):
        input_ = self.test.browser.find_element_by_xpath(
            "//input[@name='amount']"
        )
        input_.clear()
        input_.send_keys(new_amount)

    def update_expense(self):
        self.test.browser.find_element_by_id('id_edit_1').click()

    def delete_expense(self, row_index):
        self.test.browser.find_element_by_id(f'id_delete_{row_index}').click()

    def go_to_home_page(self):
        self.test.browser.find_element_by_id('id_home').click()
        return HomePage(self.test)

    @wait
    def wait_for_multiple_rows_in_table(self, description, amount,
                                         expense_date, count):

        input_rows = self.test.browser.find_elements_by_tag_name('input')
        input_values = [input_row.get_attribute('value') for input_row in
                        input_rows]
        self.test.assertEqual(
            len([ value for value in input_values if value == expense_date.strftime('%Y-%m-%d')]),
            count * 2
        )
        self.test.assertEqual(
            len([ value for value in input_values if value == description]),
            count
        )
        self.test.assertEqual(
            len([ value for value in input_values if value == amount]),
            count
        )

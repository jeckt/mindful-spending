from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.common.exceptions import WebDriverException
from selenium import webdriver

import os
import time
from datetime import date

MAX_WAIT = 20

def wait(fn):
    def modified_fn(*args, **kwargs):
        start_time = time.time()
        while True:
            try:
                return fn(*args, **kwargs)
            except (AssertionError, WebDriverException) as e:
                if time.time() - start_time > MAX_WAIT:
                    raise e
                time.sleep(0.5)
    return modified_fn

class FunctionalTest(StaticLiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()
        self.staging_server = os.environ.get('STAGING_SERVER')
        self.expense_date = date.today().strftime('%d-%b-%Y')
        if self.staging_server:
            from .server_tools import reset_database
            self.live_server_url = 'http://' + self.staging_server
            reset_database(self.staging_server)

    def tearDown(self):
        self.browser.quit()
        super().tearDown()

    def get_description_input_box(self):
        return self.browser.find_element_by_id('id_description')

    def get_amount_input_box(self):
        return self.browser.find_element_by_id('id_amount')

    def get_submit_input_button(self):
        return self.browser.find_element_by_id('id_submit')

    @wait
    def wait_for(self, fn):
        return fn()

    @wait
    def wait_for_row_in_list_table(self, description, amount, expense_date):
        rows = self.browser.find_elements_by_tag_name('td')
        self.assertIn(description, [row.text for row in rows])
        self.assertIn(amount, [row.text for row in rows])
        self.assertIn(expense_date, [row.text for row in rows])

    @wait
    def wait_for_multiple_rows_in_edit_table(self, description, amount,
                                             expense_date, count):

        input_rows = self.browser.find_elements_by_tag_name('input')
        input_values = [input_row.get_attribute('value') for input_row in
                        input_rows]
        self.assertEqual(len([ value for value in input_values if value ==
                             expense_date]), count * 2)
        self.assertEqual(len([ value for value in input_values if value ==
                             description]), count)
        self.assertEqual(len([ value for value in input_values if value ==
                             amount]), count)

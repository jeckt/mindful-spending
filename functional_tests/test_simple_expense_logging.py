from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.common.exceptions import WebDriverException
from selenium import webdriver

import time

MAX_WAIT = 20

class NewVistorTest(StaticLiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

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

    @wait
    def wait_for_row_in_list_table(self, description, amount):
        rows = self.browser.find_elements_by_tag_name('td')
        self.assertIn(description, [row.text for row in rows])
        self.assertIn(description, [row.text for row in rows])

    def test_vistor_can_log_expenses_and_view_total(self):
        # Harold hears about a cool new web app that allows
        # him to log expenses. He goes to the homepage to
        # check it out
        self.browser.get(self.live_server_url)

        # He notices the page title and header contains
        # the name of the web app
        self.assertIn('Mindful Spending', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('Mindful Spending', header_text)

        # He sees that there are two input boxes where
        # he is invited to enter a short description
        # of the expense and the amount
        description_box = self.browser.find_element_by_id('id_desc_text')
        self.assertEqual(
            description_box.get_attribute('placeholder'),
            'Enter a short description of the expense'
        )

        amount_box = self.browser.find_element_by_id('id_amount')
        self.assertEqual(
            amount_box.get_attribute('placeholder'),
            '$0.00'
        )

        # Remembering that he bought some smashed avocado for
        # breakfast he decides to put that in to give the app
        # a go.
        description_box.send_keys('Smashed Avo for brekkie')
        amount_box.send_keys("6.50")
        self.browser.find_element_by_id('id_submit').click()

        # After hitting enter, the page refreshes and he
        # can see the smashed avo expense in the log
        self.wait_for_row_in_list_table('Smashed Avo for brekkie',
                                        '$6.50')

        # After entering the breakfast in the app he decides
        # to take a break and grab a coffee with a work friend,
        # where he tells his friend about the cool new app!
        # Coming back from coffee and logs that into the app
        description_box = self.browser.find_element_by_id('id_desc_text')
        description_box.send_keys('Moonbucks Mocha')

        amount_box = self.browser.find_element_by_id('id_amount')
        amount_box.send_keys("2.75")

        self.browser.find_element_by_id('id_submit').click()

        # The page updates and shows both expenses with
        # how much each item cost.
        self.wait_for_row_in_list_table('Smashed Avo for brekkie',
                                        '$6.50')
        self.wait_for_row_in_list_table('Moonbucks Mocha',
                                        '$2.75')

        # It shows him the total amount he has spent. Neat!
        rows = self.browser.find_elements_by_id('id_total_expense')
        self.assertIn('$9.25', [row.text for row in rows])

        # Before getting too carried away - he gets back to work!

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

# TODO(steve): Implement wait decorator when checking
# that expenses have been logged
class NewVistorTest(StaticLiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def test_vistor_can_log_expenses_and_view_total(self):
        # Harold hears about a cool new web app that allows
        # him to log expenses. He goes to the homepage to
        # check it out
        self.browser.get(self.live_server_url)

        # He notices the page title and header contains
        # the name of the web app
        self.assertIn('wallets', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('wallets', header_text)

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
        amount_box.send_keys(Keys.ENTER)

        # After hitting enter, the page refreshes and he
        # can see the smashed avo expense in the log
        rows = self.browser.find_elements_by_tag_name('td')
        self.assertIn('Smashed Avo for brekkie', [row.text for row in rows])
        self.assertIn('6.50', [row.text for row in rows])

        # After entering the breakfast in the app he decides
        # to take a break and grab a coffee with a work friend,
        # where he tells his friend about the cool new app!
        # Coming back from coffee and logs that into the app
        description_box.send_keys('Moonbucks Mocha')
        amount_box.send_keys(2.75)
        amount_box.send_keys(Keys.ENTER)

        # The page updates and shows both expenses with
        # how much each item cost.
        rows = self.browser.find_elements_by_tag_name('td')
        self.assertIn('Smashed Avo for brekkie', [row.text for row in rows])
        self.assertIn('6.50', [row.text for row in rows])
        self.assertIn('Moonbucks Mocha', [row.text for row in rows])
        self.assertIn('2.75', [row.text for row in rows])

        # It shows him the total amount he has spent. Neat!
        rows = self.browser.find_elements_by_tag_name('th')
        self.assertIn('Total', [row.text for row in rows])
        self.assertIn('9.25', [row.text for row in rows])

        # Before getting too carried away - he gets back to work!

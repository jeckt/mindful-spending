
class Page(object):

    def __init__(self, test):
        self.test = test

class HomePage(Page):

    def go_to_edit_page(self):
        self.test.browser.find_element_by_id('id_edit').click()
        return EditPage(self.test)

class EditPage(Page):

    def update_date(self, new_date):
        input_ = self.test.browser.find_element_by_xpath(
            "//input[@name='date']"
        )
        input_.clear()
        input_.send_keys(new_date)

    def update_amount(self, new_amount):
        input_ = self.test.browser.find_element_by_xpath(
            "//input[@name='amount']"
        )
        input_.clear()
        input_.send_keys(new_amount)

    def go_to_home_page(self):
        self.test.browser.find_element_by_id('id_home').click()
        return HomePage(self.test)

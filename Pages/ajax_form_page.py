from playwright.sync_api import expect

class AjaxFormPage:
    def __init__(self, page):
        self.page = page
        self.name_input = page.locator("#title")
        self.comment_input = page.locator("#description")
        self.submit_btn = page.locator("form#ajaxform button[type='submit']")
        self.success_div = page.locator("#submit-control")

    def submit_form(self, name, comment):
        self.name_input.fill(name)
        self.comment_input.fill(comment)
        self.submit_btn.click()

    def assert_submission_message(self, expected_text):
        expect(self.success_div).to_have_text(expected_text)

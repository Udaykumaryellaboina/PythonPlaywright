from Pages.base_page import BasePage

class LoginPage(BasePage):
    def login(self, username, password):
        self.page.fill("#username", username)
        self.page.fill("#password", password)
        self.page.click("#loginButton")

    def is_login_successful(self):
        return self.page.locator("text=Welcome").is_visible()

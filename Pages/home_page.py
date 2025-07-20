class HomePage:
    def __init__(self, page):
        self.page = page

    def click_menu(self, menu_text):
        self.page.get_by_role("link", name=menu_text).click()

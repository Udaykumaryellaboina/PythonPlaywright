from behave import given, when, then
from Pages.login_page import LoginPage
from playwright.sync_api import sync_playwright
from Utils.config import BASE_URL, HEADLESS

@given("the user launches the browser")
def step_launch_browser(context):
    context.playwright = sync_playwright().start()
    context.browser = context.playwright.chromium.launch(headless=HEADLESS)
    context.page = context.browser.new_page()
    context.page.goto(BASE_URL)
    context.login_page = LoginPage(context.page)

@when('the user logs in with username "{username}" and password "{password}"')
def step_login(context, username, password):
    context.login_page.login(username, password)

@then("the user should see a welcome message")
def step_verify_login(context):
    assert context.login_page.is_login_successful()
    context.browser.close()
    context.playwright.stop()

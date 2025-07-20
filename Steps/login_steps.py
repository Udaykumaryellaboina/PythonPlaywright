from behave import given, when, then
from Pages.home_page import HomePage
from Pages.ajax_form_page import AjaxFormPage
from Utils.config import BASE_URL

@given("the user navigates to Url")
def step_navigate_to_url(context):
    context.page.goto(BASE_URL)
    context.home_page = HomePage(context.page)

@when('the user clicks on "{link_text}"')
def step_click_on_menu(context, link_text):
    context.home_page.click_menu(link_text)

@when('the user submits the form with name "{name}" and comment "{comment}"')
def step_fill_ajax_form(context, name, comment):
    context.ajax_form_page = AjaxFormPage(context.page)
    context.ajax_form_page.submit_form(name, comment)

@then('the user should see the message "{expected_text}"')
def step_assert_success_message(context, expected_text):
    context.ajax_form_page.assert_submission_message(expected_text)

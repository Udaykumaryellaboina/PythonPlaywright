import os
import re
import nest_asyncio
import asyncio
from behave import given, when, then
from playwright.async_api import async_playwright

# Allow nested asyncio loops (fix for asyncio.run() error)
nest_asyncio.apply()


# ---------------- API Steps ----------------
@when("user creates the url")
def step_create_url(context):
    context.api_url = "https://jsonplaceholder.typicode.com/users/1"
    print(f"API URL created: {context.api_url}")


@when('user hit "{method}" http request for URL')
def step_hit_http_request(context, method):
    async def run():
        async with async_playwright() as pw:
            context.api_context = await pw.request.new_context()

            if method.upper() == "GET":
                context.api_response = await context.api_context.get(context.api_url)
            else:
                raise Exception(f"Unsupported method: {method}")

            context.response_status = context.api_response.status
            print(f"Response status: {context.response_status}")

    loop = asyncio.get_event_loop()
    loop.run_until_complete(run())


@when('user validates the status as "{expected_status}"')
def step_validate_status(context, expected_status):
    actual = str(getattr(context, "response_status", None))
    assert actual == expected_status, f"Expected {expected_status}, but got {actual}"
    print(f"✅ Status validation passed: {actual}")


@then("user should see status code {expected:d}")
def step_validate_status_code(context, expected):
    actual = getattr(context, "response_status", None)
    assert actual == expected, f"Expected {expected}, but got {actual}"
    print(f"✅ Final status code validation passed: {actual}")
    context.attach(f"Status code is {actual}", "text/plain")


# ---------------- Cleanup ----------------




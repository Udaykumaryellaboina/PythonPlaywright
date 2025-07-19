import os
from playwright.sync_api import sync_playwright

def before_all(context):
    from playwright.sync_api import sync_playwright
    context.debug = os.getenv("DEBUG", "false").lower() == "true"
    context.playwright = sync_playwright().start()
    context.browser = context.playwright.chromium.launch(headless=not context.debug)
    context.context = context.browser.new_context()
    context.page = context.context.new_page()
    print(f"🎯 Playwright launched in {'DEBUG (headful)' if context.debug else 'headless'} mode")

def after_all(context):
    context.page.close()
    context.context.close()
    context.browser.close()
    context.playwright.stop()

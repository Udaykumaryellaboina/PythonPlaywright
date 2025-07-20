import os
import time
from pathlib import Path
from playwright.sync_api import sync_playwright, BrowserContext

def before_all(context):
    context.debug = os.getenv("DEBUG", "false").lower() == "true"
    context.reports_dir = Path("reports")
    context.reports_dir.mkdir(exist_ok=True)

def before_scenario(context, scenario):
    context.playwright = sync_playwright().start()
    context.browser = context.playwright.chromium.launch(headless=not context.debug)
    context.context: BrowserContext = context.browser.new_context()
    context.page = context.context.new_page()

    # Start tracing
    trace_path = context.reports_dir / f"trace_{scenario.name.replace(' ', '_')}.zip"
    context.trace_path = trace_path
    context.context.tracing.start(screenshots=True, snapshots=True, sources=True)

def after_scenario(context, scenario):
    # Stop tracing
    context.context.tracing.stop(path=str(context.trace_path))

    if scenario.status == "failed":
        # Save screenshot
        screenshot_path = context.reports_dir / f"screenshot_{scenario.name.replace(' ', '_')}.png"
        context.page.screenshot(path=str(screenshot_path))

        print(f"❌ Scenario failed. Screenshot saved to {screenshot_path}")
        print(f"📦 Trace saved to {context.trace_path}")
    else:
        # Clean up traces/screenshots if not failed
        if context.trace_path.exists():
            context.trace_path.unlink()

    context.page.close()
    context.context.close()
    context.browser.close()
    context.playwright.stop()

def after_all(context):
    print(f"📁 Reports are available at: {context.reports_dir.absolute()}")

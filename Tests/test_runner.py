import os
import glob
import subprocess
from datetime import datetime
import argparse

# ---------------- Paths ----------------
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
FEATURES_DIR = os.path.join(BASE_DIR, "Features")
REPORTS_DIR = os.path.join(BASE_DIR, "reports")

# ---------------- CLI Arguments ----------------
parser = argparse.ArgumentParser(description="Run Behave tests with debug support.")
parser.add_argument("--tag", help="Tag expression to filter scenarios (run all if omitted)", default=None)
parser.add_argument("--debug", action="store_true", help="Enable debug/headful browser mode")
args = parser.parse_args()

TAG_EXPRESSION = args.tag
DEBUG_MODE = args.debug

# Set environment variable for Playwright headless toggle
os.environ["DEBUG"] = "true" if DEBUG_MODE else "false"

# ---------------- Ensure reports directory ----------------
os.makedirs(REPORTS_DIR, exist_ok=True)

# ---------------- Find feature files ----------------
feature_files = glob.glob(os.path.join(FEATURES_DIR, "*.feature"))
if not feature_files:
    print(f"❌ No .feature files found in {FEATURES_DIR}.")
    exit(1)

if TAG_EXPRESSION:
    print(f"🚀 Running with tag filter: {TAG_EXPRESSION}")
else:
    print("🚀 Running all scenarios (no tag filter).")

print(f"🧪 Found {len(feature_files)} feature file(s).")
print(f"📄 HTML reports will be saved in: {REPORTS_DIR}")

# ---------------- Run features ----------------
for feature_file in feature_files:
    feature_name = os.path.basename(feature_file).replace(".feature", "")
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    html_report = os.path.join(REPORTS_DIR, f"{feature_name}_{timestamp}.html")

    # Only add --tags if provided
    tag_filter = ["--tags", TAG_EXPRESSION] if TAG_EXPRESSION else []

    cmd = [
        "behave",
        feature_file,
        *tag_filter,
        "-f", "behave_html_formatter:HTMLFormatter",
        "-o", html_report
    ]

    print(f"\n▶️ Running: {feature_file}")
    print(f"🛠️ Debug mode: {'ON' if DEBUG_MODE else 'OFF'}")
    result = subprocess.run(cmd, check=False)

    if result.returncode != 0:
        print(f"❌ Feature failed: {feature_file}")
    else:
        print(f"✅ Feature passed: {feature_file}")

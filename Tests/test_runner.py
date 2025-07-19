import os
import glob
import multiprocessing
import argparse
from datetime import datetime

# === PROJECT PATHS ===
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
FEATURES_DIR = os.path.join(BASE_DIR, "features")
REPORTS_DIR = os.path.join(BASE_DIR, "reports")

# === CLI ARGUMENT PARSER ===
parser = argparse.ArgumentParser(description="Run Behave tests with debug support.")
parser.add_argument("--tag", help="Tag expression to filter scenarios", default="@login or @smoke")
parser.add_argument("--debug", action="store_true", help="Enable debug/headful browser mode")
args = parser.parse_args()

TAG_EXPRESSION = args.tag
DEBUG_MODE = args.debug

# Set environment variable for Playwright headless toggle
os.environ["DEBUG"] = "true" if DEBUG_MODE else "false"

def run_feature(feature_file):
    feature_name = os.path.basename(feature_file).replace(".feature", "")
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    html_report = os.path.join(REPORTS_DIR, f"{feature_name}_{timestamp}.html")

    tag_filter = f'--tags="{TAG_EXPRESSION}"' if "@all" not in TAG_EXPRESSION else ""

    cmd = (
        f'cd "{BASE_DIR}" && behave "{feature_file}" {tag_filter} '
        f'-f behave_html_formatter:HTMLFormatter -o "{html_report}"'
    )

    print(f"\n▶️ Running: {feature_file}")
    print(f"🛠️ Debug mode: {'ON' if DEBUG_MODE else 'OFF'}")
    os.system(cmd)

def main():
    os.makedirs(REPORTS_DIR, exist_ok=True)

    feature_files = glob.glob(os.path.join(FEATURES_DIR, "*.feature"))
    if not feature_files:
        print("❌ No .feature files found.")
        return

    print(f"🚀 Running with tag filter: {TAG_EXPRESSION}")
    print(f"🧪 Found {len(feature_files)} feature file(s).")
    print(f"📄 HTML reports will be saved in: {REPORTS_DIR}")

    pool = multiprocessing.Pool(processes=min(4, len(feature_files)))
    pool.map(run_feature, feature_files)
    pool.close()
    pool.join()

    print(f"\n✅ Test execution finished.")

if __name__ == "__main__":
    main()

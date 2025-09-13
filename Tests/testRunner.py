import os
import glob
import argparse
import subprocess

# === PROJECT PATHS ===
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
FEATURES_DIR = (
    os.path.join(BASE_DIR, "Features")
    if os.path.isdir(os.path.join(BASE_DIR, "Features"))
    else os.path.join(BASE_DIR, "features")
)
REPORTS_DIR = os.path.join(BASE_DIR, "reports")

# === CLI ARGUMENT PARSER ===
parser = argparse.ArgumentParser(description="Run Behave tests with debug support.")
parser.add_argument("--tag", help="Tag expression to filter scenarios (run all if omitted)")
parser.add_argument("--debug", action="store_true", help="Enable debug/headful browser mode")
args = parser.parse_args()

TAG_EXPRESSION = args.tag
DEBUG_MODE = args.debug

# Set environment variable for Playwright headless toggle
os.environ["DEBUG"] = "true" if DEBUG_MODE else "false"

def run_behave(features_dir, reports_dir):
    os.makedirs(reports_dir, exist_ok=True)

    if not os.path.isdir(features_dir):
        print(f"❌ Features directory not found: {features_dir}")
        return

    # Discover all feature files
    feature_files = glob.glob(os.path.join(features_dir, "*.feature"))
    if not feature_files:
        print(f"❌ No feature files found in {features_dir}")
        return

    print(f"🚀 Running {len(feature_files)} feature(s) from: {features_dir}")
    print(f"📄 Reports will be saved in: {reports_dir}")

    # Build behave command
    cmd = [
        "behave",
        features_dir,
        "-f", "behave_html_formatter:HTMLFormatter",
        "-o", reports_dir
    ]
    if TAG_EXPRESSION:
        cmd.extend(["--tags", TAG_EXPRESSION])

    # Run Behave
    print(f"▶️ Running command: {' '.join(cmd)}")
    subprocess.run(cmd, check=True)
    print("\n✅ Test execution finished.")

if __name__ == "__main__":
    run_behave(FEATURES_DIR, REPORTS_DIR)
    if TAG_EXPRESSION:
        print(f"🚀 Running with tag filter: {TAG_EXPRESSION}")
    else:
        print("🚀 Running all scenarios (no tag filter).")
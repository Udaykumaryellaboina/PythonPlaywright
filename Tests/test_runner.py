import os
import glob
import multiprocessing

# === SET YOUR TAG EXPRESSION HERE ===
TAG_EXPRESSION = "@login or @smoke"  # Example: "@login and not @skip"

# === PROJECT PATHS ===
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
FEATURES_DIR = os.path.join(BASE_DIR, "features")
REPORTS_DIR = os.path.join(BASE_DIR, "reports")

def run_feature(feature_file):
    feature_name = os.path.basename(feature_file).replace(".feature", "")
    html_report = os.path.join(REPORTS_DIR, f"{feature_name}.html")

    # Handle @all (i.e., no filtering)
    tag_filter = f'--tags="{TAG_EXPRESSION}"' if "@all" not in TAG_EXPRESSION else ""

    # Build behave command with full paths
    cmd = (
        f'cd "{BASE_DIR}" && behave "{feature_file}" {tag_filter} '
        f'-f behave_html_formatter:HTMLFormatter -o "{html_report}"'
    )

    print(f"▶️ Running: {cmd}")
    result = os.system(cmd)
    print(f"⏹ Exit Code: {result}")

def main():
    os.makedirs(REPORTS_DIR, exist_ok=True)

    # 🔍 Discover feature files
    feature_files = glob.glob(os.path.join(FEATURES_DIR, "*.feature"))
    if not feature_files:
        print("❌ No .feature files found.")
        return

    print(f"🚀 Running with tag filter: {TAG_EXPRESSION}")
    print(f"🧪 Found {len(feature_files)} feature file(s).")

    args = feature_files
    pool = multiprocessing.Pool(processes=min(4, len(feature_files)))
    pool.map(run_feature, args)
    pool.close()
    pool.join()

    print(f"\n✅ Test execution finished.")
    print(f"📁 Reports are in: {REPORTS_DIR}")

if __name__ == "__main__":
    main()

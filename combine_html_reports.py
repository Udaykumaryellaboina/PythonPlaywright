import glob
import os

REPORTS_DIR = "reports"
OUTPUT_FILE = os.path.join(REPORTS_DIR, "combined_report.html")

def combine_reports():
    report_files = glob.glob(os.path.join(REPORTS_DIR, "*.html"))
    combined_content = "<html><head><title>Combined Report</title></head><body>"

    for report_file in report_files:
        with open(report_file, "r", encoding="utf-8") as f:
            content = f.read()

            # Strip outer html/body tags to avoid nesting
            body_start = content.find("<body>")
            body_end = content.find("</body>")
            if body_start != -1 and body_end != -1:
                body_content = content[body_start + 6:body_end]
                combined_content += f"<h2>{os.path.basename(report_file)}</h2><hr>{body_content}<br><br>"

    combined_content += "</body></html>"

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(combined_content)

    print(f"✅ Combined report saved to: {OUTPUT_FILE}")

if __name__ == "__main__":
    combine_reports()

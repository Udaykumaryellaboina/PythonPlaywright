import os
import glob
import multiprocessing
import tkinter as tk
from tkinter import ttk, messagebox

# === Project Paths ===
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
FEATURES_DIR = os.path.join(BASE_DIR, "features")
REPORTS_DIR = os.path.join(BASE_DIR, "reports")

# === Tag Options ===
TAGS = ["@login", "@smoke", "@regression", "@all"]

def run_feature_with_tag(args):
    feature_file, tag_expr = args
    feature_name = os.path.basename(feature_file).replace(".feature", "")
    html_report = os.path.join(REPORTS_DIR, f"{feature_name}.html")

    # Tag filtering
    tag_filter = f'--tags="{tag_expr}"' if tag_expr != "@all" else ""
    cmd = (
        f'cd "{BASE_DIR}" && behave "{feature_file}" {tag_filter} '
        f'-f behave_html_formatter:HTMLFormatter -o "{html_report}"'
    )

    print(f"▶️ Running: {cmd}")
    result = os.system(cmd)
    print(f"⏹ Exit Code: {result}")

def run_tests(selected_tag):
    os.makedirs(REPORTS_DIR, exist_ok=True)
    feature_files = glob.glob(os.path.join(FEATURES_DIR, "*.feature"))

    if not feature_files:
        messagebox.showerror("❌ No Feature Files", "No .feature files found.")
        return

    args = [(file, selected_tag) for file in feature_files]
    pool = multiprocessing.Pool(processes=min(4, len(feature_files)))
    pool.map(run_feature_with_tag, args)
    pool.close()
    pool.join()

    messagebox.showinfo("✅ Done", f"Reports generated in: {REPORTS_DIR}")

def start_gui():
    window = tk.Tk()
    window.title("Playwright + Behave Test Runner")

    label = tk.Label(window, text="Select Tag to Run:", font=("Arial", 12))
    label.pack(pady=10)

    selected_tag = tk.StringVar()
    dropdown = ttk.Combobox(window, textvariable=selected_tag, values=TAGS, state="readonly")
    dropdown.pack(pady=5)
    dropdown.set(TAGS[0])

    run_button = tk.Button(
        window, text="Run Tests", bg="green", fg="white",
        font=("Arial", 11), command=lambda: run_tests(selected_tag.get())
    )
    run_button.pack(pady=20)

    window.mainloop()

if __name__ == "__main__":
    start_gui()

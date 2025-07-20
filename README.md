# Playwright BDD Automation Framework

A robust Python automation framework using [Playwright](https://playwright.dev/python/) and [Behave](https://behave.readthedocs.io/en/latest/) for BDD-style browser testing.  
Supports tag-based test execution, parallel runs, HTML reporting, and a Tkinter GUI runner.

---

## 📁 Project Structure

```
.env
behave.ini
combine_html_reports.py
environment.py
requirements.txt
Commands.txt
Features/
  login.feature
Pages/
  base_page.py
  home_page.py
  login_page.py
  ajax_form_page.py
Reports/
Steps/
  login_steps.py
Tests/
  test_runner.py
  test_runner_gui.py
Utils/
  config.py
```

---

## 🚀 Getting Started

### 1. **Install Dependencies**

```sh
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python -m playwright install
```

### 2. **Configure Environment**

Edit `.env` for base URL and headless mode:

```
BASE_URL=https://www.lambdatest.com/selenium-playground/
HEADLESS=true
```

---

## 🧪 Running Tests

### **Command-Line Runner**

Run all tests (default tags):

```sh
python Tests/test_runner.py
```

Run specific tags (e.g., `@login`):

```sh
python Tests/test_runner.py --tag="@login"
```

Enable debug/headful browser:

```sh
python Tests/test_runner.py --debug
```

### **Tkinter GUI Runner**

Launch GUI to select tags and run tests:

```sh
python Tests/test_runner_gui.py
```

---

## 📊 HTML Reporting

- Individual HTML reports per feature in `reports/`.
- Combine all reports:

```sh
python combine_html_reports.py
```

Open combined report:

- Windows: `start reports/combined_report.html`
- macOS/Linux: `open reports/combined_report.html`

---

## 🏷️ Tag Expressions

- Run by tag: `@login`, `@smoke`, etc.
- AND/OR: `@login and @smoke`
- Exclude: `not @skip`
- All: `@all`

---

## 🛠️ Framework Overview

- **Features**: Gherkin `.feature` files (`Features/login.feature`)
- **Steps**: Step definitions (`Steps/login_steps.py`)
- **Pages**: Page Object Model (`Pages/base_page.py`, `Pages/home_page.py`, `Pages/login_page.py`, `Pages/ajax_form_page.py`)
- **Config**: Environment variables (`Utils/config.py`)
- **Test Runner**: CLI (`Tests/test_runner.py`), GUI (`Tests/test_runner_gui.py`)
- **Reporting**: HTML reports (`combine_html_reports.py`)

---

## ⚙️ CI Integration

See `.github/workflows/ci.yml` for automated test runs and report uploads.

---

## 📚 Useful Commands

See `Commands.txt` for quick reference and advanced usage.

---

## 📝 Contributing

1. Fork the repo
2. Create feature branches
3. Submit PRs

---

## 📄 License

MIT

---

## 🙏 Credits

- [Playwright](https://playwright.dev/python/)
- [Behave](https://behave.readthedocs.io/en/latest/)
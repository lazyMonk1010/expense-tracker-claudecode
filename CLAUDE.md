# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

```bash
# Install dependencies
pip install -r requirements.txt

# Run dev server (port 5001, debug mode)
python app.py

# Run tests
pytest

# Run a single test file
pytest tests/test_app.py

# Run a single test by name
pytest tests/test_app.py::test_function_name
```

## Architecture

**Spendly** is a Flask expense tracker targeting Indian users (currency: ₹/INR). It is structured as a teaching project where most backend features are stubs awaiting implementation.

### Stack
- **Backend:** Python/Flask 3.1.3, single-file app (`app.py`)
- **Database:** SQLite via `database/db.py` (not yet wired up — stub only)
- **Frontend:** Jinja2 templates extending `templates/base.html`, single CSS file (`static/css/style.css`), stub JS (`static/js/main.js`)
- **Testing:** pytest + pytest-flask

### Key files
- `app.py` — all routes defined here; currently only landing/legal pages render real content; auth + expense routes return placeholder strings
- `database/db.py` — stub for `get_db()`, `init_db()`, `seed_db()`; the SQLite DB (`expense_tracker.db`) is gitignored and doesn't exist yet
- `static/css/style.css` — complete design system using CSS custom properties; warm paper/ink palette; do not break existing variables

### Current implementation state
| Area | Status |
|---|---|
| Landing page, Terms, Privacy | Complete |
| Login/Register HTML forms | Template only — no POST handlers |
| Session management | Not started |
| Database schema + seed | Stub only |
| Expense CRUD (add/edit/delete) | Route stubs only |

### Intended implementation order
Steps are numbered in comments inside `app.py` and `database/db.py`:
1. DB setup (schema + seed in `database/db.py`, call `init_db()` in `app.py`)
2. Register POST handler
3. Login/Logout with Flask sessions
4. Profile page
5. Expense listing/dashboard
6–9. Add, edit, delete expenses

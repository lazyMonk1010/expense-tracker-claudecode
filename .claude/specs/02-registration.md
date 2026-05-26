# Spec: Registration

## Overview
This feature wires up the POST handler for `/register` so new users can create
a Spendly account. The HTML form already exists in `templates/register.html`;
this step adds the server-side logic: validate input, check for duplicate
emails, hash the password with werkzeug, and insert the new row into the
`users` table. On success the user is redirected to `/login`; on failure the
same form re-renders with an inline error message.

## Depends on
- **Step 01 — Database setup**: `users` table must exist (`init_db()` already
  called in `app.py`).

## Routes
- `POST /register` — validates form data, creates user account — public

The existing `GET /register` route (renders the form) stays unchanged.

## Database changes
No database changes. The `users` table already has all required columns:
`id`, `name`, `email`, `password_hash`, `created_at`.

## Templates
- **Modify:** `templates/register.html`
  - Already contains `{% if error %}` block — no structural changes needed.
  - Optionally repopulate `name` and `email` fields with submitted values on
    validation failure so the user does not have to retype them.

## Files to change
- `app.py` — convert the `register` view into a dual-method route (`GET`,
  `POST`); add POST handler logic.

## Files to create
None.

## New dependencies
No new dependencies. `werkzeug.security` ships with Flask.

## Rules for implementation
- No SQLAlchemy or ORMs — use raw `sqlite3` via `get_db()` from `database/db.py`
- Parameterised queries only — never use f-strings or `%` formatting in SQL
- Passwords hashed with `werkzeug.security.generate_password_hash`
- Use CSS variables — never hardcode hex values
- All templates extend `base.html`
- Validate server-side: name non-empty, valid email format, password ≥ 8 chars
- Return HTTP 409 / re-render form if email already exists (do not leak whether
  the email is registered vs wrong password — keep the message generic:
  "An account with that email already exists.")
- After successful registration, redirect to `/login` with a `?registered=1`
  query param so the login page can show a confirmation banner (the banner
  display is optional in this step but the param should be passed)
- Do not log the user in automatically — that is Step 3 (Login)

## Definition of done
- [ ] `GET /register` still renders the form (no regression)
- [ ] Submitting the form with valid data inserts a row in `users` and
      redirects to `/login`
- [ ] Submitting with an email that already exists re-renders the form with
      an error message and returns HTTP 400
- [ ] Submitting with a password shorter than 8 characters re-renders the
      form with a validation error
- [ ] Submitting with an empty name re-renders the form with a validation error
- [ ] The stored `password_hash` is never the plaintext password
      (verify with `sqlite3 database/expense_tracker.db "SELECT password_hash FROM users LIMIT 1"`)
- [ ] All existing tests pass: `pytest`

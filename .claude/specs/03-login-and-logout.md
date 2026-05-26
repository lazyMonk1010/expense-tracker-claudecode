# Spec: Login and Logout

## Overview
This feature wires up the POST handler for `/login` and the `GET /logout` route so
users can authenticate into Spendly and end their session. The HTML form already
exists in `templates/login.html`; this step adds server-side credential checking
(look up by email, verify the hashed password with werkzeug), Flask session
management, and a `login_required` helper for protecting future routes. On
successful login the user is redirected to `/profile`; on failure the same form
re-renders with a generic error. The nav in `base.html` should also update
conditionally to show "Sign out" when the user is logged in.

## Depends on
- **Step 01 — Database setup**: `users` table must exist with `id`, `email`,
  `password_hash` columns.
- **Step 02 — Registration**: at least one user must exist to test login against.

## Routes
- `POST /login` — validates credentials, sets Flask session, redirects to `/profile` — public
- `GET /logout` — clears Flask session, redirects to `/` — public (works for both logged-in and logged-out)

The existing `GET /login` route (renders the form) stays unchanged except it should
pass `registered=True` to the template when `?registered=1` is present in the query
string.

## Database changes
No database changes. All required columns already exist in the `users` table.

## Templates
- **Modify:** `templates/login.html`
  - Add a success banner: `{% if registered %}` — "Account created! Please sign in."
  - Repopulate the `email` field with the submitted value on validation failure
    so the user does not have to retype it

- **Modify:** `templates/base.html`
  - In the `nav-links` div, conditionally render:
    - When **logged in** (`session.user_id` is set): a "My Profile" link to
      `/profile` and a "Sign out" link to `/logout`
    - When **logged out** (default): the existing "Sign in" and "Get started" links

## Files to change
- `app.py`
  - Add `session` to the `from flask import ...` line
  - Convert the `login` view to handle both `GET` and `POST`
  - Add `POST /login` handler: look up user by email, verify password hash,
    set `session['user_id']` and `session['user_name']`, redirect to `/profile`
  - Implement `GET /logout`: call `session.clear()`, redirect to `url_for('landing')`
  - Add a `login_required` helper function (plain function, not a decorator) that
    checks `session.get('user_id')` and returns a redirect to `/login` if not set;
    future protected routes call this at the top

## Files to create
None.

## New dependencies
No new dependencies. `flask.session` and `werkzeug.security.check_password_hash`
both ship with Flask.

## Rules for implementation
- No SQLAlchemy or ORMs — use raw `sqlite3` via `get_db()` from `database/db.py`
- Parameterised queries only — never use f-strings or `%` formatting in SQL
- Passwords verified with `werkzeug.security.check_password_hash`
- Use CSS variables — never hardcode hex values
- All templates extend `base.html`
- Use a **generic error message** for all credential failures: "Incorrect email or
  password." — never distinguish between "email not found" and "wrong password"
- The `login_required` helper must return a `redirect(url_for('login'))` response
  object (not raise an exception) so callers can do `return login_required() or ...`
- `session.permanent` need not be set; default session lifetime is fine for this step
- Do not store anything sensitive in the session beyond `user_id` and `user_name`

## Definition of done
- [ ] `GET /login` renders the form (no regression)
- [ ] `GET /login?registered=1` shows the "Account created! Please sign in." banner
- [ ] Submitting valid credentials sets a session and redirects to `/profile`
- [ ] Submitting an unknown email re-renders the form with the generic error
- [ ] Submitting a correct email but wrong password re-renders the form with the
      same generic error (no distinction leaked)
- [ ] `GET /logout` clears the session and redirects to `/`; visiting `/logout`
      again (when already logged out) also works without error
- [ ] `base.html` nav shows "Sign out" when logged in and "Sign in"/"Get started"
      when logged out — verify by logging in, refreshing any page, then logging out
- [ ] All existing tests pass: `pytest`

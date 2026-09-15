# MyApp

FastAPI + Jinja2 + HTMX + Tailwind, server-rendered, SQLite-backed. Built for
low/moderate traffic with a photo-gallery-style use case in mind.

## What's here

- **Auth**: signup/login/logout using server-side sessions (opaque token in
  an HttpOnly/Secure/SameSite=Lax cookie, backed by a `sessions` table) —
  not JWT. Logout just deletes the row, no token blocklist to manage.
- **Public vs protected pages**: `/` is public, `/dashboard` is protected —
  see `app/api/dependencies.py` (`get_current_user` vs `require_user`) and
  `app/api/routes/pages.py` for the pattern to copy for new pages.
- **Templates**: `base.html` provides the shared layout; `components/`
  holds reusable Jinja macros (`button`, `card`, `photo_card`) — extend
  these rather than writing one-off markup per page.
- **Database**: SQLite in WAL mode via SQLAlchemy 2.0 async + aiosqlite.
  Good for well beyond 500 users/day of read-heavy traffic at this scale.
- **Styling**: Tailwind, built via the CLI (not the runtime CDN script) —
  see `tailwind.config.js` for the custom design tokens.

## Run it locally

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

cp .env.example .env
# then edit .env and set a real SESSION_SECRET:
python3 -c "import secrets; print(secrets.token_hex(32))"

mkdir -p data media

npm install
npm run build:css        # one-off build; use `npm run watch:css` while developing

uvicorn app.main:app --reload
```

Visit http://127.0.0.1:8000 — sign up, then check `/dashboard`.

## Project layout

```
app/
├── main.py                # FastAPI app, middleware, static/media mounts
├── config.py              # environment-driven settings
├── database.py            # async engine, WAL pragmas, session factory
├── models/user.py         # User, Session ORM models
├── schemas/user.py        # Pydantic request schemas
├── repositories/users.py  # DB access, isolated from business logic
├── services/auth.py       # signup/login/session logic — no HTTP here
├── api/
│   ├── dependencies.py    # get_current_user, require_user, DB session
│   └── routes/
│       ├── pages.py       # public + protected page routes
│       └── auth.py        # signup/login/logout routes
├── templates/
│   ├── base.html
│   ├── components/        # navbar.html, button.html, card.html
│   └── pages/             # home, login, signup, dashboard
└── static/css/            # input.css (source) + output.css (built, gitignored)
```

## Adding a new protected page

```python
# app/api/routes/pages.py
@router.get("/gallery")
async def gallery(request: Request, user: User = Depends(require_user)):
    return templates.TemplateResponse(
        request=request, name="pages/gallery.html", context={"user": user}
    )
```

```html
{# app/templates/pages/gallery.html #}
{% extends "base.html" %}
{% from "components/card.html" import photo_card %}
{% block content %}
  <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
    {% for photo in photos %}
      {{ photo_card(photo.id, photo.thumb_url, photo.caption) }}
    {% endfor %}
  </div>
{% endblock %}
```

That's the whole pattern — `require_user` handles the redirect-to-login for
you, `base.html` handles the shared shell, `photo_card` handles the
repeated markup.

## Deploying (no Docker)

1. Clone the repo onto the VM, create a venv, `pip install -r
   requirements.txt`, `npm install && npm run build:css`.
2. Copy `deploy/myapp.service` to `/etc/systemd/system/`, adjust the
   paths/user, then:
   ```bash
   sudo systemctl daemon-reload
   sudo systemctl enable --now myapp
   ```
3. Copy `deploy/nginx.conf.example` to `/etc/nginx/sites-available/`,
   adjust the domain and paths, symlink into `sites-enabled/`, reload nginx.
   It serves `/static` and `/media` directly (not through Python) and
   proxies everything else to Uvicorn on `127.0.0.1:8000`.
4. Set up `deploy/backup_db.sh` on a daily cron — see the comment at the
   top of that script for the crontab line.
5. Redeploys: `git pull`, reinstall deps if changed, `npm run build:css`
   if templates/CSS changed, `sudo systemctl restart myapp`.

## Notes on things you'll build next

- **Uploads**: add a `photos` table, a repository, and a service that uses
  Pillow to generate 2-3 sizes (thumbnail/medium/full) on upload. Serve
  thumbnails in grids, full-size only on click-through. Store files under
  `media/{user_id}/{photo_id}/{size}.jpg` and let Nginx serve them
  directly — don't route image bytes through FastAPI.
- **Infinite scroll**: HTMX pattern is a sentinel element with
  `hx-trigger="revealed"` at the end of the grid, `hx-get` for the next
  page, `hx-swap="afterend"` (or `beforeend` on the grid container).
- **Migrations**: `init_models()` in `app/database.py` just does
  `create_all`, which is fine for schema-doesn't-change-often. If you find
  yourself editing models frequently once there's real data, switch to
  Alembic.

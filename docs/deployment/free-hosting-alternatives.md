# Free Cloud Hosting Alternatives for AI Job Hunt

> **Why this guide exists:** Heroku's free tier was discontinued in November 2022 and now requires a verified credit card even for the cheapest plan. This guide covers student-friendly, **no-credit-card-required** alternatives that work well with the GitHub Student Developer Pack.

---

## Table of Contents

1. [Quick Comparison](#1-quick-comparison)
2. [Railway](#2-railway)
3. [Render](#3-render)
4. [PythonAnywhere](#4-pythonanywhere)
5. [Supabase (PostgreSQL only)](#5-supabase-postgresql-only)
6. [Neon (PostgreSQL only)](#6-neon-postgresql-only)
7. [Recommended Setup for Students](#7-recommended-setup-for-students)
8. [Migrating from Heroku](#8-migrating-from-heroku)
9. [Environment Variables Reference](#9-environment-variables-reference)

---

## 1. Quick Comparison

| Platform | Free Tier | GitHub Student Pack | PostgreSQL | Credit Card Required | Best For |
|---|---|---|---|---|---|
| **Railway** | $5/month credit (GitHub Student Pack) | ✅ Yes — extra $5/month | ✅ Built-in plugin | ❌ No (with Student Pack) | Full-stack Flask + PostgreSQL |
| **Render** | 750 hrs/month free web service | ✅ Yes | ✅ 90-day free DB | ❌ No | Simple one-click deploys |
| **PythonAnywhere** | Always-on free Python hosting | ✅ Yes — student discount | ⚠️ MySQL on free tier | ❌ No | Pure Python/Flask hosting |
| **Supabase** | 2 free projects, 500 MB DB | ✅ Yes | ✅ Hosted PostgreSQL | ❌ No | Managed PostgreSQL + extras |
| **Neon** | 0.5 GB storage free | ✅ Yes | ✅ Serverless PostgreSQL | ❌ No | Lightweight PostgreSQL |

---

## 2. Railway

**Website:** https://railway.app  
**GitHub Student Pack benefit:** $5/month in free credits (on top of the free $5 monthly allowance = $10/month total). No credit card required when signing up with GitHub.

### What you get
- Native **PostgreSQL plugin** — one click to add a database to your project
- Automatic deploys from GitHub (push to deploy)
- Custom domains on all plans
- Environment variables via dashboard or CLI
- Auto-scaling and sleep prevention (unlike Render free tier)

### Pros
- ✅ No credit card needed when linked to GitHub Student Pack
- ✅ PostgreSQL plugin is trivially easy to provision
- ✅ The existing `Procfile` is respected — zero config needed
- ✅ Scales well beyond the student period
- ✅ Active community + good docs

### Cons
- ❌ Credits run out if the app is resource-heavy (monitor usage)
- ❌ Free credits expire at month end (don't roll over)
- ❌ Compute is shared

### Deployment Steps

1. **Sign up** at https://railway.app using "Login with GitHub" — link to your `.edu` or GitHub Student Pack account.

2. **Create a new project:**
   ```
   railway new
   ```
   Or use the dashboard → "New Project" → "Deploy from GitHub Repo".

3. **Add a PostgreSQL database:**
   - Dashboard → your project → "New Service" → "Database" → "Add PostgreSQL"
   - Railway auto-sets `DATABASE_URL` in your service's environment.

4. **Set environment variables** in the Railway dashboard (Settings → Variables):
   ```
   JWT_SECRET_KEY=<your-secret>
   FLASK_ENV=production
   CORS_ORIGINS=https://your-frontend-url.com
   ```

5. **Deploy:**  
   Railway reads the existing `Procfile` at the repo root:
   ```
   web: gunicorn --chdir backend wsgi:app --log-file -
   ```
   Push to your connected GitHub branch — Railway deploys automatically.

6. **Run database migrations** (if using Flask-Migrate):
   ```bash
   railway run flask db upgrade
   ```

**Configuration file:** See [`deploy/railway/railway.toml`](../../deploy/railway/railway.toml)

---

## 3. Render

**Website:** https://render.com  
**GitHub Student Pack benefit:** Included in GitHub Student Pack — check https://education.github.com/pack for current offer. No credit card required for the free tier.

### What you get
- **Free Web Service:** 750 hours/month (enough for one always-on app)
- **Free PostgreSQL:** 90 days, then the instance is suspended (but data stays — you reactivate or export)
- Auto-deploy on GitHub push
- Free TLS/SSL certificates
- Custom domains

### Pros
- ✅ Generous free tier — no credit card needed at all
- ✅ `render.yaml` lets you define the entire stack (web + DB) in one file
- ✅ Zero-downtime deploys
- ✅ PostgreSQL included in the free tier (90 days active)

### Cons
- ❌ Free web services **sleep after 15 minutes of inactivity** (cold-start ~30 sec)
- ❌ Free PostgreSQL suspended after 90 days of inactivity
- ❌ 512 MB RAM on the free plan
- ❌ No persistent disk on the free plan

### Deployment Steps

1. **Sign up** at https://render.com with GitHub OAuth.

2. **Use the `render.yaml` Blueprint** (already in this repo at `deploy/render/render.yaml`):
   - Dashboard → "New" → "Blueprint" → select your GitHub repo.
   - Render reads `render.yaml` and creates both the web service and the PostgreSQL database automatically.

3. **Or create services manually:**
   - "New Web Service" → connect GitHub repo.
   - Build command: `pip install -r backend/requirements.txt`
   - Start command: `gunicorn --chdir backend wsgi:app --log-file -`
   - Add a "New PostgreSQL" database and copy the `DATABASE_URL`.

4. **Set environment variables** under the web service → "Environment":
   ```
   DATABASE_URL=<copied from Render PostgreSQL>
   JWT_SECRET_KEY=<your-secret>
   FLASK_ENV=production
   CORS_ORIGINS=https://your-frontend.onrender.com
   ```

5. **Deploy:** Push to your connected branch.

**Configuration file:** See [`deploy/render/render.yaml`](../../deploy/render/render.yaml)

---

## 4. PythonAnywhere

**Website:** https://www.pythonanywhere.com  
**GitHub Student Pack benefit:** Discounted paid plans (check https://education.github.com/pack). The **free tier is always available** without credit card.

### What you get (free tier)
- One web app (your Flask app)
- Python 3.x support
- 512 MB disk
- MySQL database (PostgreSQL is **paid only**)
- A public URL at `<username>.pythonanywhere.com`
- Always-on (no sleeping)

### Pros
- ✅ **Always-on** — no sleep on free tier
- ✅ No credit card ever required
- ✅ Good for pure Python/Flask apps
- ✅ Beginner-friendly dashboard and tutorials
- ✅ Console access in browser

### Cons
- ❌ **PostgreSQL is NOT available on the free tier** (MySQL only — requires app changes)
- ❌ Limited outbound network access on free tier (whitelisted domains only)
- ❌ Slower deployments (manual Git pull in their console)
- ❌ No auto-deploy on push
- ❌ 512 MB disk limit

### Deployment Steps

> **Note:** Because the free tier only provides MySQL, you have two options:
> - Option A: Use **MySQL** (requires changing `DATABASE_URL` to a `mysql://` URI and adding `PyMySQL` to requirements).
> - Option B: Pair PythonAnywhere with **Supabase** or **Neon** for a free external PostgreSQL (recommended).

1. **Sign up** at https://www.pythonanywhere.com (free Beginner account).

2. **Upload your code** via the "Files" tab, or clone from GitHub in a Bash console:
   ```bash
   git clone https://github.com/<your-username>/ai-job-hunt.git
   ```

3. **Create a virtual environment:**
   ```bash
   cd ai-job-hunt
   python -m venv venv
   source venv/bin/activate
   pip install -r backend/requirements.txt
   ```

4. **Configure the web app:**
   - "Web" tab → "Add a new web app" → Manual configuration → Python 3.x
   - **Source code:** `/home/<username>/ai-job-hunt`
   - **Virtualenv:** `/home/<username>/ai-job-hunt/venv`
   - **WSGI file:** Edit the auto-generated WSGI file to point to `backend/wsgi.py`:
     ```python
     import sys
     import os
     path = '/home/<username>/ai-job-hunt/backend'
     if path not in sys.path:
         sys.path.insert(0, path)
     os.environ['DATABASE_URL'] = 'postgresql://...'  # from Supabase or Neon
     os.environ['JWT_SECRET_KEY'] = '<your-secret>'
     os.environ['FLASK_ENV'] = 'production'
     from wsgi import app as application
     ```

5. **Reload** the web app from the "Web" tab after every code change.

**Notes file:** See [`deploy/pythonanywhere/setup_notes.md`](../../deploy/pythonanywhere/setup_notes.md)

---

## 5. Supabase (PostgreSQL only)

**Website:** https://supabase.com  
**GitHub Student Pack benefit:** Included in the Student Pack. Free tier available to everyone.

Supabase is a hosted PostgreSQL service (plus auth, storage, and more). Use it as the **database backend** alongside any of the hosting platforms above.

### What you get (free tier)
- 2 free projects
- 500 MB database storage
- 2 GB file storage
- 50,000 monthly active users (auth)
- Unlimited API requests
- **Full PostgreSQL** with connection string

### Pros
- ✅ Full PostgreSQL — drop-in replacement for Heroku Postgres
- ✅ No credit card required
- ✅ Direct connection string works with `DATABASE_URL`
- ✅ Includes a GUI table editor, SQL editor, and real-time features
- ✅ Projects are **paused after 1 week of inactivity** on the free tier but **data is preserved** — just reactivate

### Cons
- ❌ Projects pause after 1 week inactivity (free tier)
- ❌ 500 MB storage limit
- ❌ Direct connections are pooled (use the `?pgbouncer=true` connection string for production)

### Setup Steps

1. Sign up at https://supabase.com with GitHub OAuth.
2. "New Project" → choose region → set a database password.
3. Go to **Settings → Database → Connection String** → copy the `URI` string.
4. Use this as your `DATABASE_URL` environment variable:
   ```
   DATABASE_URL=postgresql://postgres:<password>@db.<project-ref>.supabase.co:5432/postgres
   ```
5. The app's `db.create_all()` will create all tables on first run.

---

## 6. Neon (PostgreSQL only)

**Website:** https://neon.tech  
**GitHub Student Pack benefit:** Included in Student Pack.

Neon is a serverless PostgreSQL provider with a generous free tier and no credit card required.

### What you get (free tier)
- 1 project, 1 branch
- 0.5 GB storage
- Always-on (no pausing unlike Supabase)
- Connection pooling included

### Pros
- ✅ Full PostgreSQL
- ✅ No credit card required
- ✅ **Does not pause** (unlike Supabase free tier)
- ✅ Branching feature useful for dev/staging/prod workflows
- ✅ Works seamlessly with `DATABASE_URL`

### Cons
- ❌ 0.5 GB storage (less than Supabase)
- ❌ 1 project limit on free tier
- ❌ Relatively newer service

### Setup Steps

1. Sign up at https://neon.tech with GitHub OAuth.
2. Create a new project → choose a region.
3. Copy the connection string from the dashboard.
4. Update your `DATABASE_URL`:
   ```
   DATABASE_URL=postgresql://<user>:<password>@<endpoint>.neon.tech/<dbname>?sslmode=require
   ```

---

## 7. Recommended Setup for Students

### Best overall (no credit card, easiest):

```
Flask App Hosting  →  Railway (GitHub Student Pack)
PostgreSQL         →  Railway built-in PostgreSQL plugin
```

**Why:** Railway's Student Pack gives you $10/month in credits, has a PostgreSQL plugin that auto-injects `DATABASE_URL`, and respects the existing `Procfile` with zero extra config.

### Best fallback (Render + Supabase):

```
Flask App Hosting  →  Render (free web service)
PostgreSQL         →  Supabase (free PostgreSQL)
```

**Why:** Both are completely free with no credit card. The 15-minute sleep on Render can be mitigated by using a free uptime monitor like UptimeRobot to ping the app every 10 minutes.

### Best if you need always-on (no sleep):

```
Flask App Hosting  →  PythonAnywhere (free always-on)
PostgreSQL         →  Neon (serverless, doesn't pause)
```

---

## 8. Migrating from Heroku

### Step 1 — Export your Heroku PostgreSQL data

```bash
# Create a dump of your Heroku Postgres database
heroku pg:backups:capture --app <your-heroku-app>
heroku pg:backups:download --app <your-heroku-app>
# This creates a `latest.dump` file
```

### Step 2 — Import into your new PostgreSQL provider

```bash
# Using pg_restore (for Railway / Render / Supabase / Neon)
pg_restore --verbose --clean --no-acl --no-owner \
  -h <new-db-host> \
  -U <new-db-user> \
  -d <new-db-name> \
  latest.dump
```

Or use the provider's dashboard import tool (Supabase and Render both have UI importers).

### Step 3 — Update environment variables

Replace all Heroku Config Vars in your new platform's dashboard:

| Heroku Config Var | New Platform Variable |
|---|---|
| `DATABASE_URL` | Provided by the new PostgreSQL service |
| `JWT_SECRET_KEY` | Set manually |
| `FLASK_ENV` | Set to `production` |
| `CORS_ORIGINS` | Update to new frontend URL |

### Step 4 — Update `DATABASE_URL` prefix (if needed)

SQLAlchemy 1.4+ requires `postgresql://` instead of `postgres://`. The app already handles this, but double-check your connection string from the new provider. If it starts with `postgres://`, update it to `postgresql://`.

### Step 5 — Remove Heroku-specific files (optional)

The `Procfile` at the repo root is **compatible with Railway** and can stay. No changes are needed for Railway or Render.

### Step 6 — Update DNS / custom domain

If you have a custom domain pointing to `<app>.herokuapp.com`, update your DNS `CNAME` to the new platform's domain.

---

## 9. Environment Variables Reference

All platforms above support setting environment variables via their dashboard or CLI. Here is the full list used by this app:

| Variable | Required | Description | Example |
|---|---|---|---|
| `DATABASE_URL` | ✅ Yes | PostgreSQL connection URI | `postgresql://user:pass@host:5432/dbname` |
| `JWT_SECRET_KEY` | ✅ Yes | Secret key for JWT signing — **use a long random string in production** | `openssl rand -hex 32` |
| `FLASK_ENV` | Recommended | `production` disables debug mode | `production` |
| `JWT_ACCESS_TOKEN_EXPIRES` | Optional | Token expiry in seconds (default: 3600) | `3600` |
| `CORS_ORIGINS` | Recommended | Comma-separated allowed origins | `https://yourapp.onrender.com` |

> **Security tip:** Never commit `.env` files to Git. Use each platform's secret/environment variable management feature instead.

---

*Last updated: March 2026*

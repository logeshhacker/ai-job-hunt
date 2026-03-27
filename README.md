# AI Job Hunt

An AI-powered job hunting web application built with Flask (Python) and PostgreSQL.

## Project Structure

```
ai-job-hunt/
├── backend/             # Flask application
│   ├── app/             # Application package
│   │   ├── __init__.py  # App factory (SQLAlchemy, JWT, CORS)
│   │   ├── agents/      # AI agent modules
│   │   ├── models/      # SQLAlchemy models
│   │   ├── routes/      # Flask blueprints
│   │   └── wsgi.py      # WSGI entry point
│   ├── requirements.txt # Python dependencies
│   └── wsgi.py          # Root WSGI entry for gunicorn
├── deploy/              # Platform-specific deployment configs
│   ├── railway/         # Railway.app config
│   ├── render/          # Render.com Blueprint
│   └── pythonanywhere/  # PythonAnywhere setup notes
├── docs/
│   └── deployment/
│       └── free-hosting-alternatives.md  # ← Hosting guide for students
└── Procfile             # Gunicorn start command (used by Railway)
```

## Deployment

> **Heroku requires a credit card.** If you are a student using the GitHub Student Developer Pack, see the guide below for free alternatives that require no credit card.

### 📖 [Free Hosting Alternatives Guide](docs/deployment/free-hosting-alternatives.md)

Covers:
- **Railway** — Recommended. $10/month in free credits with the GitHub Student Pack. Built-in PostgreSQL plugin.
- **Render** — Free web service + free PostgreSQL (90-day active period). No credit card needed.
- **PythonAnywhere** — Always-on free Python hosting. Pair with Supabase or Neon for PostgreSQL.
- **Supabase** — Free managed PostgreSQL. No credit card. Included in the Student Pack.
- **Neon** — Free serverless PostgreSQL. No credit card. Never pauses.

Each platform section includes step-by-step deployment instructions, pros/cons, and migration steps from Heroku.

## Quick Start (Local Development)

```bash
# Clone the repo
git clone https://github.com/<your-username>/ai-job-hunt.git
cd ai-job-hunt

# Create a virtual environment
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r backend/requirements.txt

# Set environment variables
export DATABASE_URL="sqlite:///app.db"   # SQLite for local dev
export JWT_SECRET_KEY="dev-secret-key"
export FLASK_ENV="development"

# Run the app
gunicorn --chdir backend wsgi:app --log-file -
```

The API will be available at `http://localhost:8000`.

## Environment Variables

| Variable | Required | Description |
|---|---|---|
| `DATABASE_URL` | ✅ | PostgreSQL (or SQLite) connection URI |
| `JWT_SECRET_KEY` | ✅ | Secret key for JWT signing |
| `FLASK_ENV` | Recommended | `development` or `production` |
| `JWT_ACCESS_TOKEN_EXPIRES` | Optional | Token expiry in seconds (default: 3600) |
| `CORS_ORIGINS` | Recommended | Comma-separated allowed origins |

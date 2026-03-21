# PythonAnywhere Deployment Notes

PythonAnywhere offers a free, always-on Python/Flask hosting tier that requires no credit card.
The free tier does **not** include PostgreSQL (MySQL only), so this setup pairs PythonAnywhere
with an external free PostgreSQL provider (Supabase or Neon).

See the full guide at `docs/deployment/free-hosting-alternatives.md` for context and alternatives.

---

## Prerequisites

- A PythonAnywhere free account: https://www.pythonanywhere.com/registration/register/beginner/
- A free PostgreSQL connection string from either:
  - **Supabase:** https://supabase.com  (free, no credit card)
  - **Neon:** https://neon.tech        (free, no credit card, no pausing)

---

## Step-by-Step Setup

### 1. Clone the repository

Open a Bash console on PythonAnywhere (Dashboard → "New console" → "Bash"):

```bash
git clone https://github.com/<your-username>/ai-job-hunt.git ~/ai-job-hunt
```

### 2. Create a virtual environment

```bash
cd ~/ai-job-hunt
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r backend/requirements.txt
```

### 3. Configure the web app

- Go to the **Web** tab → "Add a new web app"
- Choose "Manual configuration" → Python 3.x (latest available)
- Set **Source code** to `/home/<username>/ai-job-hunt`
- Set **Virtualenv** to `/home/<username>/ai-job-hunt/venv`

### 4. Edit the WSGI configuration file

PythonAnywhere generates a WSGI file at `/var/www/<username>_pythonanywhere_com_wsgi.py`.
Click the link in the Web tab to edit it. Replace the entire contents with:

```python
import sys
import os

# Add the backend directory to the Python path
path = '/home/<username>/ai-job-hunt/backend'
if path not in sys.path:
    sys.path.insert(0, path)

# Set environment variables
os.environ['DATABASE_URL'] = 'postgresql://<user>:<password>@<host>/<dbname>?sslmode=require'
os.environ['JWT_SECRET_KEY'] = '<your-long-random-secret>'
os.environ['FLASK_ENV'] = 'production'
os.environ['CORS_ORIGINS'] = 'https://<username>.pythonanywhere.com'

# Import the Flask app
from wsgi import app as application  # noqa
```

Replace `<username>`, `<user>`, `<password>`, `<host>`, `<dbname>`, and `<your-long-random-secret>`
with your actual values.

### 5. Reload the web app

Click the green **"Reload"** button on the Web tab. Your app will be live at:
```
https://<username>.pythonanywhere.com
```

### 6. Updating the app

After pushing changes to GitHub, pull them in a PythonAnywhere Bash console:

```bash
cd ~/ai-job-hunt
git pull
source venv/bin/activate
pip install -r backend/requirements.txt  # if requirements changed
```

Then click **"Reload"** on the Web tab.

---

## Limitations on the Free Tier

| Limitation | Detail |
|---|---|
| PostgreSQL | Not available — use Supabase or Neon externally |
| Outbound network | Only whitelisted domains (covers Supabase and Neon) |
| CPU seconds | 100 CPU-seconds/day |
| Disk | 512 MB |
| Custom domains | Paid only |
| HTTPS | Free on `<username>.pythonanywhere.com` |
| Always-on | ✅ Yes — no sleeping unlike Render free tier |

---

## Generating a JWT_SECRET_KEY

Run this in any terminal (or in a PythonAnywhere Bash console):

```bash
python3 -c "import secrets; print(secrets.token_hex(32))"
```

Copy the output and use it as your `JWT_SECRET_KEY`.

# 🌊 DigitalOcean Deployment Guide for Students
## AI Job Hunt — Flask + PostgreSQL on DigitalOcean (Free with GitHub Student Pack)

> **Who is this for?** Complete beginners. Every step is written out — nothing is skipped or assumed.  
> **Cost:** $0 — covered by your GitHub Student Developer Pack ($200 DigitalOcean credit as of 2026).

---

## 📋 Table of Contents

1. [Redeem Your DigitalOcean Credits (Student Pack)](#part-1-redeem-your-digitalocean-credits)
2. [Create Your First Droplet (Virtual Server)](#part-2-create-your-first-droplet)
3. [Connect to Your Droplet via Terminal (SSH)](#part-3-connect-via-terminal-ssh)
4. [Deploy Flask + PostgreSQL on DigitalOcean](#part-4-deploy-flask--postgresql)
5. [One-Click Apps & Marketplace Tips](#part-5-one-click-apps--marketplace-tips)
6. [Troubleshooting](#part-6-troubleshooting)

---

## PART 1: Redeem Your DigitalOcean Credits

### Step 1.1 — Visit the GitHub Student Developer Pack

```
1. Open your browser
2. Go to: https://education.github.com/pack
3. Sign in with your GitHub student account
4. Look for "DigitalOcean" in the list of benefits
```

**What you'll see:**
```
┌──────────────────────────────────────────────────┐
│  DigitalOcean                                    │
│  $200 in platform credit for 1 year              │
│  [Get access] ← CLICK THIS BUTTON               │
└──────────────────────────────────────────────────┘
```

---

### Step 1.2 — Click "Get Access"

```
1. Click the "Get access" or "Get the offer" button next to DigitalOcean
2. You will be redirected to the DigitalOcean website
3. A special student offer URL opens (do NOT close this tab)
```

---

### Step 1.3 — Create a DigitalOcean Account

```
On the DigitalOcean signup page:

1. Click "Sign up with GitHub" (easiest option for students)
   OR
   Enter your email address and create a password

2. Verify your email address:
   - Check your inbox for a verification email from DigitalOcean
   - Click the confirmation link in the email

3. Return to the DigitalOcean dashboard
```

> ⚠️ **Important:** Use the same GitHub account that has the Student Pack activated.

---

### Step 1.4 — Add a Payment Method (Required for Verification Only)

DigitalOcean requires a payment method to verify you're a real person.

```
What to know:
├─ Your card will NOT be charged while credits last
├─ $200 credits will be applied immediately after this step
├─ Keep enough balance to cover any overage (credits last 1 year)
└─ You control spending limits

Steps:
1. Click "Add a credit card" or "Verify with PayPal"
2. Enter your card details (or PayPal login)
3. DigitalOcean charges $1.00 to verify (refunded immediately)
4. After verification, you'll see your credit balance applied
```

> 💡 **Tip:** If you are a student in India or another country where international cards are hard to get, use a virtual Visa/Mastercard (from apps like Wise, or ask a family member).

---

### Step 1.5 — Apply the Student Credit

```
After account creation, the student credits apply automatically if:
├─ You signed up via the GitHub Student Pack link
└─ Your GitHub account is verified as a student

To confirm credits were applied:
1. Go to: https://cloud.digitalocean.com/account/billing
2. Look for "Credits" section
3. You should see: "$200.00 credit remaining"
```

**Billing page confirmation:**
```
┌──────────────────────────────────────────┐
│  Billing                                 │
├──────────────────────────────────────────┤
│  Credits                                 │
│  $200.00 remaining ✅                   │
│  Expires: [1 year from signup]           │
│                                          │
│  Payment Method: Visa ending in XXXX     │
└──────────────────────────────────────────┘
```

🎉 **Credits are redeemed! You're ready to create your server.**

---

## PART 2: Create Your First Droplet

A **Droplet** is DigitalOcean's name for a virtual server (like a computer in the cloud).

### Step 2.1 — Go to Droplets

```
1. Log in to: https://cloud.digitalocean.com
2. Click "Create" button (top navigation bar)
3. Select "Droplets" from the dropdown menu
```

---

### Step 2.2 — Choose a Region

```
1. Select the region closest to your users or to you
2. Recommended for India: Bangalore (BLR1)
3. Recommended for US: New York or San Francisco
4. Any region works — pick the nearest one
```

---

### Step 2.3 — Choose an Image (Operating System)

```
1. Under "Choose an image", select:
   ├─ "Ubuntu" tab
   └─ Version: Ubuntu 24.04 (LTS) x64  ← RECOMMENDED

Why Ubuntu?
├─ Most documentation uses Ubuntu
├─ Beginner-friendly
└─ Widest community support
```

---

### Step 2.4 — Choose a Plan (Size)

```
For a student project (Flask + PostgreSQL):

Select: "Basic" plan
Select: "Regular" CPU
Select: $6/month Droplet

Specs:
├─ 1 vCPU
├─ 1 GB RAM
├─ 25 GB SSD
└─ 1 TB Transfer

With your $200 credit, this runs for:
└─ 200 / 6 = 33 months (well beyond your project!)
```

> ✅ **Your $200 credit will cover this entire project and more.**

---

### Step 2.5 — Set Up Authentication (SSH Key or Password)

**Option A: Password (Easiest for Beginners)**

```
1. Select "Password" under "Authentication"
2. Enter a strong root password (save this somewhere safe!)
3. Example: MyApp@2026!  (must have uppercase, number, symbol)
```

**Option B: SSH Key (More Secure — Recommended)**

```
1. Select "SSH Key" under "Authentication"
2. Click "New SSH Key"
3. Follow Part 3.1 below to generate your key first
4. Paste your public key and give it a name
```

---

### Step 2.6 — Name Your Droplet and Create

```
1. Scroll down to "Finalize and create"
2. Under "Hostname", enter: ai-job-hunt-server
3. Click the green "Create Droplet" button
4. Wait 30-60 seconds for the Droplet to be created
```

**After creation:**
```
┌─────────────────────────────────────────┐
│  ai-job-hunt-server                     │
│  Status: Active ✅                     │
│  IP Address: 123.456.789.000 ← NOTE THIS│
│  Region: Bangalore                      │
│  Size: 1 GB / 1 CPU                    │
└─────────────────────────────────────────┘
```

> 📝 **Write down your IP Address — you need it in the next step.**

---

## PART 3: Connect via Terminal (SSH)

SSH (Secure Shell) lets you control your server from your computer's terminal/command prompt.

### Step 3.1 — Generate an SSH Key (If You Haven't Already)

**On Windows (using PowerShell or Git Bash):**

```powershell
# Open PowerShell (search "PowerShell" in Start menu)
# Type this command and press Enter:

ssh-keygen -t ed25519 -C "your-email@example.com"

# When it asks:
# "Enter file in which to save the key"
# → Press Enter to use default location

# "Enter passphrase"
# → Press Enter (no passphrase, easier for beginners)
# → Press Enter again to confirm

# Result:
# Your key is saved to: C:\Users\YourName\.ssh\id_ed25519
```

**On Mac or Linux (using Terminal):**

```bash
# Open Terminal
# Type this command and press Enter:

ssh-keygen -t ed25519 -C "your-email@example.com"

# Press Enter 3 times (accept defaults, no passphrase)

# Result:
# Your key is saved to: /home/yourname/.ssh/id_ed25519
```

---

### Step 3.2 — View Your Public Key

```bash
# On Windows (PowerShell):
type C:\Users\YourName\.ssh\id_ed25519.pub

# On Mac/Linux (Terminal):
cat ~/.ssh/id_ed25519.pub

# You will see output like this:
# ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAA... your-email@example.com
# ↑ Copy this entire line — you'll paste it in DigitalOcean
```

---

### Step 3.3 — Add Your SSH Key to DigitalOcean

```
1. Go to: https://cloud.digitalocean.com/account/security
2. Click "Add SSH Key"
3. Paste your public key (the long text from Step 3.2)
4. Give it a name (e.g., "My Laptop")
5. Click "Add SSH Key"
```

---

### Step 3.4 — Connect to Your Droplet

Now you can connect to your server from any terminal.

**Replace `YOUR_DROPLET_IP` with the IP address from Step 2.6:**

```bash
# On Windows (PowerShell), Mac, or Linux (Terminal):

ssh root@YOUR_DROPLET_IP

# Example:
ssh root@123.456.789.000

# First time connecting, you'll see:
# "Are you sure you want to continue connecting? (yes/no)"
# Type: yes
# Press Enter

# You are now inside your DigitalOcean server! ✅
```

**If you used a password (not SSH key):**

```bash
ssh root@YOUR_DROPLET_IP

# Enter the root password you set in Step 2.5
# You will NOT see characters as you type — this is normal
# Press Enter after typing your password
```

**What success looks like:**

```
The authenticity of host '123.456.789.000' can't be established.
ED25519 key fingerprint is SHA256:xxxxxxxxxxxxxxxxxxxx.
Are you sure you want to continue connecting (yes/no)? yes

Warning: Permanently added '123.456.789.000' to known hosts.

Welcome to Ubuntu 24.04.1 LTS (GNU/Linux 6.8.0 amd64)

root@ai-job-hunt-server:~# ← YOU ARE NOW ON YOUR SERVER!
```

> 🎉 **You are now connected to your virtual server!** Every command you type now runs on the server, not your laptop.

---

### Step 3.5 — Basic Server Navigation

```bash
# Show current directory (you'll be in /root)
pwd

# List files and folders
ls

# Update the server (do this first, always!)
apt update && apt upgrade -y

# This may take 1-2 minutes — let it finish
```

---

## PART 4: Deploy Flask + PostgreSQL

### Step 4.1 — Install Required Software

```bash
# You're still connected via SSH from Part 3

# Install Python, pip, and PostgreSQL
apt install -y python3 python3-pip python3-venv postgresql postgresql-contrib nginx

# Install git (to pull your code)
apt install -y git

# Verify installations
python3 --version   # Should show Python 3.x.x
psql --version      # Should show psql 16.x
git --version       # Should show git 2.x.x
```

---

### Step 4.2 — Set Up PostgreSQL Database

```bash
# Switch to postgres user to manage the database
sudo -u postgres psql

# Inside PostgreSQL prompt (looks like: postgres=#)
# Create a database user for your app:
CREATE USER aijobhunt WITH PASSWORD 'YourSecurePassword123!';

# Create the database:
CREATE DATABASE aijobhuntdb OWNER aijobhunt;

# Give full permissions:
GRANT ALL PRIVILEGES ON DATABASE aijobhuntdb TO aijobhunt;

# Exit PostgreSQL:
\q

# You're back to the normal terminal prompt
```

---

### Step 4.3 — Clone Your Project from GitHub

```bash
# Navigate to a good location for apps
cd /var/www

# Clone your repository (replace with your actual GitHub URL)
git clone https://github.com/logeshhacker/ai-job-hunt.git

# Enter the project folder
cd ai-job-hunt

# List files to confirm everything is there
ls
```

---

### Step 4.4 — Set Up Python Virtual Environment

```bash
# While inside /var/www/ai-job-hunt:

# Create a virtual environment
python3 -m venv venv

# Activate it
source venv/bin/activate

# Your prompt changes to show (venv):
# (venv) root@ai-job-hunt-server:/var/www/ai-job-hunt#

# Install dependencies
pip install -r backend/requirements.txt

# Install gunicorn (production server for Flask)
pip install gunicorn
```

---

### Step 4.5 — Configure Environment Variables

```bash
# Create a .env file with your app's settings
nano /var/www/ai-job-hunt/.env

# Add these lines (replace values with your actual secrets):
```

```
SECRET_KEY=your-super-secret-key-change-this
DATABASE_URL=postgresql://aijobhunt:YourSecurePassword123!@localhost/aijobhuntdb
OPENAI_API_KEY=sk-your-openai-key-here
FLASK_ENV=production
```

```bash
# Save and exit nano:
# Press Ctrl+X
# Press Y
# Press Enter

# Confirm the file was created:
cat .env
```

---

### Step 4.6 — Run Database Migrations

```bash
# Still in /var/www/ai-job-hunt with (venv) active:

cd backend

# Initialize the database (run your migration commands)
flask db upgrade

# OR if you use a different migration setup:
python3 -c "from app import db; db.create_all()"

cd ..
```

---

### Step 4.7 — Test Flask is Running

```bash
# Quick test: start gunicorn manually
cd /var/www/ai-job-hunt
source venv/bin/activate
gunicorn --chdir backend wsgi:app --bind 0.0.0.0:5000

# Open a browser and go to: http://YOUR_DROPLET_IP:5000
# You should see your Flask app! ✅

# Press Ctrl+C to stop the test server
```

---

### Step 4.8 — Set Up Gunicorn as a System Service

This makes your app run automatically even after rebooting.

```bash
# Create a systemd service file
nano /etc/systemd/system/aijobhunt.service
```

Paste this content (edit paths if needed):

```ini
[Unit]
Description=AI Job Hunt Flask App
After=network.target

[Service]
User=root
WorkingDirectory=/var/www/ai-job-hunt
Environment="PATH=/var/www/ai-job-hunt/venv/bin"
EnvironmentFile=/var/www/ai-job-hunt/.env
ExecStart=/var/www/ai-job-hunt/venv/bin/gunicorn --chdir backend wsgi:app --workers 3 --bind unix:aijobhunt.sock -m 007

[Install]
WantedBy=multi-user.target
```

```bash
# Save with Ctrl+X, Y, Enter

# Enable and start the service
systemctl daemon-reload
systemctl enable aijobhunt
systemctl start aijobhunt

# Check it's running
systemctl status aijobhunt
# Should show: Active: active (running) ✅
```

---

### Step 4.9 — Configure Nginx as a Reverse Proxy

Nginx routes web traffic from port 80 (HTTP) to your Flask app.

```bash
# Create nginx config for your site
nano /etc/nginx/sites-available/aijobhunt
```

Paste this (replace `YOUR_DROPLET_IP` with your actual IP):

```nginx
server {
    listen 80;
    server_name YOUR_DROPLET_IP;

    location / {
        include proxy_params;
        proxy_pass http://unix:/var/www/ai-job-hunt/aijobhunt.sock;
    }
}
```

```bash
# Save with Ctrl+X, Y, Enter

# Enable the site
ln -s /etc/nginx/sites-available/aijobhunt /etc/nginx/sites-enabled

# Test nginx configuration
nginx -t
# Should say: syntax is ok / test is successful

# Restart nginx
systemctl restart nginx

# Open firewall for web traffic
ufw allow 'Nginx Full'
ufw allow OpenSSH
ufw enable
# Type "y" and Enter if prompted

# Visit your app in a browser:
# http://YOUR_DROPLET_IP  ← Your Flask app is live! 🎉
```

---

## PART 5: One-Click Apps & Marketplace Tips

DigitalOcean has a **Marketplace** with pre-configured apps you can deploy in 1 click — no manual setup needed for common stacks.

### Option A: Use the Marketplace (Fastest)

```
1. Go to: https://marketplace.digitalocean.com/
2. Search for "Django" or "Python" or "LAMP"
3. Click on a suitable app (e.g., "Django" or "Python Flask")
4. Click "Create Droplet"
5. Everything (Python, Nginx, Gunicorn) is pre-installed!
6. SSH in, upload your code, configure .env, done!
```

**Recommended Marketplace apps for Flask:**

| App | What's Included | Use If |
|-----|-----------------|--------|
| LAMP Stack | Linux, Apache, MySQL, PHP | You need MySQL |
| Django | Python, Nginx, PostgreSQL | Closest to Flask setup |
| Docker | Docker Engine | You use containers |

---

### Option B: App Platform (Easiest, Like Heroku)

DigitalOcean's **App Platform** is the most Heroku-like experience.

```
1. Go to: https://cloud.digitalocean.com/apps
2. Click "Create App"
3. Connect your GitHub account
4. Select your repository: logeshhacker/ai-job-hunt
5. DigitalOcean detects it's a Python app automatically
6. Configure settings:
   ├─ Build Command: pip install -r backend/requirements.txt
   └─ Run Command: gunicorn --chdir backend wsgi:app
7. Add environment variables (OPENAI_API_KEY, DATABASE_URL, etc.)
8. Click "Next" → "Create Resources"
9. Add a Database:
   ├─ Click "Add Resource" → "Database"
   └─ Select "PostgreSQL" → "Dev Database" (free tier)
10. Click "Deploy"
```

**App Platform pricing with your student credits:**

```
┌────────────────────────────────────────────┐
│  App Platform Plans                        │
├────────────────────────────────────────────┤
│  Basic (512 MB): $5/month                  │
│  With $200 credit: FREE for 40 months ✅  │
│                                            │
│  Dev Database (PostgreSQL): $0/month       │
│  (free managed database for dev apps)      │
└────────────────────────────────────────────┘
```

> 🌟 **App Platform is the RECOMMENDED approach for students** — it's the most like Heroku and requires the least manual setup.

---

### Step-by-Step: App Platform Deployment

```
STEP 1: Connect GitHub
─────────────────────
Go to: https://cloud.digitalocean.com/apps
Click: "Create App"
Click: "GitHub"
Authorize DigitalOcean to access your GitHub
Select: logeshhacker/ai-job-hunt
Branch: main (or your default branch)
Click: "Next"

STEP 2: Configure Your App
──────────────────────────
Source Directory: / (root)
Build Command: pip install -r backend/requirements.txt
Run Command: gunicorn --chdir backend wsgi:app --log-file -
HTTP Port: 5000
Click: "Next"

STEP 3: Add Environment Variables
──────────────────────────────────
Click "Edit" next to your app component
Add these variables:
  Key: SECRET_KEY         Value: your-secret-key
  Key: OPENAI_API_KEY     Value: sk-your-openai-key
  Key: FLASK_ENV          Value: production
Click: "Save"
Click: "Next"

STEP 4: Add PostgreSQL Database
────────────────────────────────
Click: "Add Resource"
Select: "Database"
Choose: "Dev Database" (PostgreSQL)
Name: aijobhunt-db
Click: "Add"
DigitalOcean auto-injects DATABASE_URL into your app ✅

STEP 5: Review & Deploy
────────────────────────
Review plan: Basic ($5/month)
Review your settings
Click: "Create Resources"
Wait 3-5 minutes for first deployment

STEP 6: Access Your App
────────────────────────
After deployment, you'll see:
├─ App URL: https://your-app-name.ondigitalocean.app
└─ Status: Running ✅
```

---

## PART 6: Troubleshooting

### Problem: SSH Connection Refused

```
Error: "ssh: connect to host XX.XX.XX.XX port 22: Connection refused"

Fix:
1. Wait 2-3 minutes after Droplet creation (it needs to boot)
2. Check your Droplet IP is correct
3. Try using password auth instead of SSH key:
   ssh -o PubkeyAuthentication=no root@YOUR_IP
4. Check DigitalOcean console (web-based terminal) as backup:
   Go to Droplet → Click "Console" button
```

---

### Problem: Permission Denied (SSH Key)

```
Error: "Permission denied (publickey)"

Fix:
1. Re-add your SSH key to the Droplet
2. Or use DigitalOcean web console to log in:
   Droplets → Your Droplet → Access → Launch Droplet Console
3. Then add your key manually:
   echo "YOUR_PUBLIC_KEY_HERE" >> ~/.ssh/authorized_keys
   chmod 600 ~/.ssh/authorized_keys
```

---

### Problem: Flask App Not Starting

```
Error when running gunicorn: "No module named..."

Fix:
1. Make sure virtual environment is activated:
   source /var/www/ai-job-hunt/venv/bin/activate

2. Reinstall requirements:
   pip install -r backend/requirements.txt

3. Check service logs:
   journalctl -u aijobhunt -n 50 --no-pager
```

---

### Problem: Can't Connect to Database

```
Error: "could not connect to server: Connection refused"

Fix:
1. Check PostgreSQL is running:
   systemctl status postgresql

2. Restart if needed:
   systemctl restart postgresql

3. Verify your DATABASE_URL in .env:
   cat /var/www/ai-job-hunt/.env

4. Test connection manually:
   psql -U aijobhunt -d aijobhuntdb -h localhost
   (enter your database password)
```

---

### Problem: Nginx 502 Bad Gateway

```
Error: "502 Bad Gateway" in browser

Fix:
1. Check if gunicorn is running:
   systemctl status aijobhunt

2. Check socket file exists:
   ls /var/www/ai-job-hunt/*.sock

3. Restart both services:
   systemctl restart aijobhunt
   systemctl restart nginx

4. Check nginx error logs:
   tail -20 /var/log/nginx/error.log
```

---

## 📊 Cost Summary (With Student Credits)

| Resource | Monthly Cost | With $200 Credit |
|----------|-------------|------------------|
| Basic Droplet (1GB) | $6/month | Covered ✅ |
| App Platform (Basic) | $5/month | Covered ✅ |
| Dev Database (PostgreSQL) | $0/month | Free ✅ |
| Bandwidth (1TB) | Included | Free ✅ |
| **Total** | **~$5-6/month** | **FREE for 33-40 months** |

---

## ✅ Final Checklist

```
PART 1 - Credits:
☐ Opened GitHub Student Pack page
☐ Clicked "Get access" for DigitalOcean
☐ Created DigitalOcean account
☐ Added payment method (for verification)
☐ Confirmed $200 credit in Billing page

PART 2 - Droplet:
☐ Created a Droplet (Ubuntu 24.04, $6/month)
☐ Noted the Droplet IP Address

PART 3 - SSH:
☐ Generated SSH key on my laptop
☐ Added public key to DigitalOcean
☐ Connected via: ssh root@YOUR_IP
☐ Saw welcome message on server

PART 4 - Deployment:
☐ Installed Python, PostgreSQL, Nginx
☐ Created database and user
☐ Cloned project from GitHub
☐ Configured .env with secrets
☐ Started app with gunicorn service
☐ Configured Nginx
☐ App accessible at http://YOUR_IP ✅

OR (App Platform - Easier):
☐ Connected GitHub to App Platform
☐ Configured build & run commands
☐ Added environment variables
☐ Added PostgreSQL Dev Database
☐ Deployed & accessed at .ondigitalocean.app URL ✅
```

---

## 🔗 Useful Links

| Resource | URL |
|----------|-----|
| GitHub Student Pack | https://education.github.com/pack |
| DigitalOcean Dashboard | https://cloud.digitalocean.com |
| App Platform | https://cloud.digitalocean.com/apps |
| Marketplace | https://marketplace.digitalocean.com |
| DigitalOcean Docs | https://docs.digitalocean.com |
| SSH Docs | https://docs.digitalocean.com/products/droplets/how-to/connect-with-ssh/ |

---

> **You're all set!** 🚀 Your AI Job Hunt project is now live on DigitalOcean — for free with your GitHub Student Pack.

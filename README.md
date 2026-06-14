# Bird Creek Studios — Glaze Lab

A glaze management web app for Bird Creek Studios. Tracks recipes, UMF analysis, test series, tile results, and materials inventory.

---

## Setup

### Requirements
- Python 3.10+
- pip

### Install

```bash
cd glazelab
pip install -r requirements.txt
```

### Run locally

```bash
python app.py
```

Open in browser: http://localhost:5000

### Access from phone (same WiFi)

1. Find your Mac's local IP: System Settings → WiFi → Details → IP Address
2. On your phone, open Safari and go to: http://[your-ip]:5000
3. Optional: Add to home screen for app-like access

---

## Deploy to Railway

### Prerequisites
- GitHub account
- Railway account (railway.app) — free to sign up

### Step 1 — Push to GitHub

```bash
cd glazelab
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/YOUR_USERNAME/glazelab.git
git push -u origin main
```

### Step 2 — Deploy on Railway

1. Go to railway.app → New Project → Deploy from GitHub repo
2. Select your glazelab repository
3. Railway will auto-detect it's a Python app

### Step 3 — Add PostgreSQL

1. In your Railway project, click + New → Database → PostgreSQL
2. Railway will automatically set DATABASE_URL in your environment

### Step 4 — Set environment variables

In Railway project settings → Variables, add:
- SECRET_KEY → any long random string (e.g. use https://randomkeygen.com)

### Step 5 — Done

Railway gives you a URL like glazelab-production.up.railway.app
That's your app, accessible from anywhere.

### Cost
Railway hobby plan: ~$5/month. Includes the PostgreSQL database.

---

## File structure

```
glazelab/
├── app.py              # Flask application and routes
├── models.py           # Database models
├── seed_data.py        # Pre-loaded glaze data (all 115 glazes)
├── requirements.txt    # Python dependencies
├── Procfile            # For Railway deployment
├── static/
│   ├── css/style.css   # All styles
│   ├── js/main.js      # JavaScript
│   └── uploads/        # Photo uploads (local only)
└── templates/
    ├── base.html        # Layout with sidebar
    ├── glazes.html      # Glaze library
    ├── glaze_detail.html
    ├── glaze_form.html
    ├── tests.html
    ├── test_detail.html
    ├── test_form.html
    ├── tile_form.html
    ├── materials.html
    └── material_form.html
```

---

## Notes

- The app runs on SQLite locally and PostgreSQL on Railway
- Photos upload to static/uploads/ locally; on Railway you'll want cloud storage (Cloudinary) for persistent photo storage — this can be added in V2
- All 115 glazes are pre-loaded on first run
- The database seeds automatically if empty on startup

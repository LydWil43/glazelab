# GlazeLab — Claude Code Reference

## Repo
https://github.com/LydWil43/glazelab.git

## Stack
- Python / Flask
- SQLAlchemy (ORM)
- PostgreSQL (Railway)
- Cloudinary (image hosting)
- BeautifulSoup4 (HTML parsing / importer)
- Gunicorn (production server)
- Jinja2 templates + static files

## Deployed site
https://glazelab-production.up.railway.app

## Database
Production PostgreSQL on Railway — always use this, not a local SQLite file.

```
postgresql://postgres:cPEzHtRudqIsHFLAjjRSzAjoXsbUzPBX@hopper.proxy.rlwy.net:59489/railway
```

Internal (Railway-only, not usable locally):
```
postgresql://postgres:cPEzHtRudqIsHFLAjjRSzAjoXsbUzPBX@postgres.railway.internal:5432/railway
```

## Cloudinary
- Cloud name: `dahoefiyw`
- API key: `485887873533373`
- API secret: `5NwCHgyK9zI1A4z5LkRYEpyt60M`

## Local dev
```bash
pip install -r requirements.txt
python app.py
```

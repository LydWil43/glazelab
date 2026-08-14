"""
One-time script: fix names and set Glazy IDs for Daisy glazes #124–#131.
Run from Railway shell: python scripts/update_daisy_glazes.py
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from app import app, db
from models import Glaze

UPDATES = [
    (107, "John Britt Snowflake Crackle #4", "36127"),
    (108, "Chun Seafoam",                    "274269"),
    (109, "Panama Blue",                      "6562"),
    (110, "John's Blue",                      "94136"),
    (111, "Golden Fake Ash",                  "2659"),
    (112, "Val's Turquoise",                  "790500"),
    (113, "Lynette's Opal",                   "111469"),
    (114, "Ile de Clay Sweet Minty Turquoise","114007"),
]

with app.app_context():
    for glaze_id, name, glazy_id in UPDATES:
        g = Glaze.query.get(glaze_id)
        if g:
            g.name = name
            g.glazy_id = glazy_id
            print(f"  #{g.studio_number} → {name} (Glazy #{glazy_id})")
        else:
            print(f"  WARNING: glaze id {glaze_id} not found")
    db.session.commit()
    print("Done.")

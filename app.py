import os
import urllib.request
import json as _json
from dotenv import load_dotenv
load_dotenv()
import cloudinary
import cloudinary.uploader
from flask import Flask, render_template, request, redirect, url_for, jsonify, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
from datetime import datetime
from models import db, Glaze, Ingredient, Material, GlazeTest, Tile, TileAddition, FiringLog, Fire, Document

app = Flask(__name__)

# Config
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-change-in-production')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///glazelab.db')
if app.config['SQLALCHEMY_DATABASE_URI'].startswith('postgres://'):
    app.config['SQLALCHEMY_DATABASE_URI'] = app.config['SQLALCHEMY_DATABASE_URI'].replace('postgres://', 'postgresql://', 1)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = os.path.join(os.path.dirname(__file__), 'static', 'uploads')
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max upload

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'heic', 'webp'}

db.init_app(app)

# Cloudinary config (set CLOUDINARY_URL or individual env vars)
cloudinary.config(
    cloud_name=os.environ.get('CLOUDINARY_CLOUD_NAME'),
    api_key=os.environ.get('CLOUDINARY_API_KEY'),
    api_secret=os.environ.get('CLOUDINARY_API_SECRET'),
)
USE_CLOUDINARY = bool(os.environ.get('CLOUDINARY_CLOUD_NAME'))

app.jinja_env.filters['fromjson'] = _json.loads

import re as _re

def _parse_addition(s):
    """Return list of {material, increment} dicts, or None.
    Handles JSON array, JSON object, and plain text 'Material +Xg' format."""
    if not s:
        return None
    if s.startswith('['):
        try:
            result = _json.loads(s)
            return result or None
        except Exception:
            pass
    elif s.startswith('{'):
        try:
            return [_json.loads(s)]
        except Exception:
            pass
    # Plain text format: "Material +Xg"
    m = _re.match(r'^(.+?)\s*\+(\d+\.?\d*)g?$', s.strip())
    if m:
        return [{'material': m.group(1).strip(), 'increment': float(m.group(2))}]
    return None

app.jinja_env.filters['parse_addition'] = _parse_addition

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def upload_photo(file):
    """Upload a photo file and return a URL string, or None on failure."""
    if not (file and file.filename and allowed_file(file.filename)):
        return None
    if USE_CLOUDINARY:
        result = cloudinary.uploader.upload(
            file,
            folder='glazelab',
            resource_type='image',
        )
        return result['secure_url']
    filename = secure_filename(f"tile_{datetime.utcnow().timestamp()}_{file.filename}")
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    return f"uploads/{filename}"

def upload_photo_b64(data_url):
    """Upload a base64 data URL (from cropper) and return a URL string, or None."""
    if not data_url or not data_url.startswith('data:image'):
        return None
    import base64
    header, b64 = data_url.split(',', 1)
    image_bytes = base64.b64decode(b64)
    if USE_CLOUDINARY:
        result = cloudinary.uploader.upload(
            f"data:image/jpeg;base64,{b64}",
            folder='glazelab',
            resource_type='image',
        )
        return result['secure_url']
    filename = f"tile_{datetime.utcnow().timestamp()}.jpg"
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    with open(os.path.join(app.config['UPLOAD_FOLDER'], filename), 'wb') as f:
        f.write(image_bytes)
    return f"uploads/{filename}"

# ─── ROUTES ──────────────────────────────────────────────────────────────────

@app.route('/')
def index():
    return redirect(url_for('glazes'))

# ─── GLAZES ──────────────────────────────────────────────────────────────────

@app.route('/glazes')
def glazes():
    status_filter = request.args.get('status', '')
    tag_filter = request.args.get('tag', '')
    category_filter = request.args.get('category', '')
    search = request.args.get('q', '')
    query = Glaze.query
    if status_filter:
        query = query.filter_by(status=status_filter)
    if tag_filter:
        query = query.filter(Glaze.tags.ilike(f'%{tag_filter}%'))
    if category_filter:
        query = query.filter(
            db.or_(
                Glaze.primary_category == category_filter,
                Glaze.secondary_category == category_filter
            )
        )
    if search:
        query = query.filter(
            db.or_(
                Glaze.name.ilike(f'%{search}%'),
                Glaze.studio_number.ilike(f'%{search}%'),
                Glaze.notes.ilike(f'%{search}%'),
                Glaze.ingredients.any(Ingredient.material.ilike(f'%{search}%'))
            )
        )
    all_glazes = query.order_by(Glaze.created_at.desc()).all()
    # Collect all unique tags for filter chips
    all_tags = sorted(set(
        t.strip() for g in Glaze.query.all()
        if g.tags for t in g.tags.split(',') if t.strip()
    ))
    return render_template('glazes.html', glazes=all_glazes, status_filter=status_filter,
                           tag_filter=tag_filter, category_filter=category_filter,
                           search=search, all_tags=all_tags)

@app.route('/glazes/<int:glaze_id>')
def glaze_detail(glaze_id):
    glaze = Glaze.query.get_or_404(glaze_id)
    return render_template('glaze_detail.html', glaze=glaze)

@app.route('/glazes/new', methods=['GET', 'POST'])
def new_glaze():
    if request.method == 'POST':
        glaze = Glaze(
            studio_number=request.form['studio_number'],
            name=request.form['name'],
            glazy_id=request.form.get('glazy_id', ''),
            cone=request.form.get('cone', ''),
            atmosphere=request.form.get('atmosphere', ''),
            surface=request.form.get('surface', ''),
            transparency=request.form.get('transparency', ''),
            status=request.form.get('status', 'testing'),
            notes=request.form.get('notes', ''),
            lineage_notes=request.form.get('lineage_notes', ''),
            batch_date=request.form.get('batch_date', ''),
            tags=request.form.get('tags', ''),
            primary_category=request.form.get('primary_category', '') or None,
            secondary_category=request.form.get('secondary_category', '') or None,
            umf_expansion=float(request.form['umf_expansion']) if request.form.get('umf_expansion') else None,
            umf_r2o_ro=request.form.get('umf_r2o_ro', ''),
            umf_sio2_al2o3=float(request.form['umf_sio2_al2o3']) if request.form.get('umf_sio2_al2o3') else None,
            umf_na2o=float(request.form['umf_na2o']) if request.form.get('umf_na2o') else None,
            umf_k2o=float(request.form['umf_k2o']) if request.form.get('umf_k2o') else None,
            umf_cao=float(request.form['umf_cao']) if request.form.get('umf_cao') else None,
            umf_mgo=float(request.form['umf_mgo']) if request.form.get('umf_mgo') else None,
            umf_al2o3=float(request.form['umf_al2o3']) if request.form.get('umf_al2o3') else None,
            umf_sio2=float(request.form['umf_sio2']) if request.form.get('umf_sio2') else None,
            umf_b2o3=float(request.form['umf_b2o3']) if request.form.get('umf_b2o3') else None,
        )
        db.session.add(glaze)
        db.session.flush()

        materials = request.form.getlist('material[]')
        amounts = request.form.getlist('amount[]')
        additives = request.form.getlist('is_additive[]')

        for i, (mat, amt) in enumerate(zip(materials, amounts)):
            if mat.strip():
                ingredient = Ingredient(
                    glaze_id=glaze.id,
                    material=mat.strip(),
                    amount=float(amt) if amt else 0,
                    is_additive=str(i) in additives,
                    sort_order=i
                )
                db.session.add(ingredient)

        db.session.commit()
        flash('Glaze added successfully.', 'success')
        return redirect(url_for('glaze_detail', glaze_id=glaze.id))
    all_numbers = [g.studio_number for g in Glaze.query.with_entities(Glaze.studio_number).all()]
    numeric = [int(n) for n in all_numbers if n and n.isdigit()]
    next_number = str(max(numeric) + 1) if numeric else ''
    return render_template('glaze_form.html', glaze=None, next_studio_number=next_number)

@app.route('/glazes/<int:glaze_id>/edit', methods=['GET', 'POST'])
def edit_glaze(glaze_id):
    glaze = Glaze.query.get_or_404(glaze_id)
    if request.method == 'POST':
        glaze.studio_number = request.form['studio_number']
        glaze.name = request.form['name']
        glaze.glazy_id = request.form.get('glazy_id', '')
        glaze.cone = request.form.get('cone', '')
        glaze.atmosphere = request.form.get('atmosphere', '')
        glaze.surface = request.form.get('surface', '')
        glaze.transparency = request.form.get('transparency', '')
        glaze.status = request.form.get('status', 'testing')
        glaze.notes = request.form.get('notes', '')
        glaze.lineage_notes = request.form.get('lineage_notes', '')
        glaze.batch_date = request.form.get('batch_date', '')
        glaze.tags = request.form.get('tags', '')
        glaze.primary_category = request.form.get('primary_category', '') or None
        glaze.secondary_category = request.form.get('secondary_category', '') or None
        glaze.umf_expansion = float(request.form['umf_expansion']) if request.form.get('umf_expansion') else None
        glaze.umf_r2o_ro = request.form.get('umf_r2o_ro', '')
        glaze.umf_sio2_al2o3 = float(request.form['umf_sio2_al2o3']) if request.form.get('umf_sio2_al2o3') else None
        glaze.umf_na2o = float(request.form['umf_na2o']) if request.form.get('umf_na2o') else None
        glaze.umf_k2o = float(request.form['umf_k2o']) if request.form.get('umf_k2o') else None
        glaze.umf_cao = float(request.form['umf_cao']) if request.form.get('umf_cao') else None
        glaze.umf_mgo = float(request.form['umf_mgo']) if request.form.get('umf_mgo') else None
        glaze.umf_al2o3 = float(request.form['umf_al2o3']) if request.form.get('umf_al2o3') else None
        glaze.umf_sio2 = float(request.form['umf_sio2']) if request.form.get('umf_sio2') else None
        glaze.umf_b2o3 = float(request.form['umf_b2o3']) if request.form.get('umf_b2o3') else None
        glaze.updated_at = datetime.utcnow()

        # Replace ingredients
        for ing in glaze.ingredients:
            db.session.delete(ing)
        db.session.flush()

        materials = request.form.getlist('material[]')
        amounts = request.form.getlist('amount[]')
        additives = request.form.getlist('is_additive[]')

        for i, (mat, amt) in enumerate(zip(materials, amounts)):
            if mat.strip():
                ingredient = Ingredient(
                    glaze_id=glaze.id,
                    material=mat.strip(),
                    amount=float(amt) if amt else 0,
                    is_additive=str(i) in additives,
                    sort_order=i
                )
                db.session.add(ingredient)

        db.session.commit()
        flash('Glaze updated.', 'success')
        return redirect(url_for('glaze_detail', glaze_id=glaze.id))
    return render_template('glaze_form.html', glaze=glaze)

@app.route('/glazes/<int:glaze_id>/delete', methods=['POST'])
def delete_glaze(glaze_id):
    glaze = Glaze.query.get_or_404(glaze_id)
    db.session.delete(glaze)
    db.session.commit()
    flash('Glaze deleted.', 'success')
    return redirect(url_for('glazes'))

@app.route('/glazes/<int:glaze_id>/note', methods=['POST'])
def add_glaze_note(glaze_id):
    glaze = Glaze.query.get_or_404(glaze_id)
    text = request.json.get('text', '').strip()
    if not text:
        return jsonify({'error': 'empty'}), 400
    date_str = datetime.utcnow().strftime('%B %d, %Y')
    new_entry = f"[{date_str}] {text}"
    glaze.notes = (new_entry + '\n\n' + glaze.notes) if glaze.notes else new_entry
    db.session.commit()
    return jsonify({'notes': glaze.notes})

# ─── TESTS ───────────────────────────────────────────────────────────────────

@app.route('/tests')
def tests():
    active_tests = GlazeTest.query.filter(GlazeTest.status != 'complete').order_by(GlazeTest.created_at.desc()).all()
    unassigned_count = GlazeTest.query.filter(GlazeTest.fire_id==None, GlazeTest.status != 'complete').count()
    return render_template('tests.html', tests=active_tests, unassigned_count=unassigned_count)

@app.route('/tests/archive')
def tests_archive():
    archived = GlazeTest.query.filter_by(status='complete').order_by(GlazeTest.created_at.desc()).all()
    return render_template('tests_archive.html', tests=archived)

@app.route('/tests/new', methods=['GET', 'POST'])
def new_test():
    glazes = Glaze.query.order_by(Glaze.studio_number).all()
    if request.method == 'POST':
        test = GlazeTest(
            glaze_id=int(request.form['glaze_id']),
            name=request.form['name'],
            description=request.form.get('description', ''),
            test_type=request.form.get('test_type', 'progression_blend'),
            base_batch_size=float(request.form['base_batch_size']) if request.form.get('base_batch_size') else 100,
            excluded_ingredients=request.form.get('excluded_ingredients', '[]'),
            status='planned'
        )
        db.session.add(test)
        db.session.commit()
        flash('Test created.', 'success')
        return redirect(url_for('test_detail', test_id=test.id))
    glaze_id = request.args.get('glaze_id')
    return render_template('test_form.html', glazes=glazes, preselected_glaze=glaze_id)

@app.route('/tests/<int:test_id>')
def test_detail(test_id):
    test = GlazeTest.query.get_or_404(test_id)
    # Compute per-material cumulative totals for progression_blend tiles.
    # Prefer TileAddition records (from import); fall back to parsing tile.additions text.
    cumulative = {}
    running = {}
    for tile in test.tiles:
        tile_adds = (db.session.query(TileAddition, Material)
                     .join(Material, TileAddition.material_id == Material.id)
                     .filter(TileAddition.tile_id == tile.id)
                     .order_by(TileAddition.sort_order).all())
        if tile_adds:
            if test.test_type == 'progression_blend':
                for ta, mat in tile_adds:
                    running[mat.name] = round(running.get(mat.name, 0) + ta.amount, 4)
                cumulative[tile.id] = dict(running)
            else:
                cumulative[tile.id] = {mat.name: ta.amount for ta, mat in tile_adds}
        elif test.test_type == 'progression_blend':
            items = _parse_addition(tile.additions)
            if items:
                for item in items:
                    mat = item.get('material')
                    inc = item.get('increment', 0)
                    if mat and mat != 'Base' and inc:
                        running[mat] = round(running.get(mat, 0) + inc, 4)
            if running:
                cumulative[tile.id] = dict(running)
    return render_template('test_detail.html', test=test, cumulative=cumulative)

@app.route('/tests/<int:test_id>/status', methods=['POST'])
def update_test_status(test_id):
    test = GlazeTest.query.get_or_404(test_id)
    test.status = request.form.get('status', test.status)
    db.session.commit()
    return redirect(url_for('test_detail', test_id=test_id))

@app.route('/tests/<int:test_id>/edit', methods=['GET', 'POST'])
def edit_test(test_id):
    test = GlazeTest.query.get_or_404(test_id)
    if request.method == 'POST':
        test.name = request.form.get('name', test.name).strip() or test.name
        test.test_type = request.form.get('test_type', test.test_type)
        test.variable = request.form.get('variable', '').strip() or None
        test.description = request.form.get('description', '').strip() or None
        test.base_batch_size = float(request.form['base_batch_size']) if request.form.get('base_batch_size') else test.base_batch_size
        db.session.commit()
        return redirect(url_for('test_detail', test_id=test_id))
    return render_template('test_edit.html', test=test)

@app.route('/tests/<int:test_id>/delete', methods=['POST'])
def delete_test(test_id):
    test = GlazeTest.query.get_or_404(test_id)
    db.session.delete(test)
    db.session.commit()
    flash('Test deleted.', 'success')
    return redirect(url_for('tests'))

@app.route('/tests/<int:test_id>/tiles/new', methods=['GET', 'POST'])
def new_tile(test_id):
    test = GlazeTest.query.get_or_404(test_id)
    materials = Material.query.order_by(Material.name).all()
    if request.method == 'POST':
        photo_data = request.form.get('photo_data', '')
        photo_path = upload_photo_b64(photo_data) or upload_photo(request.files.get('photo'))
        if test.test_type == 'progression_blend':
            mats = request.form.getlist('addition_material[]')
            incs = request.form.getlist('addition_increment[]')
            pairs = [{'material': m, 'increment': float(i) if i else 0}
                     for m, i in zip(mats, incs) if m]
            additions = _json.dumps(pairs) if pairs else _json.dumps([{'material': 'Base', 'increment': 0}])
        else:
            additions = request.form.get('additions', '')

        tile = Tile(
            test_id=test_id,
            tile_number=int(request.form['tile_number']),
            additions=additions,
            thickness=int(request.form['thickness']) if request.form.get('thickness') else None,
            wood_ash_on_top=request.form.get('wood_ash_on_top') == 'on',
            atmosphere=request.form.get('atmosphere', ''),
            cone=request.form.get('cone', ''),
            body_reduction=request.form.get('body_reduction', ''),
            glaze_reduction=request.form.get('glaze_reduction', ''),
            cooling=request.form.get('cooling', ''),
            result_notes=request.form.get('result_notes', ''),
            photo_path=photo_path,
            fired_at=datetime.utcnow() if request.form.get('atmosphere') else None
        )
        db.session.add(tile)
        db.session.commit()
        flash('Tile logged.', 'success')
        return redirect(url_for('test_detail', test_id=test_id))
    next_tile = len(test.tiles) + 1
    return render_template('tile_form.html', test=test, next_tile=next_tile, materials=materials)

@app.route('/tiles/<int:tile_id>/edit', methods=['GET', 'POST'])
def edit_tile(tile_id):
    tile = Tile.query.get_or_404(tile_id)
    materials = Material.query.order_by(Material.name).all()
    if request.method == 'POST':
        photo_data = request.form.get('photo_data', '')
        new_photo = upload_photo_b64(photo_data) or upload_photo(request.files.get('photo'))
        if new_photo:
            tile.photo_path = new_photo

        if tile.test.test_type == 'progression_blend':
            mats = request.form.getlist('addition_material[]')
            incs = request.form.getlist('addition_increment[]')
            pairs = [{'material': m, 'increment': float(i) if i else 0}
                     for m, i in zip(mats, incs) if m]
            tile.additions = _json.dumps(pairs) if pairs else _json.dumps([{'material': 'Base', 'increment': 0}])
        else:
            tile.additions = request.form.get('additions', '')
        tile.thickness = int(request.form['thickness']) if request.form.get('thickness') else None
        tile.wood_ash_on_top = request.form.get('wood_ash_on_top') == 'on'
        tile.atmosphere = request.form.get('atmosphere', '')
        tile.cone = request.form.get('cone', '')
        tile.body_reduction = request.form.get('body_reduction', '')
        tile.glaze_reduction = request.form.get('glaze_reduction', '')
        tile.cooling = request.form.get('cooling', '')
        tile.result_notes = request.form.get('result_notes', '')
        if tile.atmosphere and not tile.fired_at:
            tile.fired_at = datetime.utcnow()
        db.session.commit()
        flash('Tile updated.', 'success')
        return redirect(url_for('test_detail', test_id=tile.test_id))
    addition_data = _parse_addition(tile.additions)
    return render_template('tile_form.html', test=tile.test, tile=tile, next_tile=tile.tile_number,
                           materials=materials, addition_data=addition_data)

# ─── MATERIALS ───────────────────────────────────────────────────────────────

@app.route('/materials')
def materials():
    all_materials = Material.query.order_by(Material.name).all()
    return render_template('materials.html', materials=all_materials)

@app.route('/materials/new', methods=['GET', 'POST'])
def new_material():
    if request.method == 'POST':
        material = Material(
            name=request.form['name'],
            price_per_lb=float(request.form['price_per_lb']) if request.form.get('price_per_lb') else None,
            stock_lbs=float(request.form['stock_lbs']) if request.form.get('stock_lbs') else None,
            notes=request.form.get('notes', ''),
            invoice_date=request.form.get('invoice_date', '')
        )
        db.session.add(material)
        db.session.commit()
        flash('Material added.', 'success')
        return redirect(url_for('materials'))
    return render_template('material_form.html', material=None)

@app.route('/materials/<int:material_id>/edit', methods=['GET', 'POST'])
def edit_material(material_id):
    material = Material.query.get_or_404(material_id)
    if request.method == 'POST':
        material.name = request.form['name']
        material.price_per_lb = float(request.form['price_per_lb']) if request.form.get('price_per_lb') else None
        material.stock_lbs = float(request.form['stock_lbs']) if request.form.get('stock_lbs') else None
        material.notes = request.form.get('notes', '')
        material.invoice_date = request.form.get('invoice_date', '')
        material.updated_at = datetime.utcnow()
        db.session.commit()
        flash('Material updated.', 'success')
        return redirect(url_for('materials'))
    return render_template('material_form.html', material=material)

@app.route('/materials/<int:material_id>/delete', methods=['POST'])
def delete_material(material_id):
    material = Material.query.get_or_404(material_id)
    TileAddition.query.filter_by(material_id=material_id).delete()
    db.session.delete(material)
    db.session.commit()
    flash('Material deleted.', 'success')
    return redirect(url_for('materials'))

@app.route('/tests/print')
def print_tests():
    tag_filter = request.args.get('tag', '')
    query = GlazeTest.query
    if tag_filter:
        query = query.join(Glaze).filter(Glaze.tags.ilike(f'%{tag_filter}%'))
    all_tests = query.order_by(GlazeTest.glaze_id, GlazeTest.id).all()
    all_tags = sorted(set(
        t.strip() for g in Glaze.query.all()
        if g.tags for t in g.tags.split(',') if t.strip()
    ))
    now = datetime.utcnow().strftime('%B %d, %Y')
    return render_template('tests_print.html', tests=all_tests, now=now,
                           all_tags=all_tags, tag_filter=tag_filter)

# ─── FIRES ───────────────────────────────────────────────────────────────────

@app.route('/fires')
def fires():
    all_fires = Fire.query.order_by(Fire.created_at.desc()).all()
    return render_template('fires.html', fires=all_fires)

@app.route('/fires/new', methods=['GET', 'POST'])
def new_fire():
    if request.method == 'POST':
        fire = Fire(
            name=request.form['name'],
            cone=request.form.get('cone', ''),
            atmosphere=request.form.get('atmosphere', ''),
            status=request.form.get('status', 'planning'),
        )
        db.session.add(fire)
        db.session.commit()
        return redirect(url_for('fire_detail', fire_id=fire.id))
    return render_template('fire_form.html', fire=None)

@app.route('/fires/<int:fire_id>')
def fire_detail(fire_id):
    fire = Fire.query.get_or_404(fire_id)
    unassigned = GlazeTest.query.filter_by(fire_id=None).order_by(GlazeTest.id).all()
    return render_template('fire_detail.html', fire=fire, unassigned=unassigned)

@app.route('/fires/<int:fire_id>/edit', methods=['GET', 'POST'])
def edit_fire(fire_id):
    fire = Fire.query.get_or_404(fire_id)
    if request.method == 'POST':
        fire.name = request.form['name']
        fire.cone = request.form.get('cone', '')
        fire.atmosphere = request.form.get('atmosphere', '')
        fire.status = request.form.get('status', 'planning')
        db.session.commit()
        return redirect(url_for('fire_detail', fire_id=fire.id))
    return render_template('fire_form.html', fire=fire)

@app.route('/fires/<int:fire_id>/assign', methods=['POST'])
def assign_test(fire_id):
    fire = Fire.query.get_or_404(fire_id)
    test_id = request.form.get('test_id')
    test = GlazeTest.query.get_or_404(test_id)
    test.fire_id = fire.id
    db.session.commit()
    return redirect(url_for('fire_detail', fire_id=fire.id))

@app.route('/tiles/<int:tile_id>/photo', methods=['POST'])
def upload_tile_photo(tile_id):
    tile = Tile.query.get_or_404(tile_id)
    photo_path = upload_photo(request.files.get('photo'))
    if photo_path:
        tile.photo_path = photo_path
        db.session.commit()
    return redirect(url_for('test_detail', test_id=tile.test_id))

@app.route('/tiles/<int:tile_id>/set-cover', methods=['POST'])
def set_cover_tile(tile_id):
    tile = Tile.query.get_or_404(tile_id)
    glaze = tile.test.glaze
    if glaze.cover_tile_id == tile_id:
        glaze.cover_tile_id = None  # toggle off if already set
    else:
        glaze.cover_tile_id = tile_id
    db.session.commit()
    return redirect(url_for('test_detail', test_id=tile.test_id))

@app.route('/tests/<int:test_id>/unassign', methods=['POST'])
def unassign_test(test_id):
    test = GlazeTest.query.get_or_404(test_id)
    fire_id = test.fire_id
    test.fire_id = None
    db.session.commit()
    return redirect(url_for('fire_detail', fire_id=fire_id) if fire_id else url_for('tests'))

@app.route('/fires/<int:fire_id>/delete', methods=['POST'])
def delete_fire(fire_id):
    fire = Fire.query.get_or_404(fire_id)
    for test in fire.tests:
        test.fire_id = None
    db.session.delete(fire)
    db.session.commit()
    return redirect(url_for('fires'))

@app.route('/fires/<int:fire_id>/sheet.json')
def fire_sheet(fire_id):
    fire = Fire.query.get_or_404(fire_id)
    tests_data = []
    for test in fire.tests:
        base = [{'material': i.material, 'amount': i.amount}
                for i in test.glaze.ingredients if not i.is_additive]
        additives = [{'material': i.material, 'amount': i.amount}
                     for i in test.glaze.ingredients if i.is_additive]
        progression = None
        if test.tiles:
            progression = {
                'headers': ['Tile', 'Additions', 'Atmosphere', 'Result'],
                'rows': [[t.tile_number, t.additions or '—',
                          t.atmosphere or '—', t.result_notes or ''] for t in test.tiles]
            }
        elif test.progression_plan:
            progression = _json.loads(test.progression_plan)
        tests_data.append({
            'glaze': {'studio_number': test.glaze.studio_number,
                      'name': test.glaze.name, 'tags': test.glaze.tags},
            'test': {'name': test.name, 'type': test.test_type,
                     'base_batch_size': test.base_batch_size, 'status': test.status},
            'recipe': {'base': base, 'additives': additives},
            'progression': progression,
        })
    return jsonify({
        'fire': {'name': fire.name, 'cone': fire.cone,
                 'atmosphere': fire.atmosphere, 'status': fire.status,
                 'date': fire.created_at.strftime('%B %d, %Y')},
        'tests': tests_data
    })

@app.route('/proxy-image')
def proxy_image():
    url = request.args.get('url', '')
    if not url:
        return '', 400
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'GlazeLab/1.0'})
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = resp.read()
            content_type = resp.headers.get('Content-Type', 'image/jpeg')
        from flask import Response
        return Response(data, content_type=content_type)
    except Exception:
        return '', 502

# ─── API ─────────────────────────────────────────────────────────────────────

@app.route('/api/glazes')
def api_glazes():
    glazes = Glaze.query.order_by(Glaze.studio_number).all()
    return jsonify([g.to_dict() for g in glazes])

@app.route('/api/glazes/<int:glaze_id>')
def api_glaze(glaze_id):
    glaze = Glaze.query.get_or_404(glaze_id)
    return jsonify(glaze.to_dict())

@app.route('/api/glazy-fetch/<glazy_id>')
def glazy_fetch(glazy_id):
    """Proxy a Glazy recipe and return UMF analysis fields."""
    try:
        url = f"https://api.glazy.org/api/recipes/{glazy_id}"
        req = urllib.request.Request(url, headers={'Accept': 'application/json', 'User-Agent': 'GlazeLab/1.0'})
        with urllib.request.urlopen(req, timeout=8) as resp:
            data = _json.loads(resp.read())
    except Exception as e:
        return jsonify({'error': str(e)}), 502

    recipe = data.get('data', data)
    analysis = recipe.get('analysis', {})
    umf = analysis.get('umfAnalysis', {})

    def f(d, key):
        v = d.get(key)
        return round(float(v), 4) if v is not None else None

    r2o_total = f(umf, 'R2OTotal')
    ro_total  = f(umf, 'ROTotal')
    r2o = f"{r2o_total}:{ro_total}" if r2o_total is not None and ro_total is not None else None

    ingredients = [
        {
            'material': c.get('material', {}).get('name', ''),
            'amount': round(float(c.get('percentageAmount', 0)), 2),
            'is_additive': c.get('isAdditional', False),
        }
        for c in recipe.get('materialComponents', [])
        if c.get('material', {}).get('name')
    ]

    return jsonify({
        'name':           recipe.get('name'),
        'ingredients':    ingredients,
        'umf_na2o':       f(umf, 'Na2O'),
        'umf_k2o':        f(umf, 'K2O'),
        'umf_cao':        f(umf, 'CaO'),
        'umf_mgo':        f(umf, 'MgO'),
        'umf_al2o3':      f(umf, 'Al2O3'),
        'umf_sio2':       f(umf, 'SiO2'),
        'umf_b2o3':       f(umf, 'B2O3'),
        'umf_r2o_ro':     r2o,
        'umf_sio2_al2o3': f(umf, 'SiO2Al2O3Ratio'),
        'umf_expansion':  f(analysis, 'thermalExpansion'),
    })

# ─── DOCUMENTS ────────────────────────────────────────────────────────────────

@app.route('/docs')
def docs():
    documents = Document.query.order_by(Document.updated_at.desc()).all()
    return render_template('docs.html', documents=documents)

@app.route('/docs/new', methods=['GET', 'POST'])
def new_doc():
    if request.method == 'POST':
        doc = Document(
            title=request.form['title'],
            content=request.form.get('content', ''),
        )
        db.session.add(doc)
        db.session.commit()
        return redirect(url_for('doc_detail', doc_id=doc.id))
    return render_template('doc_form.html', doc=None)

@app.route('/docs/<int:doc_id>')
def doc_detail(doc_id):
    doc = Document.query.get_or_404(doc_id)
    states = _json.loads(doc.checkbox_states or '{}')
    return render_template('doc_detail.html', doc=doc, states=states)

@app.route('/docs/<int:doc_id>/edit', methods=['GET', 'POST'])
def edit_doc(doc_id):
    doc = Document.query.get_or_404(doc_id)
    if request.method == 'POST':
        doc.title = request.form['title']
        doc.content = request.form.get('content', '')
        db.session.commit()
        return redirect(url_for('doc_detail', doc_id=doc.id))
    return render_template('doc_form.html', doc=doc)

@app.route('/docs/<int:doc_id>/delete', methods=['POST'])
def delete_doc(doc_id):
    doc = Document.query.get_or_404(doc_id)
    db.session.delete(doc)
    db.session.commit()
    return redirect(url_for('docs'))

@app.route('/docs/<int:doc_id>/checkboxes', methods=['POST'])
def save_doc_checkboxes(doc_id):
    doc = Document.query.get_or_404(doc_id)
    data = request.get_json()
    states = _json.loads(doc.checkbox_states or '{}')
    states[str(data['index'])] = data['checked']
    doc.checkbox_states = _json.dumps(states)
    db.session.commit()
    return jsonify({'ok': True})

@app.route('/docs/<int:doc_id>/notes', methods=['POST'])
def save_doc_notes(doc_id):
    doc = Document.query.get_or_404(doc_id)
    data = request.get_json()
    notes = _json.loads(doc.obs_notes or '{}')
    notes[str(data['index'])] = data['value']
    doc.obs_notes = _json.dumps(notes)
    db.session.commit()
    return jsonify({'ok': True})

@app.route('/docs/<int:doc_id>/render')
def render_doc(doc_id):
    from flask import Response
    doc = Document.query.get_or_404(doc_id)
    states = _json.dumps(_json.loads(doc.checkbox_states or '{}'))
    notes = _json.dumps(_json.loads(doc.obs_notes or '{}'))
    inject = f"""<script>
(function(){{
  var DOC_ID = {doc_id};
  var SAVED = {states};
  var SAVED_NOTES = {notes};
  var noteTimers = {{}};
  function init() {{
    var boxes = document.querySelectorAll('input[type="checkbox"]');
    boxes.forEach(function(cb, i) {{
      if (SAVED[String(i)]) cb.checked = true;
      cb.addEventListener('change', function() {{
        fetch('/docs/' + DOC_ID + '/checkboxes', {{
          method: 'POST',
          headers: {{'Content-Type': 'application/json'}},
          body: JSON.stringify({{index: i, checked: cb.checked}})
        }});
      }});
    }});
    var inputs = document.querySelectorAll('.obs-input');
    inputs.forEach(function(inp, i) {{
      if (SAVED_NOTES[String(i)]) inp.value = SAVED_NOTES[String(i)];
      inp.addEventListener('input', function() {{
        clearTimeout(noteTimers[i]);
        noteTimers[i] = setTimeout(function() {{
          fetch('/docs/' + DOC_ID + '/notes', {{
            method: 'POST',
            headers: {{'Content-Type': 'application/json'}},
            body: JSON.stringify({{index: i, value: inp.value}})
          }});
        }}, 800);
      }});
    }});
    parent.postMessage({{iframeHeight: document.documentElement.scrollHeight}}, '*');
  }}
  if (document.readyState === 'loading') {{
    document.addEventListener('DOMContentLoaded', init);
  }} else {{
    init();
  }}
}})();
</script>"""
    html = doc.content
    if '</body>' in html:
        html = html.replace('</body>', inject + '</body>')
    else:
        html = html + inject
    return Response(html, mimetype='text/html')

# ─── DOC IMPORT ───────────────────────────────────────────────────────────────

_VALID_FORMAT_TYPES = {'Progression Blend', 'Line Blend', 'Discrete Batch', 'Layering Test'}


def _parse_import_block(root):
    """Parse one .glazelab-import wrapper into a structured dict. No DB access."""
    glaze_number = (root.get('data-glaze-number') or '').strip()
    incoming_name = (root.get('data-glaze-name') or '').strip()
    cone = (root.get('data-cone') or '').strip()
    atmosphere = (root.get('data-atmosphere') or '').strip()
    category = (root.get('data-category') or '').strip()

    recipe = []
    recipe_block = root.find(class_='gl-recipe')
    if recipe_block:
        for mat_el in recipe_block.find_all(class_='gl-material'):
            try:
                amount = float(mat_el.get('data-amount') or 0)
            except ValueError:
                amount = 0.0
            recipe.append({
                'material': (mat_el.get('data-material') or '').strip(),
                'amount': amount,
            })

    series_list = []
    for series_el in root.find_all(class_='gl-series'):
        tiles = []
        for tile_el in series_el.find_all(class_='gl-tile'):
            try:
                tile_num = int(tile_el.get('data-tile'))
            except (TypeError, ValueError):
                continue
            additions_data = []
            for add_el in tile_el.find_all(class_='gl-addition'):
                try:
                    amount = float(add_el.get('data-amount') or 0)
                except ValueError:
                    amount = 0.0
                additions_data.append({
                    'raw_name': (add_el.get('data-material') or '').strip(),
                    'amount': amount,
                })
            tiles.append({
                'number': tile_num,
                'addition': (tile_el.get('data-addition') or '').strip(),
                'additions_data': additions_data,
            })

        format_type = (series_el.get('data-format-type') or '').strip()
        if format_type not in _VALID_FORMAT_TYPES:
            error = (f'unrecognized format_type: "{format_type}"'
                     if format_type else 'missing data-format-type')
            valid = False
        else:
            error = None
            valid = True

        series_list.append({
            'name': (series_el.get('data-name') or 'Untitled Series').strip(),
            'variable': (series_el.get('data-variable') or '').strip(),
            'format_type': format_type if valid else None,
            'fixed_addition': (series_el.get('data-fixed') or '').strip(),
            'tiles': tiles,
            'valid': valid,
            'error': error,
        })

    return {
        'glaze_number': glaze_number,
        'incoming_name': incoming_name,
        'cone': cone,
        'atmosphere': atmosphere,
        'category': category,
        'recipe': recipe,
        'series': series_list,
    }


@app.route('/import-doc', methods=['GET', 'POST'])
def import_doc():
    if request.method == 'GET':
        return render_template('import_doc.html', state='upload')

    import json
    from bs4 import BeautifulSoup

    f = request.files.get('file')
    if not f:
        flash('No file uploaded.', 'error')
        return redirect(url_for('import_doc'))

    html = f.read().decode('utf-8')
    soup = BeautifulSoup(html, 'html.parser')
    wrappers = soup.find_all(class_='glazelab-import')

    if not wrappers:
        flash('No glazelab-import marker found. Make sure it was generated with the GlazeLab schema.', 'error')
        return redirect(url_for('import_doc'))

    # Save / update Document
    title = (wrappers[0].get('data-doc-title') or
             (soup.title.string if soup.title else None) or
             'Imported Doc')
    existing_doc = Document.query.filter_by(title=title).first()
    if existing_doc:
        existing_doc.content = html
        doc = existing_doc
    else:
        doc = Document(title=title, content=html)
        db.session.add(doc)
    db.session.commit()

    # Build a material lookup cache (name → id) for resolution
    all_materials = Material.query.order_by(Material.name).all()
    material_lookup = {m.name: m.id for m in all_materials}

    # Parse and classify each wrapper
    blocks = []
    for root in wrappers:
        block = _parse_import_block(root)
        glaze_number = block['glaze_number']
        incoming_name = block['incoming_name']

        existing_glaze = Glaze.query.filter_by(studio_number=glaze_number).first() if glaze_number else None
        if existing_glaze is None:
            block['classification'] = 'new'
            block['current_name'] = None
        elif existing_glaze.name == incoming_name:
            block['classification'] = 'clean'
            block['current_name'] = existing_glaze.name
        else:
            block['classification'] = 'name_mismatch'
            block['current_name'] = existing_glaze.name

        # Resolve materials in tile additions
        for s_idx, s in enumerate(block['series']):
            for tile in s['tiles']:
                for add in tile['additions_data']:
                    mat_id = material_lookup.get(add['raw_name'])
                    add['material_id'] = mat_id  # None if unresolved
                tile['resolved'] = all(
                    a['material_id'] is not None for a in tile['additions_data']
                )

        blocks.append(block)

    materials_for_select = [{'id': m.id, 'name': m.name} for m in all_materials]
    return render_template('import_doc.html', state='preview',
                           blocks=blocks, preview_json=json.dumps(blocks),
                           doc=doc, materials_for_select=materials_for_select)


@app.route('/import-doc/apply', methods=['POST'])
def import_doc_apply():
    import json

    blocks = json.loads(request.form.get('preview_data', '[]'))
    doc_id = request.form.get('doc_id')
    results = []

    for block in blocks:
        glaze_number = block['glaze_number']
        classification = block['classification']
        choice = request.form.get(f'choice_{glaze_number}', 'apply')

        if classification == 'name_mismatch' and choice == 'skip':
            results.append({
                'glaze_number': glaze_number,
                'name': block['current_name'],
                'status': 'skipped',
            })
            continue

        try:
            existing_glaze = Glaze.query.filter_by(studio_number=glaze_number).first()

            if classification == 'new':
                glaze = Glaze(
                    studio_number=glaze_number,
                    name=block['incoming_name'],
                    cone=block['cone'],
                    atmosphere=block['atmosphere'],
                    primary_category=block['category'] or None,
                    status='testing',
                )
                db.session.add(glaze)
                db.session.flush()
                for i, mat in enumerate(block['recipe']):
                    db.session.add(Ingredient(
                        glaze_id=glaze.id,
                        material=mat['material'],
                        amount=mat['amount'],
                        sort_order=i,
                    ))
                glaze_action = 'created'
            else:
                glaze = existing_glaze
                if classification == 'name_mismatch':
                    name_override = (request.form.get(f'name_{glaze_number}') or '').strip()
                    glaze.name = name_override or block['incoming_name']
                    glaze_action = 'name updated'
                else:
                    glaze_action = 'matched'

            tests_created = 0
            tiles_created = 0
            skipped_series = []
            for s in block['series']:
                if not s.get('valid', True):
                    skipped_series.append({'name': s['name'], 'error': s['error']})
                    continue

                existing_test = GlazeTest.query.filter_by(glaze_id=glaze.id, name=s['name']).first()
                if existing_test:
                    for t in existing_test.tiles:
                        db.session.delete(t)
                    db.session.flush()
                    test = existing_test
                    test.variable = s['variable'] or None
                    test.format_type = s['format_type']
                else:
                    test = GlazeTest(
                        glaze_id=glaze.id,
                        name=s['name'],
                        variable=s['variable'] or None,
                        format_type=s['format_type'],
                        test_type='progression_blend',
                        status='planned',
                        description=s['fixed_addition'] or None,
                    )
                    db.session.add(test)
                    db.session.flush()
                    tests_created += 1

                for s_idx, s_check in enumerate(block['series']):
                    if s_check['name'] == s['name']:
                        current_s_idx = s_idx
                        break

                skipped_tiles = []
                for tile_data in s['tiles']:
                    tile_num = tile_data['number']
                    additions_data = tile_data.get('additions_data', [])

                    # Resolve each addition from form choices
                    resolved_additions = []
                    fully_resolved = True
                    for add_idx, add in enumerate(additions_data):
                        if add.get('material_id'):
                            # Already resolved in Phase 1 — no user input needed
                            resolved_additions.append({'material_id': add['material_id'], 'amount': add['amount']})
                            continue

                        field = f'mat_{glaze_number}_{current_s_idx}_{tile_num}_{add_idx}'
                        action = (request.form.get(f'{field}_action') or '').strip()
                        if action == 'existing':
                            existing_id = (request.form.get(f'{field}_existing') or '').strip()
                            if existing_id:
                                resolved_additions.append({'material_id': int(existing_id), 'amount': add['amount']})
                            else:
                                fully_resolved = False
                                break
                        elif action == 'create':
                            mat_name = (request.form.get(f'{field}_create') or '').strip() or add['raw_name']
                            existing_mat = Material.query.filter_by(name=mat_name).first()
                            if existing_mat:
                                mat_id = existing_mat.id
                            else:
                                new_mat = Material(name=mat_name)
                                db.session.add(new_mat)
                                db.session.flush()
                                mat_id = new_mat.id
                            resolved_additions.append({'material_id': mat_id, 'amount': add['amount']})
                        else:
                            fully_resolved = False
                            break

                    if not fully_resolved:
                        skipped_tiles.append(tile_num)
                        continue

                    tile = Tile(
                        test_id=test.id,
                        tile_number=tile_num,
                        additions=tile_data['addition'] or None,
                        cone=block['cone'],
                        atmosphere=block['atmosphere'],
                    )
                    db.session.add(tile)
                    db.session.flush()
                    for add_idx, add in enumerate(resolved_additions):
                        db.session.add(TileAddition(
                            tile_id=tile.id,
                            material_id=add['material_id'],
                            amount=add['amount'],
                            sort_order=add_idx,
                        ))
                    tiles_created += 1

                if skipped_tiles:
                    skipped_series.append({
                        'name': s['name'],
                        'error': f'tiles {skipped_tiles} skipped — unresolved materials',
                    })

            db.session.commit()
            # Access glaze.name after commit (triggers reload) inside try so any
            # session error is caught rather than surfacing as a 500.
            glaze_name = glaze.name
            results.append({
                'glaze_number': glaze_number,
                'name': glaze_name,
                'status': 'imported',
                'glaze_action': glaze_action,
                'tests_created': tests_created,
                'tiles_created': tiles_created,
                'skipped_series': skipped_series,
            })

        except Exception as e:
            db.session.rollback()
            results.append({
                'glaze_number': glaze_number,
                'name': block['incoming_name'],
                'status': 'error',
                'detail': str(e),
            })

    try:
        doc = db.session.get(Document, int(doc_id)) if doc_id else None
    except Exception:
        doc = None
    return render_template('import_doc.html', state='result', results=results, doc=doc)

# ─── INIT ─────────────────────────────────────────────────────────────────────

def init_db():
    with app.app_context():
        db.create_all()
        if Glaze.query.count() == 0:
            from seed_data import seed
            seed(db, Glaze, Ingredient, Material)
            print("Database seeded.")

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000, debug=True)

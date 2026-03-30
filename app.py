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
from models import db, Glaze, Ingredient, Material, GlazeTest, Tile, FiringLog, Fire

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
    # fallback: save locally
    filename = secure_filename(f"tile_{datetime.utcnow().timestamp()}_{file.filename}")
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
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
    search = request.args.get('q', '')
    query = Glaze.query
    if status_filter:
        query = query.filter_by(status=status_filter)
    if tag_filter:
        query = query.filter(Glaze.tags.ilike(f'%{tag_filter}%'))
    if search:
        query = query.filter(
            db.or_(
                Glaze.name.ilike(f'%{search}%'),
                Glaze.studio_number.ilike(f'%{search}%'),
                Glaze.notes.ilike(f'%{search}%')
            )
        )
    all_glazes = query.order_by(Glaze.studio_number).all()
    # Collect all unique tags for filter chips
    all_tags = sorted(set(
        t.strip() for g in Glaze.query.all()
        if g.tags for t in g.tags.split(',') if t.strip()
    ))
    return render_template('glazes.html', glazes=all_glazes, status_filter=status_filter,
                           tag_filter=tag_filter, search=search, all_tags=all_tags)

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
    return render_template('glaze_form.html', glaze=None)

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
    all_tests = GlazeTest.query.order_by(GlazeTest.created_at.desc()).all()
    unassigned_count = GlazeTest.query.filter_by(fire_id=None).count()
    return render_template('tests.html', tests=all_tests, unassigned_count=unassigned_count)

@app.route('/tests/new', methods=['GET', 'POST'])
def new_test():
    glazes = Glaze.query.order_by(Glaze.studio_number).all()
    if request.method == 'POST':
        test = GlazeTest(
            glaze_id=int(request.form['glaze_id']),
            name=request.form['name'],
            description=request.form.get('description', ''),
            test_type=request.form.get('test_type', 'wet_progression'),
            base_batch_size=float(request.form['base_batch_size']) if request.form.get('base_batch_size') else 100,
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
    return render_template('test_detail.html', test=test)

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
    if request.method == 'POST':
        photo_path = upload_photo(request.files.get('photo'))

        tile = Tile(
            test_id=test_id,
            tile_number=int(request.form['tile_number']),
            additions=request.form.get('additions', ''),
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
    return render_template('tile_form.html', test=test, next_tile=next_tile)

@app.route('/tiles/<int:tile_id>/edit', methods=['GET', 'POST'])
def edit_tile(tile_id):
    tile = Tile.query.get_or_404(tile_id)
    if request.method == 'POST':
        new_photo = upload_photo(request.files.get('photo'))
        if new_photo:
            tile.photo_path = new_photo

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
    return render_template('tile_form.html', test=tile.test, tile=tile, next_tile=tile.tile_number)

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
        url = f"https://glazy.org/api/recipes/{glazy_id}"
        req = urllib.request.Request(url, headers={'Accept': 'application/json', 'User-Agent': 'GlazeLab/1.0'})
        with urllib.request.urlopen(req, timeout=8) as resp:
            data = _json.loads(resp.read())
    except Exception as e:
        return jsonify({'error': str(e)}), 502

    # Glazy nests analysis under data.analysis.umf_oxide
    recipe = data.get('data', data)
    analysis = recipe.get('analysis', {})
    umf = analysis.get('umf_oxide', {})
    percent = analysis.get('percent_oxide', {})

    def f(d, key):
        v = d.get(key)
        return round(float(v), 4) if v is not None else None

    r2o = None
    na2o = f(umf, 'Na2O')
    k2o  = f(umf, 'K2O')
    if na2o is not None and k2o is not None:
        total = (na2o or 0) + (k2o or 0)
        ro = round(1 - total, 4)
        r2o = f"{round(total, 4)}:{ro}"

    sio2   = f(umf, 'SiO2')
    al2o3  = f(umf, 'Al2O3')
    sio2_al2o3 = round(sio2 / al2o3, 4) if sio2 and al2o3 else None

    return jsonify({
        'name':           recipe.get('name'),
        'umf_na2o':       na2o,
        'umf_k2o':        k2o,
        'umf_cao':        f(umf, 'CaO'),
        'umf_mgo':        f(umf, 'MgO'),
        'umf_al2o3':      al2o3,
        'umf_sio2':       sio2,
        'umf_b2o3':       f(umf, 'B2O3'),
        'umf_r2o_ro':     r2o,
        'umf_sio2_al2o3': sio2_al2o3,
    })

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

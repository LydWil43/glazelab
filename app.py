import os
from flask import Flask, render_template, request, redirect, url_for, jsonify, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
from datetime import datetime
from models import db, Glaze, Ingredient, Material, GlazeTest, Tile, FiringLog

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

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# ─── ROUTES ──────────────────────────────────────────────────────────────────

@app.route('/')
def index():
    return redirect(url_for('glazes'))

# ─── GLAZES ──────────────────────────────────────────────────────────────────

@app.route('/glazes')
def glazes():
    status_filter = request.args.get('status', '')
    search = request.args.get('q', '')
    query = Glaze.query
    if status_filter:
        query = query.filter_by(status=status_filter)
    if search:
        query = query.filter(
            db.or_(
                Glaze.name.ilike(f'%{search}%'),
                Glaze.studio_number.ilike(f'%{search}%'),
                Glaze.notes.ilike(f'%{search}%')
            )
        )
    glazes = query.order_by(Glaze.studio_number).all()
    return render_template('glazes.html', glazes=glazes, status_filter=status_filter, search=search)

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

# ─── TESTS ───────────────────────────────────────────────────────────────────

@app.route('/tests')
def tests():
    all_tests = GlazeTest.query.order_by(GlazeTest.created_at.desc()).all()
    return render_template('tests.html', tests=all_tests)

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

@app.route('/tests/<int:test_id>/tiles/new', methods=['GET', 'POST'])
def new_tile(test_id):
    test = GlazeTest.query.get_or_404(test_id)
    if request.method == 'POST':
        photo_path = None
        if 'photo' in request.files:
            file = request.files['photo']
            if file and file.filename and allowed_file(file.filename):
                filename = secure_filename(f"tile_{test_id}_{datetime.utcnow().timestamp()}_{file.filename}")
                os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                photo_path = f"uploads/{filename}"

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
        if 'photo' in request.files:
            file = request.files['photo']
            if file and file.filename and allowed_file(file.filename):
                filename = secure_filename(f"tile_{tile_id}_{datetime.utcnow().timestamp()}_{file.filename}")
                os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                tile.photo_path = f"uploads/{filename}"

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

# ─── API ─────────────────────────────────────────────────────────────────────

@app.route('/api/glazes')
def api_glazes():
    glazes = Glaze.query.order_by(Glaze.studio_number).all()
    return jsonify([g.to_dict() for g in glazes])

@app.route('/api/glazes/<int:glaze_id>')
def api_glaze(glaze_id):
    glaze = Glaze.query.get_or_404(glaze_id)
    return jsonify(glaze.to_dict())

# ─── INIT ─────────────────────────────────────────────────────────────────────


@app.before_request
def create_tables():
    db.create_all()
    if Glaze.query.count() == 0:
        from seed_data import seed
        seed(db, Glaze, Ingredient, Material)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

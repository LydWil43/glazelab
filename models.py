from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Glaze(db.Model):
    __tablename__ = 'glazes'
    id = db.Column(db.Integer, primary_key=True)
    studio_number = db.Column(db.String(20), unique=True, nullable=False)
    name = db.Column(db.String(200), nullable=False)
    glazy_id = db.Column(db.String(50))
    cone = db.Column(db.String(50))
    atmosphere = db.Column(db.String(200))
    surface = db.Column(db.String(100))
    transparency = db.Column(db.String(100))
    status = db.Column(db.String(50), default='testing')  # production, testing, draft
    notes = db.Column(db.Text)
    lineage_notes = db.Column(db.Text)
    batch_date = db.Column(db.String(50))
    tags = db.Column(db.String(300))  # comma-separated e.g. "liner,ash,crystalline"
    primary_category = db.Column(db.String(50))
    secondary_category = db.Column(db.String(50))
    # UMF fields
    umf_expansion = db.Column(db.Float)
    umf_r2o_ro = db.Column(db.String(50))
    umf_sio2_al2o3 = db.Column(db.Float)
    umf_na2o = db.Column(db.Float)
    umf_k2o = db.Column(db.Float)
    umf_cao = db.Column(db.Float)
    umf_mgo = db.Column(db.Float)
    umf_al2o3 = db.Column(db.Float)
    umf_sio2 = db.Column(db.Float)
    umf_b2o3 = db.Column(db.Float)
    umf_zro2 = db.Column(db.Float)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    ingredients = db.relationship('Ingredient', backref='glaze', cascade='all, delete-orphan', order_by='Ingredient.sort_order')
    tests = db.relationship('GlazeTest', backref='glaze', cascade='all, delete-orphan')

    def glazy_url(self):
        if self.glazy_id:
            return f"https://glazy.org/recipes/{self.glazy_id}"
        return None

    def to_dict(self):
        return {
            'id': self.id,
            'studio_number': self.studio_number,
            'name': self.name,
            'glazy_id': self.glazy_id,
            'cone': self.cone,
            'atmosphere': self.atmosphere,
            'status': self.status,
            'notes': self.notes,
            'umf_expansion': self.umf_expansion,
            'ingredients': [i.to_dict() for i in self.ingredients]
        }


class Ingredient(db.Model):
    __tablename__ = 'ingredients'
    id = db.Column(db.Integer, primary_key=True)
    glaze_id = db.Column(db.Integer, db.ForeignKey('glazes.id'), nullable=False)
    material = db.Column(db.String(200), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    is_additive = db.Column(db.Boolean, default=False)
    sort_order = db.Column(db.Integer, default=0)

    def to_dict(self):
        return {'material': self.material, 'amount': self.amount, 'is_additive': self.is_additive}


class Material(db.Model):
    __tablename__ = 'materials'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), unique=True, nullable=False)
    price_per_lb = db.Column(db.Float)
    stock_lbs = db.Column(db.Float)
    notes = db.Column(db.Text)
    invoice_date = db.Column(db.String(50))
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'price_per_lb': self.price_per_lb,
            'stock_lbs': self.stock_lbs,
            'notes': self.notes
        }


class Fire(db.Model):
    __tablename__ = 'fires'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    cone = db.Column(db.String(50))
    atmosphere = db.Column(db.String(100))  # reduction, oxidation, neutral, wood
    status = db.Column(db.String(50), default='planning')  # planning, fired, archived
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    tests = db.relationship('GlazeTest', backref='fire', lazy=True)


class GlazeTest(db.Model):
    __tablename__ = 'glaze_tests'
    id = db.Column(db.Integer, primary_key=True)
    glaze_id = db.Column(db.Integer, db.ForeignKey('glazes.id'), nullable=False)
    fire_id = db.Column(db.Integer, db.ForeignKey('fires.id'), nullable=True)
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    test_type = db.Column(db.String(50))  # wet_progression, discrete_batch
    base_batch_size = db.Column(db.Float)
    status = db.Column(db.String(50), default='planned')  # planned, mixed, fired, complete
    progression_plan = db.Column(db.Text)  # JSON: {headers, rows, note}
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    tiles = db.relationship('Tile', backref='test', cascade='all, delete-orphan', order_by='Tile.tile_number')


class Tile(db.Model):
    __tablename__ = 'tiles'
    id = db.Column(db.Integer, primary_key=True)
    test_id = db.Column(db.Integer, db.ForeignKey('glaze_tests.id'), nullable=False)
    tile_number = db.Column(db.Integer, nullable=False)
    additions = db.Column(db.Text)  # description of what was added for this tile
    thickness = db.Column(db.Integer)  # 1-10
    wood_ash_on_top = db.Column(db.Boolean, default=False)
    # Firing notes
    atmosphere = db.Column(db.String(100))
    cone = db.Column(db.String(50))
    body_reduction = db.Column(db.String(50))  # light, medium, heavy
    glaze_reduction = db.Column(db.String(50))  # light, medium, heavy
    cooling = db.Column(db.String(100))
    # Results
    result_notes = db.Column(db.Text)
    photo_path = db.Column(db.String(500))
    fired_at = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'tile_number': self.tile_number,
            'additions': self.additions,
            'thickness': self.thickness,
            'wood_ash_on_top': self.wood_ash_on_top,
            'atmosphere': self.atmosphere,
            'cone': self.cone,
            'body_reduction': self.body_reduction,
            'glaze_reduction': self.glaze_reduction,
            'cooling': self.cooling,
            'result_notes': self.result_notes,
            'photo_path': self.photo_path
        }


class FiringLog(db.Model):
    __tablename__ = 'firing_logs'
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, nullable=False)
    cone = db.Column(db.String(50))
    atmosphere = db.Column(db.String(100))
    body_reduction = db.Column(db.String(50))
    glaze_reduction = db.Column(db.String(50))
    cooling = db.Column(db.String(100))
    kiln_notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

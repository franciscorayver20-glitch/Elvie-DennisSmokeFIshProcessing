from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(500))
    first_name = db.Column(db.String(150))
    is_admin = db.Column(db.Boolean, default=False)
    # REAL TIME TRACKING
    date_created  = db.Column(db.DateTime(timezone=True), default=func.now())
    last_login    = db.Column(db.DateTime(timezone=True), nullable=True)
    is_online     = db.Column(db.Boolean, default=False)
    last_updated = db.Column(db.DateTime(timezone=True), nullable=True)
    # Update Password Token
    reset_token    = db.Column(db.String(100), unique=True, nullable=True)
    token_expiry   = db.Column(db.DateTime(timezone=True), nullable=True)

    transactions = db.relationship('Transaction', backref='staff_member', lazy=True)

class Product(db.Model):
    """Master product catalog — name, price, unit, category only."""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    price = db.Column(db.Float, nullable=False)
    unit = db.Column(db.String(50), default="kg")
    category = db.Column(db.String(100), default="Uncategorized")
    date_updated = db.Column(db.DateTime(timezone=True), default=func.now(), onupdate=func.now())
    last_modified = db.Column(db.DateTime(timezone=True), default=func.now(), onupdate=func.now())

# NEW: Per-sheet product stock entry
class SheetProduct(db.Model):
    __tablename__ = 'sheet_product'

    """Tracks stock per product per ProductSheet."""
    id = db.Column(db.Integer, primary_key=True)
    sheet_id = db.Column(db.Integer, db.ForeignKey('product_sheet.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    stock = db.Column(db.Integer, default=0)
    status = db.Column(db.String(50), default="On Stock")
    last_modified = db.Column(db.DateTime(timezone=True), default=func.now(), onupdate=func.now())

    product = db.relationship('Product')
    sheet   = db.relationship('ProductSheet', back_populates='sheet_products')

    __table_args__ = (
        db.UniqueConstraint('sheet_id', 'product_id', name='unique_sheet_product'),
    )

class ProductSheet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(20), nullable=False)
    label = db.Column(db.String(50), nullable=False)
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())
    sheet_products = db.relationship('SheetProduct', back_populates='sheet',
                                     lazy=True, cascade='all, delete-orphan')
    snapshots = db.relationship('ProductSnapshot', backref='sheet',
                                lazy=True, cascade='all, delete-orphan')
    is_active = db.Column(db.Boolean, default=True)

class ProductSnapshot(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sheet_id = db.Column(db.Integer, db.ForeignKey('product_sheet.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=True)
    name = db.Column(db.String(150))
    price = db.Column(db.Float)
    stock = db.Column(db.Integer)
    unit = db.Column(db.String(50))
    category = db.Column(db.String(100))
    status = db.Column(db.String(50))
    last_modified = db.Column(db.DateTime(timezone=True), default=func.now())

class Sheet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(20), nullable=False)
    label = db.Column(db.String(50), nullable=False)
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())
    last_modified = db.Column(db.DateTime(timezone=True), default=func.now(), onupdate=func.now())
    # Link to the ProductSheet of the same date
    product_sheet_id = db.Column(db.Integer, db.ForeignKey('product_sheet.id'), nullable=True)
    transactions = db.relationship('Transaction', backref='sheet', lazy=True)
    is_active = db.Column(db.Boolean, default=True)

class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    box_name = db.Column(db.String(50))
    product_name = db.Column(db.String(150))
    quantity = db.Column(db.Integer)
    total_price = db.Column(db.Float)
    status = db.Column(db.String(50), default="Initialized")
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())
    last_modified = db.Column(db.DateTime(timezone=True), default=func.now(), onupdate=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))
    sheet_id = db.Column(db.Integer, db.ForeignKey('sheet.id'), nullable=True)
    items = db.relationship('TransactionItem', backref='transaction',
                            lazy=True, cascade='all, delete-orphan')

class TransactionItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    transaction_id = db.Column(db.Integer, db.ForeignKey('transaction.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False, default=1)
    unit_price = db.Column(db.Float, nullable=False, default=0.0)
    product = db.relationship('Product')

class Personnel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150))
    phone = db.Column(db.String(20))
    role = db.Column(db.String(100), default="Delivery")
    status = db.Column(db.String(50), default="Available")
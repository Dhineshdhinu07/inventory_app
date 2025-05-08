from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Product(db.Model):
    __tablename__ = 'products'
    
    product_id = db.Column(db.String(20), primary_key=True)
    product_name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<Product {self.product_id}>'


class Location(db.Model):
    __tablename__ = 'locations'
    
    location_id = db.Column(db.String(20), primary_key=True)
    location_name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<Location {self.location_id}>'


class ProductMovement(db.Model):
    __tablename__ = 'product_movements'
    
    movement_id = db.Column(db.String(20), primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    from_location = db.Column(db.String(20), db.ForeignKey('locations.location_id'), nullable=True)
    to_location = db.Column(db.String(20), db.ForeignKey('locations.location_id'), nullable=True)
    product_id = db.Column(db.String(20), db.ForeignKey('products.product_id'), nullable=False)
    qty = db.Column(db.Integer, nullable=False)
    
    # Define relationships
    product = db.relationship('Product', backref=db.backref('movements', lazy=True))
    source = db.relationship('Location', foreign_keys=[from_location], backref=db.backref('outgoing_movements', lazy=True))
    destination = db.relationship('Location', foreign_keys=[to_location], backref=db.backref('incoming_movements', lazy=True))
    
    def __repr__(self):
        return f'<ProductMovement {self.movement_id}>'
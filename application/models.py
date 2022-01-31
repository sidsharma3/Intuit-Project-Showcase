from . import db
from sqlalchemy.sql import func
from flask_login import UserMixin
# These are the database models as we can see the relationship
# between Inventory and InventoryItems is One to Many
class InventoryItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    quantity = db.Column(db.Integer)
    name = db.Column(db.String(100))
    description = db.Column(db.String(500))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    inventoryId = db.Column(db.Integer, db.ForeignKey('inventory.id'))
    userId = db.Column(db.Integer, db.ForeignKey('user.id'))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    isAdmin = db.Column(db.Boolean, default=False)
    items = db.relationship('InventoryItem')

class Inventory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    allInventoryItems = db.relationship('InventoryItem')
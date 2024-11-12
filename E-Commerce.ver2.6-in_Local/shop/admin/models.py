from shop import db
from flask_login import UserMixin

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(180), nullable=False)
    role = db.Column(db.String(20), default='customer')  # 'admin' or 'customer'
    profile = db.Column(db.String(180), default='profile.jpg')
    # Customer specific fields
    country = db.Column(db.String(50))
    state = db.Column(db.String(50))
    city = db.Column(db.String(50))
    contact = db.Column(db.String(50))
    address = db.Column(db.String(200))

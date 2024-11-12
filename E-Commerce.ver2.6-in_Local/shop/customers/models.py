from shop import db, login_manager
from datetime import datetime
from flask_login import UserMixin

@login_manager.user_loader
def user_loader(user_id):
    return RegisterModel.query.get(user_id)

class RegisterModel(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=False)
    username = db.Column(db.String(64), unique=True)
    email = db.Column(db.String(64), unique=True)
    password = db.Column(db.String(128), unique=False)
    country = db.Column(db.String(50), unique=False)
    state = db.Column(db.String(50), unique=False)
    city = db.Column(db.String(50), unique=False)
    address = db.Column(db.String(256), unique=False)
    contact = db.Column(db.String(16), unique=False)
    role = db.Column(db.String(20), default='customer')
    profile_image = db.Column(db.String(128), unique=False, default='profile.jpg')
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.now())

    def __repr__(self):
        return '<Register %r>' % self.name

class CustomerOrder(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('register_model.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    date_added = db.Column(db.DateTime, nullable=False, default=datetime.now())
    status = db.Column(db.String(20), default='in_cart')  # 'in_cart' hoặc 'removed'

    customer = db.relationship('RegisterModel', backref=db.backref('orders', lazy=True))
    product = db.relationship('Product', backref=db.backref('orders', lazy=True))


db.create_all()

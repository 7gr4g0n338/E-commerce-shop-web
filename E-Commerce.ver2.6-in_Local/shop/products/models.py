from shop import db
from datetime import datetime


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    price = db.Column(db.Numeric(10,2), nullable=False)
    stock = db.Column(db.Integer, nullable=False)
    desc = db.Column(db.Text, nullable=False)
    pub_date = db.Column(db.DateTime, nullable=False,default=datetime.now())
    brand_id = db.Column(db.Integer, db.ForeignKey('brand.id'),nullable=False)
    # db.relationship('Brand') có nghĩa là khi nào Product.brand thì sẽ trả về đối tượng brand. ví dụ air_max = Product(name="Nike Air Max", brand=nike, price=100) => print(air_max.brand.name)  # In ra: "Nike"

    # từ brand lấy ra tất cả các sản phẩm có trong brand đó. biết có nike = Brand(name="Nike") => nike_products = nike.brand  # Trả về list [tên sản phẩm 1, 2, 3...]
    brand = db.relationship('Brand', backref=db.backref('brand', lazy=True))
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'),nullable=False)
    category = db.relationship('Category' , backref=db.backref('category', lazy=True))

    image_1 = db.Column(db.String(256), nullable=False, default='image1.jpg')

    def __repr__(self):
        return '<Product %r>' % self.name

class Brand(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False, unique=True)

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False, unique=True)

db.create_all()
from flask_wtf.file import FileAllowed, FileField, FileRequired
from wtforms import Form,StringField, IntegerField, BooleanField, TextAreaField, validators, DecimalField

class AddProducts(Form):
    name = StringField("Tên sản phẩm", [validators.DataRequired()])
    price = IntegerField("Giá", [validators.DataRequired()])
    stock = IntegerField("Số lượng sản phẩm đang có", [validators.DataRequired()])
    desc = TextAreaField("Mô tả", [validators.DataRequired()])
    # colors = TextAreaField("Colors", [validators.DataRequired()])

    image_1 = FileField('Hình ảnh', validators=[FileAllowed(['jpg', 'jpeg', 'png', 'svg', 'gif'], "Images Only please")])

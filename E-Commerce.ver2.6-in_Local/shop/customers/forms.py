from wtforms import StringField, TextAreaField, PasswordField, SubmitField, IntegerField, validators, Form, ValidationError
from flask_wtf.file import FileRequired, FileAllowed, FileField
from flask_wtf import FlaskForm
from .models import RegisterModel

class CustomerRegistrationForm(FlaskForm):
    name = StringField('Nhập tên của bạn', [validators.DataRequired()])
    username = StringField('Tên tài khoản', [validators.DataRequired()])
    email = StringField("Email", validators=[validators.Email(), validators.DataRequired()])
    password = PasswordField('Nhập mật khẩu', [validators.DataRequired(), validators.EqualTo('confirm', message="Both passwords should match")])
    confirm = PasswordField("Nhập lại mật khẩu", [validators.DataRequired()])    
    country = StringField('Quốc gia', [validators.DataRequired()])
    state = StringField('Tỉnh/ Thành phố', [validators.DataRequired()])
    city = StringField('Quận/ Huyện/ Thị xã', [validators.DataRequired()])
    contact = StringField('Số điện thoại', [validators.DataRequired()])
    address = StringField('Địa chỉ Xóm/ Thôn/ Xã', [validators.DataRequired()])

    profile_image = FileField("Ảnh đại diện", validators=[FileAllowed(['jpg', 'png', 'jpeg'], "Images only")])
    
    submit = SubmitField("Đăng ký")

    def validate_username(self, username):
        if RegisterModel.query.filter_by(username=username.data).first():
            raise ValidationError("Tên tài khoản đã tồn tại.")

    def validate_email(self, email):
        if RegisterModel.query.filter_by(email=email.data).first():
            raise ValidationError("Tên Email đã tồn tại.")

class CustomerLoginForm(FlaskForm):
    email = StringField("Email", [validators.DataRequired()])
    password = PasswordField('Password', [validators.DataRequired()])

class CustomerUpdateForm(FlaskForm):
    name = StringField('Tên người dùng', validators=[validators.DataRequired()])
    username = StringField('Tên tài khoản',validators=[validators.DataRequired()])
    email = StringField('Email', validators=[validators.DataRequired(), validators.Email()])
    contact = StringField('Số điện thoại', validators=[validators.DataRequired()])
    address = StringField('Địa chỉ Xóm/ Hẻm, Làng/ Ngõ, Xã/ Phố', validators=[validators.DataRequired()])
    city = StringField('Quận/ Huyện/ Thị xã', validators=[validators.DataRequired()])
    state = StringField('Tỉnh/ Thành phố', validators=[validators.DataRequired()])
    country = StringField('Quốc gia', validators=[validators.DataRequired()])
    submit = SubmitField('Cập nhật thông tin cá nhân')

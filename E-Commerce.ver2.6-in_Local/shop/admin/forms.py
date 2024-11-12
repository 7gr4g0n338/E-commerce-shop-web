from wtforms import StringField, Form, StringField, ValidationError, PasswordField, validators

class RegistrationForm(Form):
    name = StringField("Tên quản trị viên", [validators.Length(min=3, max=40)])
    username = StringField("Tên tài khoản", [validators.Length(min=4, max=25)])
    email = StringField("Email", [validators.Length(min=6, max=64), validators.Email()])
    password = PasswordField("Nhập Mật khẩu", [
        validators.DataRequired(),
        validators.EqualTo('confirm', message="Mật khẩu phải khớp với mật khẩu vừa nhập")
    ])
    confirm = PasswordField("Nhập lại mật khẩu")
    role = StringField("Role", default='admin')


class LoginForm(Form):
    email = StringField("Email", [validators.Length(min=6, max=64), validators.Email()])
    password = PasswordField("Password", [validators.DataRequired()])
# File này đóng vai trò là điểm khởi đầu khi ứng dụng chạy và là nơi tập trung các cấu hình quan trọng của hệ thống.

# Import các thư viện cần thiết
import os
from flask import Flask, session  # Framework web chính
from flask_sqlalchemy import SQLAlchemy  # ORM để làm việc với database
from flask_bcrypt import Bcrypt  # Thư viện mã hóa password
from flask_uploads import IMAGES, UploadSet, configure_uploads  # Xử lý upload ảnh
from flask_login import LoginManager  # Quản lý đăng nhập/xác thực
from flask_migrate import Migrate  # Quản lý migration database

# Khởi tạo ứng dụng Flask
app = Flask(__name__)

# PHẦN 1: CẤU HÌNH DATABASE
app.config["SECRET_KEY"] = "1234567890098765412345678"  # Key bí mật cho session/cookie
basedir = os.path.abspath(os.path.dirname(__file__))  # Lấy đường dẫn thư mục hiện tại
# Cấu hình SQLite database
app.config["SQLALCHEMY_DATABASE_URI"] =  'sqlite:///'+ os.path.join(basedir, 'myshop.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)  # Khởi tạo database

@app.before_first_request
def clear_all_sessions():
    session.clear()

# PHẦN 2: XỬ LÝ UPLOAD ẢNH
# Cấu hình thư mục lưu ảnh upload
app.config['UPLOADED_PHOTOS_DEST'] = os.path.join(basedir, 'static/images')
photos = UploadSet('photos', IMAGES)  # Tạo upload set cho ảnh
configure_uploads(app, photos)  # Cấu hình upload

# PHẦN 3: MIGRATION DATABASE
migrate = Migrate(app, db)
with app.app_context():
    # Xử lý đặc biệt cho SQLite
    if db.engine.url.drivername == 'sqlite':
        migrate.init_app(app,db, render_as_batch=True)
    else:
        migrate.init_app(app,db)

# PHẦN 4: QUẢN LÝ ĐĂNG NHẬP
login_manager = LoginManager()  # Khởi tạo login manager
login_manager.init_app(app)
login_manager.login_view = 'customerLogin'  # Route mặc định khi cần login
login_manager.needs_refresh_message_category = 'danger'
login_manager.login_message = u"Please Login Sir/ Madam"  # Thông báo yêu cầu đăng nhập

# PHẦN 5: MÃ HÓA MẬT KHẨU
bcrypt = Bcrypt(app)  # Khởi tạo bcrypt để hash password

# PHẦN 6: IMPORT CÁC ROUTES
# Import các blueprint routes từ các module khác nhau
from shop.admin import routes
from shop.products import routes
from shop.carts import carts
from shop.customers import routes
from shop.errors import errors
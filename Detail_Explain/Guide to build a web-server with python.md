# Guide to build web-server by python
https://github.com/ChiragSaini/E-Commerce-Using-Flask

Mục lục:
1. [Install and built up again E-commerce in local environment](#install-and-built-up-again-e-commerce-in-local-environment)
2. [Install and build up in cloud aws](#install-and-build-up-in-cloud-aws)
3. [How to read understood-code](#how-to-read-understood-code)

## Install and built up again E-commerce in local environment
### Fix  bug for environment
+ download python 3.6.5
+ download sqlite3: https://www.sqlitetutorial.net/download-install-sqlite/

vì các version trong code đều dùng bản cũ nên cần cài đúng bản để chúng tương thích với nhau:
+ pip install flask_bcrypt
+ pip install flask==2.1.3 werkzeug==2.0.3
+ pip install flask_login
+ pip install sqlalchemy==1.4.46 flask-sqlalchemy==2.5.1
+ pip install wtforms

### Fix bug for code
code trong file forms.py của shop folder sai cách định nghĩa các extention cần sửa:
```markdown
image_1 = FileField('Image 1', validators=[FileAllowed(['jpg, jpeg, png, svg, gif']), "Images Only please"])
```
thành:
> image_1 = FileField('Image 1', validators=[FileAllowed(['jpg', 'jpeg', 'png', 'svg', 'gif'], "Images Only please")])


## Install and build up in cloud aws

### Hiểu tổng quát về cách triển khai code lên EC2
+ Để build được production thì cần 4 thành phần chính hoạt động tương tác với nhau: Client <--> Nginx <--> Gunicorn(WSGI Application server) <--> Flask Framework(Python code).

    + Nginx: để reveser proxy, điều hướng request từ port 80 vào localhost để Gunicorn dùng WSGI đưa nó tới Python app xử lí request.
    + Gunicorn: giống như 1 server chạy service của app
    + Flask - Python: xử lí yêu cầu, tương tác với database và phản hồi kết quả về.

reference: https://dieg.info/en/articles-en/hosting-for-python-en/ 

### Thêm các file cấu hình cho reverse proxy và gunicorn

+ file gunicorn_conf.py
```markdown
workers = 3
bind = "0.0.0.0:5000"
timeout = 120

```

+ file run.py
```markdown
from shop import app

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)

```

+ file config.py
```markdown
class Config:
    SECRET_KEY = '1234567890098765412345678'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///shop.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
class ProductionConfig(Config):
    DEBUG = False

```

+ trong file __init__.py của /shop

bỏ funcntion: patch_request_class(app) và nơi import nó trong file này.

+ thêm file requirements.txt để lên linux trên EC2 còn cài đặt môi trường
```markdown
alembic==1.13.3
bcrypt==4.2.0
blinker==1.8.2
click==8.1.7
colorama==0.4.6
distlib==0.3.9
dnspython==2.7.0
email_validator==2.2.0
filelock==3.16.1
Flask==2.1.3
Flask-Bcrypt==1.0.1
Flask-Login==0.6.3
Flask-Migrate==4.0.7
Flask-SQLAlchemy==2.5.1
Flask-Uploads==0.2.1
Flask-WTF==1.2.2
greenlet==3.1.1
idna==3.10
itsdangerous==2.2.0
Jinja2==3.1.4
Mako==1.3.6
MarkupSafe==3.0.2
platformdirs==4.3.6
SQLAlchemy==1.4.46
typing_extensions==4.12.2
virtualenv==20.27.0
Werkzeug==2.0.3
WTForms==3.2.1
gunicorn==20.1.0
Flask-Reuploaded==1.2.0

```

### Cài đặt môi trường để chạy trên aws

#### Đẩy folder code lên EC2
> scp -r -i ./.ssh/pieces.pem /folder name@ip_EC2:~/folder/to/saved


Ví dụ:
> scp -r -i ~/.ssh/pieces.pem ~/Desktop/E-Commerce.ver2.3-Modify_display_language_in_Cloud ubuntu@47.128.254.252:~/web-server/


#### Cài đặt môi trường
+ cài đặt python 3.11 để tương thích với các thư viện trong code:
Dùng python3.11 để tạo môi trường ảo trong thư mục chính của project:
> python3.11 -m venv venv
> source venv/bin/activate
> pip install -r requirements.txt

+ tạo serice flask-shop để chạy dịch vụ:
> sudo nano /etc/systemd/system/flask-shop.service

thêm vào đoạn code sau:
```markdown
[Unit]
Description=Flask Shop
After=network.target

[Service]
User=ubuntu
WorkingDirectory=/home/ubuntu/web-server
Environment="PATH=/home/ubuntu/web-server/venv/bin"
ExecStart=/home/ubuntu/web-server/venv/bin/gunicorn -c gunicorn_config.py run:app

[Install]
WantedBy=multi-user.target
```

Sau khi thêm file cấu hình này trên terminal của EC2 xong thì reload lại deamon và start service:
> sudo systemctl daemon-reload

> sudo systemctl enable flask-shop

> sudo systemctl start flask-shop

> sudo systemctl status flask-shop

restart lại bằng lệnh sau:
> sudo systemctl restart flask-shop

check chi tiết log của service:
> sudo journalctl -u flask-shop -n 50

+ cấu hình ngix để điều hướng tất cả các request từ port 80 đến port 5000 của EC2

> sudo nano /etc/nginx/sites-available/flask-shop

thêm đoạn code sau vào file cấu hình nginx:
```markdown
server {
    listen 80;
    server_name 13.250.43.174;

    location / {
        proxy_pass http://localhost:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

> sudo ln -s /etc/nginx/sites-available/flask-shop /etc/nginx/sites-enabled/

> sudo nginx -t

> sudo systemctl restart nginx

> sudo systemctl status nginx

Kiểm tra xem đã start ngix thành công chưa:
> curl localhost

check log của nginx:
> sudo tail -f /var/log/nginx/error.log

> sudo tail -f /var/log/nginx/access.log

+ cấu hình ngix để điều hướng tất cả các request từ port 443 đến port 5000 của EC2:
> sudo nano /etc/nginx/sites-available/flask-shop

```markdown
server {
    listen 80;
    server_name 13.250.42.80;
    return 301 https://$server_name$request_uri;
}
server {
    listen 443 ssl;
    server_name 13.250.42.80;

    ssl_certificate /etc/nginx/ssl/self-signed.crt;
    ssl_certificate_key /etc/nginx/ssl/self-signed.key;
   
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;

    location / {
        proxy_pass http://localhost:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}

```

Tạo key và certificate để sử dụng cho https:
> sudo mkdir -p /etc/nginx/ssl

> sudo openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout /etc/nginx/ssl/self-signed.key -out /etc/nginx/ssl/self-signed.crt

Phải điền chứng chỉ hợp lệ, nếu không có thì dùng tạm test:
```markdown
Country Name (2 letter code) [AU]: VN
State or Province Name: Hanoi  
Locality Name: Cau Giay
Organization Name: My Company
Organizational Unit Name: IT Department
Common Name: 13.250.42.80
Email Address: admin@mycompany.com
```

AI gợi ý:
```markdown
Có 2 lựa chọn chính để có chứng chỉ SSL hợp lệ:

Let's Encrypt - Miễn phí và rất phổ biến:
Tự động gia hạn mỗi 90 ngày
Được tin cậy bởi hầu hết các trình duyệt
Cần có domain name

Chứng chỉ thương mại từ các nhà cung cấp:
Comodo
DigiCert
GeoTrust
Có phí hàng năm
Hỗ trợ kỹ thuật chuyên nghiệp
Bảo hiểm bảo mật

Với dự án của bạn, Let's Encrypt là lựa chọn tốt nhất vì:
Hoàn toàn miễn phí
Dễ cài đặt và tự động gia hạn
Đủ tin cậy cho website thương mại
Bước tiếp theo sẽ là đăng ký domain name và cấu hình Let's Encrypt.
```

> sudo nginx -t

> sudo systemctl restart nginx

Kiểm tra port 443 đã được dùng chưa:
> sudo netstat -tulpn | grep :443




#### Lệnh chạy ngầm app trên terminal của EC2
> sudo systemctl enable nginx && sudo systemctl start nginx && sudo systemctl enable flask-shop && sudo systemctl start flask-shop

#### Dừng service
> sudo systemctl stop nginx && sudo systemctl stop flask-shop

Kiểm tra service đã dừng chưa:
> sudo systemctl status nginx

> sudo systemctl status flask-shop

#### Tắt dịch vụ
> sudo systemctl stop nginx && sudo systemctl disable nginx && sudo systemctl stop flask-shop && sudo systemctl disable flask-shop



## How to read understood-code

### Cách Flask tổ chức code theo mô hình MVC để xây dựng ứng dụng web có cấu trúc tốt và dễ quản lý.
#### Mô hình web MVC - Model-View-Controller:

Model(mô hình dữ liệu): 
+ định nghĩa cấu trúc dữ liệu và logic nghiệp vụ
+ Ví dụ: Product model định nghĩa một sản phẩm có id, tên, giá, số lượng, mô tả
+ Tương tác trực tiếp với database

View (Giao diện):
+ hiển thị dữ liệu cho người dùng
+ Sử dụng template engine Jinja2 để render dữ liệu
+ Không chứa logic xử lý

Controller (điều khiển):
+ xử lý request từ người dùng
+ Tương tác với Model để lấy/cập nhật dữ liệu
+ Chọn View phù hợp để hiển thị

Ví dụ: trong code thì các file routes.py là controller, các file template như .html là view, các file models.py là model. còn các file forms.py chỉ đơn giản là định nghĩa các form để quy định các trường dữ liệu.

#### Ưu điểm của MVC:
+ Tách biệt các thành phần
+ Dễ bảo trì, mở rộng
+ Tái sử dụng code
+ Phân chia trách nhiệm rõ ràng

### Cách ứng dụng web-server này hoạt động, các luồng đi như thế nào trong code ở folder hiện tại.

Cách hoạt động của ứng dụng E-Commerce Flask này:
1. Cấu trúc chính:
Ứng dụng được chia thành các module riêng biệt: admin, carts, customers, products
Mỗi module có các file forms.py để xử lý form và validation

2. Luồng xử lý chính:
ĐĂNG KÝ/ĐĂNG NHẬP:

Khách hàng đăng ký qua CustomerRegistrationForm với các trường thông tin cơ bản
Đăng nhập qua CustomerLoginForm với email
Admin có form đăng ký/đăng nhập riêng (RegistrationForm, LoginForm)

GIỎ HÀNG:

Sử dụng session để lưu giỏ hàng (shopcart)
Khi thêm sản phẩm (add_cart):
Kiểm tra sản phẩm đã có trong giỏ chưa
Nếu có thì tăng số lượng
Nếu chưa thì thêm mới vào session
Có các chức năng:
Xem giỏ hàng (get_cart)
Xóa giỏ hàng (clearcart)
Làm trống session (empty_cart)

SẢN PHẨM:

Thêm sản phẩm qua form AddProducts với các thông tin: tên, giá, số lượng, mô tả
Sử dụng SQLAlchemy để tương tác với database

MIGRATIONS:

Sử dụng Alembic để quản lý schema database
Có 2 mode chạy migration: online và offline

3. Các điểm quan trọng:
Sử dụng Flask-WTF để xử lý form và validation
Lưu trữ giỏ hàng trong session
Có xử lý upload ảnh cho profile
Kiểm tra trùng lặp username/email khi đăng ký
Tính toán tổng tiền giỏ hàng


Đây là một ứng dụng Flask cơ bản nhưng đã implement đầy đủ các chức năng chính của một website thương mại điện tử.

### Cách đọc code logic và dễ hiểu nhất.

1. Bắt đầu từ README.md
Giúp hiểu tổng quan về ứng dụng
Nắm được các tính năng đã implement
Biết được công nghệ sử dụng

2. Cấu trúc Database và Models
Đọc migrations/env.py để hiểu cấu hình database
Xem các model classes để nắm cấu trúc dữ liệu

Quá trình migration là cách quản lý và thực hiện các thay đổi cấu trúc database một cách có tổ chức.

Mục đích của migration:
+ Theo dõi thay đổi schema database
+ Đồng bộ cấu trúc database giữa các môi trường
+ Dễ dàng rollback khi cần
+ Làm việc nhóm hiệu quả

3. Forms và Validation
Đọc các file forms.py trong từng module:
+ customers/forms.py: form đăng ký/đăng nhập của khách hàng
+ admin/forms.py: form quản lý của admin
+ products/forms.py: form thêm/sửa sản phẩm

4. Core Business Logic
Module carts/carts.py:
+ Hiểu cách quản lý giỏ hàng qua session
+ Các hàm xử lý thêm/xóa/sửa giỏ hàng

5. Luồng xử lý chính:
Luồng đăng ký/đăng nhập
Luồng thêm sản phẩm vào giỏ
Luồng thanh toán
Luồng quản lý của admin

6. Templates và Static files
Xem cấu trúc HTML/CSS
Hiểu luồng render dữ liệu

7. Configuration và Utils
Các file config
Các hàm tiện ích

Sử dụng debugger để theo dõi luồng chạy
Vẽ sơ đồ để hình dung rõ hơn
Chạy thử từng chức năng để hiểu code
Đọc documentation của Flask song song

Cách tiếp cận này giúp hiểu được:

Kiến trúc tổng thể của ứng dụng
Cách các module tương tác
Business logic chính
Best practices trong lập trình web với Flask

#### Mối quan hệ giữa các thành phần

vậy sqlalchemy, alembic và sqlite có mối quan hệ như thế nào?

Python Code -> SQLAlchemy -> SQLite Database
                  ↑
               Alembic

SQLAlchemy làm việc trực tiếp với SQLite

Alembic theo dõi SQLAlchemy models và tạo migrations

Khi chạy migration, Alembic sẽ thông qua SQLAlchemy để thực hiện thay đổi trên SQLite




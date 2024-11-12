# Technical specification document

Mục lục
1. [Mô tả tổng quan kỹ thuật](#1-mô-tả-tổng-quan-kỹ-thuật)
2. [Kiến trúc hệ thống](#2-kiến-trúc-hệ-thống)
3. [Luồng xử lý chính](#3-luồng-xử-lý-chính)
4. [Giao diện lập trình ứng dụng (API)](#4-giao-diện-lập-trình-ứng-dụng-api)
5. [Thiết kế cơ sở dữ liệu](#5-thiết-kế-cơ-sở-dữ-liệu)
6. [Yêu cầu hạ tầng và môi trường triển khai](#6-yêu-cầu-hạ-tầng-và-môi-trường-triển-khai)
7. [Quy trình xử lý lỗi và bảo mật](#7-quy-trình-xử-lý-lỗi-và-bảo-mật)
8. [Chi tiết về kiểm thử kỹ thuật](#8-chi-tiết-về-kiểm-thử-kỹ-thuật)
9. [Yêu cầu và quy trình triển khai](#9-yêu-cầu-và-quy-trình-triển-khai)

## 1. Mô tả tổng quan kỹ thuật
Hệ thống dùng kiến trúc mô hình MVC (Model-View-Controller) để tách biệt logic ứng dụng từ giao diện người dùng. Mô hình này giúp quản lý và duy trì dễ dàng các thành phần của ứng dụng. Mục tiêu để dễ dàng mở rộng và bảo trì ứng dụng.

+ Các công nghệ sử dụng: 
   + Python và Flask framework để xây dựng ứng dụng web.
   + Sqlite3 làm cơ sở dữ liệu.
   + jinja2 làm template engine.
   + Bootstrap làm framework css.

+ Các thành phần chính:
   + Model: là các file models.py chứa các class định nghĩa các bảng trong cơ sở dữ liệu.
   + View: là các file html định nghĩa các giao diện người dùng.
   + Controller: là các file routes.py định nghĩa các hàm xử lý các yêu cầu từ người dùng. ngoài ra còn forms.py định nghĩa các form để xử lý dữ liệu.

## 2. Kiến trúc hệ thống

### 2.1. Frontend Layer

- Templates structure:
    + Base layout (layout.html)
    + Navigation components (navbar.html, icon_navbar.html)
    + Form helpers (_formhelpers.html)
    + Message display (_messages.html)
    + Content wrapper (content-wrapper.html)
- Static assets:
    + Product images
    + Logo assets
    + About page media

### 2.2. Application Layer

- Admin Module:
    + User management
    + Product management
    + Order processing
    + System configuration

- Products Module:
    + Product CRUD operations
    + Category management
    + Image handling
    + Product search/filter

- Customers Module:
    + Authentication
    + Profile management
    + Order history
    + Address management

- Cart Module:
    + Session-based cart
    + Price calculations
    + Quantity management
    + Checkout process

### 2.3. Data Layer:

- SQLite database (myshop.db)
- Models:
    + Product models
    + User models
    + Order models
    + Cart models

## 3. Luồng xử lý chính
### 3.1 Product Flow:
+ Product listing → Product detail → Add to cart → Checkout

+ Admin: Product creation → Image upload → Category assignment → Publication

### 3.2 User Flow:
+ Registration → Login → Profile management → Order placement

+ Admin: User creation → Role assignment → Permission management

### 3.3 Cart Flow:
+ Add product → Update quantity → Calculate totals → Checkout process

## 4. Giao diện lập trình ứng dụng (API)
### 4.1. API Documents
#### Admin Routes:
- User management endpoints
- Product management endpoints
- Order processing endpoints

 | Method | API | Parameters | Description | 
 |--------|-----|------------|-------------| 
 | GET/POST | /admin/login | email, password | Xác thực đăng nhập admin | 
 | GET/POST | /admin/register | name, username, email, password | Đăng ký tài khoản admin mới | 
 | GET | /admin | None | Trang quản trị chính | 
 | GET | /admin/brands | None |Quản lý danh sách thương hiệu |
 | GET | /admin/categories | None | Quản lý danh mục sản phẩm |
 | GET | /admin/users | None | Xem danh sách người dùng | 
 | POST | /admin/delete_user/int:id | id | Xóa người dùng khỏi hệ thống | 
 | GET | /admin/search | q, type, page | Tìm kiếm người dùng/sản phẩm | 
 | GET/POST | /admin/addproduct | name, price, stock, desc, brand, category, image_1 | Thêm sản phẩm mới | 
 | GET/POST | /admin/updateproduct/int:id | name, price, stock, desc, brand, category, image_1 | Cập nhật thông tin sản phẩm | 
 | POST | /admin/deleteproduct/int:id | id | Xóa sản phẩm |

#### Product Routes:

- Product CRUD endpoints
- Category management
- Search and filter endpoints

| Method | API | Parameters | Description | 
|--------|-----|------------|-------------| 
| GET | / | page | Trang chủ hiển thị sản phẩm | 
| GET | /about | None | Hiển thị trang giới thiệu |
| GET | /product/int:id | id | Chi tiết sản phẩm | 
| GET | /brand/int:id | id, page | Lọc sản phẩm theo thương hiệu | 
| GET | /category/int:id | id, page | Lọc sản phẩm theo danh mục | 
| GET | /search | q, sort, page | Tìm kiếm và sắp xếp sản phẩm | 
| GET/POST | /admin/addbrand | brand | Thêm thương hiệu mới | 
| GET/POST | /admin/addcategory | category | Thêm danh mục mới |  
| GET/POST | /admin/updatebrand/int:id | brand | Cập nhật thương hiệu | 
| GET/POST | /admin/updatecategory/int:id | category | Cập nhật danh mục | 
| POST | /admin/deletebrand/int:id | id | Xóa thương hiệu | 
| POST | /admin/deletecategory/int:id | id | Xóa danh mục |

#### Customer Routes:

- Authentication endpoints
- Profile management
- Order history endpoints

 | Method | API | Parameters | Description | 
 |--------|-----|------------|-------------| 
 | GET/POST | /customer/register | name, username, email, password, contact, address, city, state, country | Đăng ký tài khoản khách hàng | 
 | GET/POST | /customer/login | email, password | Đăng nhập khách hàng | 
 | GET | /customer/logout | None | Đăng xuất | 
 | GET/POST | /customer/profile | None | Quản lý thông tin cá nhân |

#### Cart Routes:

- Cart management endpoints
- Checkout process
- Order confirmation

 | Method | API | Parameters | Description | 
 |--------|-----|------------|-------------| 
 | POST | /addcart | product_id, quantity | Thêm sản phẩm vào giỏ hàng | 
 | GET | /cart | None | Xem giỏ hàng | 
 | GET | /updatecart/int:code | code, quantity | Cập nhật số lượng sản phẩm | 
 | GET | /deleteitem/int:id | id | Xóa sản phẩm khỏi giỏ hàng | 
 | GET | /clearcart | None | Xóa toàn bộ giỏ hàng |

### 4.2 Mã lỗi
#### 401 - Unauthorized
- "Vui lòng đăng nhập để thêm sản phẩm quan tâm"
- "Vui lòng đăng nhập để xem sản phẩm quan tâm"
- "Sai email hoặc password!"

#### 400 - Bad Request
- "Số lượng phải lớn hơn 0"
- "Số lượng tối đa có sẵn là {stock}"
- "Dữ liệu không hợp lệ"
- "Số điện thoại không hợp lệ!"
- "Độ dài địa chỉ lơn hơn 2"
- "Thành Phố, Huyện chỉ gồm các chữ, số và khoảng trắng"
- "Tên sản phẩm phải chứa ít nhất 3 kí tự"
- "Giá không hợp lệ"
- "Số lượng không hợp lệ"
- "Brand name must be at least 2 characters"
- "Không thể xoá {brand.name}"
- "Không thể xóa {category.name}"
- "Không thể thêm. Số lượng tối đa là {product.stock}"
- Image upload errors
- File deletion errors

#### 409 - Conflict
- "Email này đã được sử dụng"
- "Username này đã được sử dụng"
- "Brand already exists"
- "Category already exists"

#### 404 - Not Found
- Product not found
- Brand not found
- Category not found
- "Không tìm thấy kết quả cho từ khóa: {keyword}"

#### 200 - Success
- "Đã thêm sản phẩm vào danh sách quan tâm"
- "Item Updated"
- "Thông tin cá nhân của bạn đã được cập nhật!"
- "{name} đã được thêm vào database"
- "Thương hiệu của bạn đã được cập nhật"
- "Danh mục sản phẩm đã được cập nhật"
- "Xóa {name} thành công"

## 5. Thiết kế cơ sở dữ liệu

- Sơ đồ cơ sở dữ liệu: 
```markdown
Tables:
- User (Admin users)
- RegisterModel (Customer users)
- Product
- Brand
- Category 
- CustomerOrder

```

- Mối quan hệ:
    + Product -> Brand (Many-to-One)
    + Product -> Category (Many-to-One)
    + CustomerOrder -> Product (Many-to-One)
    + CustomerOrder -> RegisterModel (Many-to-One)

- Thiết kế bảng:
```markdown
Product:
- id: Integer, Primary Key
- name: String(80), NOT NULL
- price: Numeric, NOT NULL
- stock: Integer, NOT NULL
- desc: Text
- image_1: String(150)
- brand_id: Integer, Foreign Key
- category_id: Integer, Foreign Key

Brand:
- id: Integer, Primary Key
- name: String(30), UNIQUE, NOT NULL

Category:
- id: Integer, Primary Key
- name: String(30), UNIQUE, NOT NULL

CustomerOrder:
- id: Integer, Primary Key
- product_id: Integer, Foreign Key
- customer_id: Integer, Foreign Key
- quantity: Integer
- status: String
- date_added: DateTime

RegisterModel:
- id: Integer, Primary Key
- name: String(50)
- username: String(50), UNIQUE
- email: String(50), UNIQUE
- password: String(200)
- country: String(50)
- state: String(50)
- city: String(50)
- contact: String(50)
- address: String(50)
- date_created: DateTime

```

## 6. Yêu cầu hạ tầng và môi trường triển khai

- Môi trường phát triển:
```markdown
- Python 3.11
- Flask Framework
- SQLite Database
- Flask extensions:
  - Flask-SQLAlchemy
  - Flask-Login
  - Flask-Bcrypt
  - Flask-Uploads
```

- Bảo mật:
```markdown
- Password hashing với Bcrypt
- Session management
- Admin authentication decorator
- File upload security
```

## 7. Quy trình xử lý lỗi và bảo mật

- Xử lý lỗi:
```markdown
- Form validation
- Database integrity checks
- File upload validation
- Authentication checks
```

- Bảo mật:
```markdown
- Password hashing
- Login required decorators
- Admin required decorators
- CSRF protection
- Secure file uploads
```

## 8. Chi tiết về kiểm thử kỹ thuật

Test cases:
```markdown
1. User Authentication:
- Register validation
- Login validation
- Admin access control

2. Product Management:
- CRUD operations
- Image upload
- Stock management

3. Cart Operations:
- Add to cart
- Update quantity
- Remove items
```

## 9. Yêu cầu và quy trình triển khai
- Thiết lập triển khai:
```markdown
- pip install -r requirements.txt
- flask db init
- flask db migrate
- flask db upgrade
```

- Triển khai sản phẩm:
```markdown
- Database initialization
- Static files configuration
- Environment variables setup
- Server configuration (e.g., Gunicorn)
```

- Chiến lược backup:
```markdown
- Database backups
- Image files backup
- Configuration backup
```
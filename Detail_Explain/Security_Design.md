# Security Design Document

Tables of content:<br>
I. [System Classification](#i-system-classification)<br>
II. [Data Classification and Applied Data Security Standards](#ii-data-classification-and-applied-data-security-standards)<br>
III. [Network table](#iii-network-table)<br>
IV. [Requirements for Application Security](#iv-requirements-for-application-security)<br>
&nbsp;&nbsp;&nbsp;&nbsp;1. [Authentication and authorization](#1-authentication-and-authorization)<br>
&nbsp;&nbsp;&nbsp;&nbsp;2. [API security](#2-api-security)<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;- Admin Routes<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;- Product Routes<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;- Customer Routes<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;- Cart Routes<br>
&nbsp;&nbsp;&nbsp;&nbsp;3. [Application Security Controls](#3-application-security-controls)<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;- SQL Injection<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;- XSS Attacks<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;- CSRF Attacks<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;- File Upload Vulnerabilities<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;- Business Logic Flaws<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;- Information Disclosure<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;- API Security<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;- Session Management<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;- Data Exposure<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;- Server Security<br>
V. [Data storage](#v-data-storage)<br>
&nbsp;&nbsp;&nbsp;&nbsp;1. [Data in rest state](#1-data-in-rest-state)<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;- Database Encryption<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;- Access Control<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;- Backup Security<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;- File System Security<br>
&nbsp;&nbsp;&nbsp;&nbsp;2. [Data in transit state](#2-data-in-transit-state)<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;- Transport Layer Security<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;- API Communication<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;- Internal Communications<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;- Data Transfer Controls<br>
VI. [Log and monitoring](#vi-log-and-monitoring)<br>
VII. [Plan to penetration testing and testcase](#vii-plan-to-penetration-testing-and-testcase)<br>
VIII. [Risk Assessment & Treatment](#viii-risk-assessment--treatment)<br>

## I. System Classification

| System Name | Description | Users | Number of Users Served | System Classification | System Security Level |
|---|--- | --- | --- | --- | --- |
| E-commerce Web System | A web system that displays store products and provides consultation based on products that customers are interested in. | Administrator: manages products and users.<br> Customers: view and express interest in products for consultation | 100 | Publicly accessible system with external access | Low security system |

## II. Data Classification and Applied Data Security Standards

### 1. Users data need to secure
- Basic Personal information: name, email, phone number, address.
- Authentication information: password.
- Product interest history.

### 2. System data
- Product information
- Product images
- System configuration, source code
- Log files

### 3. Applied Data Security Standards
Data Privacy Compliance:
- ISO-27001 compliance
- Data minimization
- Data retention policies
- Privacy policy implementation

## III. Network table

### 1. Network security
```markdown
Requirements:
- Network segmentation (if applicable)
- Firewall configuration 
- IDS/IPS systems (if applicable)
```

### 2. Inbound traffic:
| No. | Source | Source IP/IP address range | Destination | Destination IP/IP address range | Protocol name | Port | Description |
| --- | --- | --- | --- | --- | --- | ---- | --- |
| 1 | Internet | 0.0.0.0/0 | Web server | xxx | TCP(https) | 443 | Web application access |
| 2 | Internet | x.x.x.x | Web server | xxx | TCP(ssh) | 22 | Server administration |
| .... | ... | ... | ... | ... | ... | ... | ... |

### 3. Outbound traffic:
| No. | Source | Source IP/IP address range | Destination | Destination IP/IP address range | Protocol name | Port | Description |
| --- | --- | --- | --- | --- | --- | ---- | --- |
| 1 | Web server | xxx | Internet | 0.0.0.0/0  | TCP(SMTP) | 587 | Email notification |
| ... | ... | ... | ... | ... | ... | ... | ... |

## IV. Requirements for Application Security
### 1. Authentication and authorization
```markdown
# Authentication
- Password policy:
  Min length: 8
  Complexity: letters, numbers, special chars
  Hashing: bcrypt with salt
  
- Session management:
  Session timeout: 30 mins
  Secure cookie flags
  CSRF protection
  Secure cookie attributes: SESSION_COOKIE_SECURE = True, SESSION_COOKIE_HTTPONLY = True, SESSION_COOKIE_SAMESITE = 'Strict'

- Rate limiting on login attempts or capcha (5 attempts/15 minutes)
- Implement 2FA for admin accounts

# Authorization 
Access Levels:
1. Store Administrator  
2. Customer
3. Guest User

Access Control Matrix:
- Store Admin: Product/user management
- Customer: Personal data, orders
- Guest: Public content only

Role-based access control (RBAC):
- Admin: Full system access
- Customer: Limited to personal data and cart
- Anonymous: Public product viewing only

Custom decorators for route protection: 
@admin_required
@login_required
@csrf_protect

```

### 2. API security
```markdown
# API protection
All endpoints:
- X-Frame-Options: DENY
- X-XSS-Protection: 1; mode=block
- X-Content-Type-Options: nosniff
- Content-Security-Policy: default-src 'self'
- Strict-Transport-Security: max-age=31536000
- Rate limiting: 100 req/min
- Input validation
- Output encoding
- Error handling
- JWT for API authentication
- API versioning

# Error handling
Standard error responses:
- 200/201: Success
- 400: Validation errors with details
- 401: Authentication required
- 403: Permission denied
- 404: Resource not found
- 409: Conflict
- 429: Rate limit exceeded
- 500: Internal server error (no details exposed)
```

#### Admin Routes:
- User management endpoints
- Product management endpoints
- Order processing endpoints

 | Method | API | Parameters | Description | API security requirements |
 |--------|-----|------------|-------------| -------------------------------|
 | GET/POST | /admin/login | email, password | Xác thực đăng nhập admin | Input validation:<br>- email: Required, valid email format<br>- password: Required, min 8 chars and mixed letters, numbers, special chars<br>Rate limit: 5 attempts/15 minutes<br>Response:<br>- 200: Admin JWT token + admin info<br>- 401: "Invalid credentials"<br>- 429: "Too many attempts" |
 | GET | /admin | None | Trang quản trị chính | Authentication: Admin token required<br>Rate limit: 100 req/min<br>Response:<br>- 200: Success message<br> - 401: Unauthorized |
 | GET | /admin/brands | None |Quản lý danh sách thương hiệu | Authentication: Admin token required<br>Rate limit: 100 req/min<br>Response:<br>- 200: Success message<br> - 401: Unauthorized |
 | GET | /admin/categories | None | Quản lý danh mục sản phẩm | Authentication: Admin token required<br>Rate limit: 100 req/min<br>Response:<br>- 200: Success message<br> - 401: Unauthorized |
 | GET | /admin/users | None | Xem danh sách người dùng | Authentication: Admin token required<br>Rate limit: 100 req/min<br>Response:<br>- 200: Success message<br> - 401: Unauthorized |
 | POST | /admin/delete_user/int:id | id | Xóa người dùng khỏi hệ thống | Authentication: Admin token required<br> Rate limit: 10 req/min<br> Input validation:<br> - id: Required, numeric, existing user<br> Response:<br> - 200: Success message<br> - 404: "User not found"<br> - 403: Not admin |
 | GET | /admin/search | q, type, page | Tìm kiếm người dùng/sản phẩm | Authentication: Admin token required<br>Input validation:<br>- q: Required, max 100 chars<br>- type: Required, enum[user,product]<br>- page: Optional, numeric<br>Response:<br>- 200: Search results<br>- 400: Invalid parameters |
 | GET/POST | /admin/addproduct | name, price, stock, desc, brand, category, image_1 | Thêm sản phẩm mới | Authentication: Admin token required<br> Rate limit: 30 req/min<br> Input validation:<br> - name: Required, 3-80 chars<br> - price: Required, numeric, > 0<br> - stock: Required, numeric, >= 0<br> - image_1: Required, jpg/png, max 5MB<br> - brand_id: Required, valid brand<br> - category_id: Required, valid category<br> Response:<br> - 201: Success message<br> - 400: Validation errors<br> - 401: Unauthorized<br> - 403: Not admin |
 | GET/POST | /admin/updateproduct/int:id | name, price, stock, desc, brand, category, image_1 | Cập nhật thông tin sản phẩm | Authentication: Admin token required<br>Input validation:<br>- All product fields<br>- id: Valid product ID<br>Response:<br>- 200: Success message<br>- 404: Product not found |
 | POST | /admin/deleteproduct/int:id | id | Xóa sản phẩm | Authentication: Admin token required<br>Input validation:<br>- id: Valid product ID<br>Response:<br>- 200: Success message<br>- 404: Product not found |
 | GET | /admin/logout | None | Đăng xuất | Authentication: Admin token required<br>Ressponse:<br>- 200: success<br>- 404: "No found" |

#### Product Routes:

- Product CRUD endpoints
- Category management
- Search and filter endpoints

| Method | API | Parameters | Description | API security requirements |
|--------|-----|------------|-------------| -------------------------------|
| GET | / | page | Trang chủ hiển thị sản phẩm | Authentication: Optional<br>Rate limit: 50 req/min<br>Ressponse:<br>- 200: Product list<br>- 404: "No products found" |
| GET | /about | None | Hiển thị trang giới thiệu | Authentication: Optional<br>Rate limit: 50 req/min<br>Ressponse:<br>- 200: Detail information<br>- 404: "No found" |
| GET | /product/int:id | id | Chi tiết sản phẩm | Authentication: optional<br> Rate limit: 100 req/min <br> Input validation:<br> - id: Required, numeric <br> Response:<br> - 200: Product details <br> - 404: "Product not found" |
| GET | /brand/int:id | id, page | Lọc sản phẩm theo thương hiệu | Authentication: Optional<br> Input validation:<br>- id: Valid brand ID<br>- page: Optional, numeric<br>Response:<br>- 200: Brand products<br>- 404: Brand not found |
| GET | /category/int:id | id, page | Lọc sản phẩm theo danh mục | Authentication: Optional <br>Input validation:<br>- id: Valid category ID<br>- page: Optional, numeric<br>Response:<br>- 200: Category products<br>- 404: Category not found |
| GET | /search | q, sort, page | Tìm kiếm và sắp xếp sản phẩm | Authentication: Optional <br> Rate limit: 50 req/min<br> Input validation:<br> - q: Required, max 100 chars<br> - sort: Optional, enum[price_asc, price_desc, brand]<br> - page: Optional, numeric, default 1<br> Response:<br> - 200: Paginated products<br> - 400: "Invalid parameters" |
| GET/POST | /admin/addbrand | brand | Thêm thương hiệu mới | Authentication: Admin token required<br>Input validation:<br>- name: Required, unique, 2-30 chars<br>Response:<br>- 201: Success message<br>- 409: "Brand exists" |
| GET/POST | /admin/addcategory | category | Thêm danh mục mới | Authentication: Admin token required <br>Input validation:<br>- name: Required, unique, 2-30 chars<br>Response:<br>- 201: Success message<br>- 409: "Brand exists" |
| GET/POST | /admin/updatebrand/int:id | brand | Cập nhật thương hiệu | Authentication: Admin token required<br>Input validation:<br>- name: Required, unique<br>- id: Valid brand ID<br>Response:<br>- 200: Success message<br>- 404: Brand not found |
| GET/POST | /admin/updatecategory/int:id | category | Cập nhật danh mục | Authentication: Admin token required<br>Input validation:<br>- name: Required, unique<br>- id: Valid category ID<br>Response:<br>- 200: Success message<br>- 404: Category not found |
| POST | /admin/deletebrand/int:id | id | Xóa thương hiệu | Authentication: Admin token required<br>Input validation:<br>- id: Valid brand ID<br>Response:<br>- 200: Success message<br>- 404: Brand not found<br>- 409: "Cannot delete brand in use" |
| POST | /admin/deletecategory/int:id | id | Xóa danh mục | Authentication: Admin token required<br>Input validation:<br>- id: Valid category ID<br>Response:<br>- 200: Success message<br>- 404: Category not found<br>- 409: "Cannot delete category in use" |

#### Customer Routes:

- Authentication endpoints
- Profile management
- Order history endpoints

 | Method | API | Parameters | Description | API security requirements |
 |--------|-----|------------|-------------| ------------------------------|
 | GET/POST | /customer/register | name, username, email, password, contact, address, city, state, country | Đăng ký tài khoản khách hàng | Input validation:<br> - name: Required, 2-50 chars, alphanumeric <br> - username: Required, 4-50 chars, unique<br> - email: Required, valid format, unique<br> - password: Required, min 8 chars, complexity rules<br> - contact: Valid phone format<br> - address: Required, max 200 chars<br> Response:<br> - 201: Success message<br> - 409: "Email/username already exists"<br> - 400: Validation errors |
 | GET/POST | /customer/login | email, password | Đăng nhập khách hàng | Input validation:<br> - email: Required, valid email format<br> - password: Required, min 8 chars<br> Rate limit: 5 attempts/15 minutes<br> Response:<br>  - 200: JWT token + user info<br> - 401: "Invalid email or password"<br> - 429: "Too many attempts" |
 | GET | /customer/logout | None | Đăng xuất | Authentication: Customer token required<br>Ressponse:<br>- 200: success<br>- 404: "No found" |
 | GET/POST | /customer/profile | None | Quản lý thông tin cá nhân | Authentication: Customer token required<br>Input validation for POST:<br>- All profile fields<br>Response:<br>- 200: Profile data/Updated<br>- 400: Validation errors |

#### Cart Routes:

- Cart management endpoints
- Checkout process
- Order confirmation

 | Method | API | Parameters | Description | API security requirements |
 |--------|-----|------------|-------------| ----------------------------- |
 | POST | /addcart | product_id, quantity | Thêm sản phẩm vào giỏ hàng | Authentication: Customer token required<br> Rate limit: 50 req/min<br> Input validation:<br> - product_id: Required, valid product<br> - quantity: Required, numeric, > 0<br> Response:<br> - 200: Success message<br> - 400: "Invalid quantity"<br> - 404: "Product not found" |
 | GET | /cart | None | Xem giỏ hàng | Authentication: Customer token required<br>Rate limit: 50 req/min<br>Ressponse:<br>- 200: Product list<br>- 404: "Not found" |
 | GET | /updatecart/int:id | id, quantity | Cập nhật số lượng sản phẩm | Authentication: Customer token required<br>Input validate for id and quantity >= 0<br>Rate limit: 50 req/min<br>Ressponse:<br>- 200: success update<br>- 404: "Not found" |
 | GET | /deleteitem/int:id | id | Xóa sản phẩm khỏi giỏ hàng | Authentication: Customer token required<br>Input validation:<br>- id: Valid cart item ID<br>Response:<br>- 200: Success message<br>- 404: Item not found | 
 | GET | /clearcart | None | Xóa toàn bộ giỏ hàng | Authentication: Customer token required <br> Rate limit: 20 req/min<br> Response:<br> - 200: Success message<br> - 401: Unauthorized |

### 3. Application Security Controls
#### SQL Injection
Prevention:
- Use SQLAlchemy ORM with parameterized queries
- Input validation, sanitization and escape special characters
- Limit database user privileges
- Regular security audits

```markdown
# Using SQLAlchemy ORM with Parameterized Queries
  Never use string concatenation or f-strings for SQL queries
  Always use SQLAlchemy models and relationships
  Implement query filters through ORM methods
  Use bind parameters for dynamic values
  Enable SQLAlchemy query logging in development

# Input Validation, Sanitization and Character Escaping
- Implement strict validation rules for all user inputs:
    Product names: alphanumeric + basic punctuation only
    Prices: numeric values only, positive numbers
    Quantities: positive integers only
    Email addresses: valid email format
    Phone numbers: numeric + basic formatting only
    Usernames: alphanumeric only

- Remove or encode special SQL characters: ', ", ;, --, /*, */
- Use prepared statements for all dynamic queries
- Implement input length limits matching database field sizes

# Database User Privileges Restrictions
- Create separate database users for different operations:
    Admin user: Full privileges, used only for schema changes
    Application user: Limited to SELECT, INSERT, UPDATE, DELETE
    Backup user: SELECT only
- Restrict database access by IP address
- Never use root/admin credentials in application code
- Regularly audit database user permissions
- Remove unused database accounts

# Regular Security Audits
- Weekly automated scan of database queries
- Monthly review of:
    Database access logs
    Failed query attempts
    Unusual query patterns
    User privilege changes
- Quarterly security assessment:
    SQL injection vulnerability testing
    Database configuration review
    User access audit
    Performance impact analysis

- Annual comprehensive database security audit

# Additional Security Measures
  Enable database query logging
  Monitor for suspicious query patterns
  Implement database connection pooling
  Use database encryption at rest
  Regular database backup testing
  Keep database software updated
  Document all database access patterns
```

#### XSS Attacks
Prevention:
- Content Security Policy headers
- HTML escaping
- Input validation
- Output encoding
- Sanitize user-generated content
- X-XSS-Protection header

```markdown
# Content Security Policy Headers
Implement strict CSP rules:
  Allow scripts only from trusted domains
  Disable inline scripts and eval()
  Restrict media sources to specific domains
  Set frame-ancestors to 'none'
  Enable strict-dynamic for scripts
  Configure report-uri for violations

#  HTML Escaping Requirements
  Escape all dynamic content in HTML templates
  Use template engine's built-in escaping
  Double-escape content in JavaScript contexts
  Escape URL parameters
  Special handling for JSON data embedding

# Input Validation Rules
  Validate length and format of all inputs
  Create whitelists for allowed characters
  Block known malicious patterns
  Implement context-specific validation
  Validate before storing in database
  Log suspicious input patterns

# Output Encoding Standards
Context-specific encoding:
  HTML context: Encode special characters
  JavaScript context: Unicode escape sequences
  URL context: URL encoding
  CSS context: CSS escape sequences

Encode all dynamic data before display
Use different encoding for different contexts

# User-Generated Content Sanitization
  Define allowed HTML tags whitelist
  Specify allowed attributes for each tag
  Remove all script elements and events
  Sanitize URLs in href/src attributes
  Convert newlines appropriately
  Handle markdown/rich text safely
  Implement preview functionality

# X-XSS-Protection Configuration
  Enable XSS filtering
  Set mode=block for violations
  Configure reporting endpoint
  Handle legacy browser support
  Monitor filter effectiveness
  Log blocked attempts
```

#### CSRF Attacks
Prevention:
- CSRF tokens for all forms
- SameSite cookie policy
- Origin validation
- Custom CSRF decorators
- Secure session management

```markdown
# CSRF Tokens Implementation
  Generate cryptographically secure random tokens using `secrets.token_urlsafe()`
  Token length must be minimum 32 bytes
  Include token in all forms using hidden field
  Store token in session and validate on each POST request
  Rotate tokens after successful form submission
  Set token expiration time (30 minutes recommended)

# SameSite Cookie Policy
- Set SameSite=Strict for all session cookies
- Configure cookie attributes:
    Secure flag must be enabled
    HttpOnly flag must be enabled
    Domain restriction to application domain only
    Set appropriate expiration time
    Use __Host- prefix for cookies when possible

# Origin Validation
  Validate Origin header against allowed domains list
  Check Referer header as fallback
  Maintain whitelist of allowed origins
  Block requests with missing/invalid origins
  Log suspicious origin mismatches
  Implement strict CORS policy

# Custom CSRF Decorators
  Create decorator to enforce token validation
  Apply decorator to all state-changing routes
  Verify token presence and validity
  Check token expiration
  Handle token mismatch errors appropriately
  Log failed validation attempts

# Secure Session Management
  Use secure session identifiers (min 128 bits entropy)
  Regenerate session ID after login
  Clear session data on logout
  Implement absolute session timeout (24 hours)
  Implement idle session timeout (30 minutes)
  Store session data server-side only

# Additional Recommendations
  Use POST for state-changing operations
  Avoid GET requests for sensitive actions
  Implement re-authentication for critical operations
  Monitor and alert on suspicious patterns
  Regular security testing of CSRF protections
  Document CSRF protection requirements for developers

# Error Handling
  Return 403 Forbidden on CSRF validation failure
  Do not expose token validation details in errors
  Log validation failures with request details
  Implement graceful error recovery
  Provide clear user feedback

# Monitoring & Auditing
  Log all CSRF validation failures
  Track token generation and usage
  Monitor for unusual patterns
  Set up alerts for multiple failures
  Regular review of CSRF logs
  Periodic testing of protection mechanisms
```

#### File Upload Vulnerabilities
Prevention:
- Whitelist extensions (jpg, png only)
- File size limit (5MB)
- File type validation
- Randomize filenames
- Store outside webroot
- Scan for malware
- Secure file permissions

```markdown
# Extension Whitelist Implementation
  Create strict whitelist: ['jpg', 'jpeg', 'png']
  Verify both file extension and MIME type
  Reject files with multiple extensions (example.php.jpg)
  Convert all extensions to lowercase before validation
  Block executables and script files completely

# File Size Controls
  Set hard limit of 5MB per file
  Configure server-side upload limits in nginx/apache
  Add client-side validation for better UX
  Monitor total storage usage per user
  Implement upload quotas if needed

# File Type Validation
  Check magic numbers/file signatures
  Verify MIME type matches extension
  Use python-magic library for deep file inspection
  Reject files failing integrity checks
  Log all failed validation attempts

# Filename Security
  Generate random UUIDs for filenames
  Preserve original extension after sanitization
  Remove special characters and spaces
  Add timestamp prefix for uniqueness
  Maintain mapping of original to stored names

# Storage Location Security
  Store files outside document root
  Use separate partition/storage for uploads
  Implement directory structure by date/user
  Restrict direct file access
  Use X-Sendfile for secure file serving

# Malware Protection
  Integrate ClamAV for virus scanning
  Quarantine suspicious files
  Scan files before saving to storage
  Set up real-time malware monitoring
  Configure automated malware alerts

# File Permissions
  Set restrictive file permissions (640)
  Use dedicated service account for file operations
  Implement proper ownership (www-data)
  Disable execute permissions
  Regular permission audits

# Additional Security Measures
  Implement file type specific validation
  Add watermarks to images
  Generate thumbnails securely
  Log all file operations
  Regular security scans of stored files

# Error Handling
  Provide clear error messages
  Log validation failures
  Alert on repeated failures
  Clean up failed uploads
  Monitor storage capacity

# Access Control
  Implement user-based access control
  Verify file ownership
  Use signed URLs for downloads
  Time-limited access tokens
  Track file access history
```

#### Business Logic Flaws
Prevention:
- Validate quantity limits
- Check stock availability
- Verify price calculations
- Implement request rate limiting
- Transaction integrity checks

```markdown
# Quantity Limit Validation
  Set maximum order quantity per product (e.g. 10 items)
  Validate against current stock levels
  Check quantity against business rules (bulk orders)
  Implement server-side validation before cart updates
  Add quantity checks at both cart and checkout stages

# Stock Availability Management
  Implement real-time stock tracking
  Add stock reservation during checkout process (15 minutes hold)
  Set low stock alerts (notify when < 5 items)
  Validate stock before order confirmation
  Handle concurrent access with database locks

# Price Calculation Verification
  Implement server-side price calculations
  Store product prices in database, never client-side
  Validate all price components (base price, discounts)
  Check price consistency across sessions
  Log all price modifications
  Compare final price against original product price

# Request Rate Limiting
  Cart updates: max 10 requests/minute
  Checkout attempts: max 3 requests/5 minutes
  Product views: max 100 requests/minute
  Search queries: max 20 requests/minute
  Track by user ID and IP address
  Implement exponential backoff for repeated violations

# Transaction Integrity
  Use database transactions for order processing
  Implement order state machine (pending → processing → complete)
  Record all state changes with timestamps
  Verify order totals at each step
  Create audit trails for all transactions
  Handle partial failures gracefully
  Implement idempotency for payment processing

# Additional Security Measures
  Monitor unusual buying patterns
  Track failed transaction attempts
  Implement order amount limits
  Verify shipping address validity
  Check payment method consistency
  Log all critical business operations

# Monitoring & Alerts
- Set up alerts for:
    Unusual order volumes
    Price discrepancies
    High failure rates
    Stock level anomalies
    Multiple failed transactions
    Suspicious user behavior

# Regular Audits
  Daily transaction reconciliation
  Weekly inventory checks
  Monthly pricing audit
  Quarterly business logic review
  Regular security assessment of business flows
```

#### Information Disclosure
Prevention:
- Hide system information
- Custom error pages
- Remove debug info
- Secure error handling
- Data minimization
- Access logging

```markdown
# Hide System Information
  Remove all server headers revealing technology stack
  Configure web server to hide version numbers
  Use custom server tokens
  Strip metadata from uploaded files
  Remove comments containing sensitive info from HTML/JS

# Custom Error Pages
  Create specific error templates for 404, 403, 500
  Never expose stack traces or system paths
  Log detailed errors server-side only
  Return generic messages to users
  Implement different error handling for dev/prod

# Remove Debug Information
  Disable debug mode in production
  Remove all print/console statements
  Clear all development comments
  Configure logging levels appropriately
  Sanitize all API responses

# Secure Error Handling
  Implement centralized error handling
  Use try-catch blocks for sensitive operations
  Log errors with proper severity levels
  Sanitize error messages before display
  Create error codes for tracking

# Data Minimization
  Only collect necessary user data
  Mask sensitive data in logs (emails, phones)
  Implement data retention policies
  Regular data cleanup procedures
  Use role-based data access

# Access Logging
  Log all authentication attempts
  Track admin actions
  Monitor file access patterns
  Record API usage statistics
  Implement log rotation

# Additional Security Measures
  Regular security audits
  Penetration testing
  Code reviews focusing on information leakage
  Security headers configuration
  Third-party dependency reviews
```

#### API Security
Prevention:
- Input validation
- Rate limiting
- JWT authentication
- HTTPS only
- API versioning
- Request validation

```markdown
# Input Validation Requirements
  Validate request parameters against predefined schemas
  Enforce strict data types and formats
  Check length limits for all string inputs
  Validate file uploads before processing
  Implement custom validators for business logic
  Log validation failures for security monitoring

# Rate Limiting Implementation
  Set 100 requests/minute for general endpoints
  Restrict login attempts to 5/15 minutes
  Implement 30 requests/minute for admin endpoints
  Use IP-based and token-based rate limiting
  Configure retry-after headers
  Store rate limit data in Redis/cache

# JWT Authentication Controls
  Use RS256 algorithm for token signing
  Set token expiration to 30 minutes
  Include essential claims only (sub, exp, iat)
  Implement token refresh mechanism
  Store token blacklist
  Rotate signing keys regularly

# HTTPS Configuration
  Force HTTPS redirect
  Enable HSTS with 1-year duration
  Use TLS 1.3 only
  Configure secure cipher suites
  Implement certificate pinning
  Regular SSL configuration audits

# API Versioning Strategy
  Include version in URL path (/api/v1/)
  Maintain backwards compatibility
  Document version changes
  Deprecation notices for old versions
  Version-specific rate limits
  Monitor version usage

# Request Validation Process
  Validate HTTP methods per endpoint
  Check Content-Type headers
  Validate request body size
  Implement request timeout
  Check API key/credentials
  Log invalid requests

# Additional Security Controls
  Enable CORS with strict origin policy
  Implement request signing for sensitive endpoints
  Monitor unusual traffic patterns
  Regular security scanning of API endpoints
  Maintain security documentation
  Incident response procedures
```

#### Session Management
Prevention:
- Secure session IDs
- Session timeout
- Session invalidation on logout
- Prevent session fixation
- Secure cookie attributes

```markdown
# Secure Session IDs:
  Use cryptographically secure random values (min 128 bits)
  Never expose session IDs in URLs
  Regenerate session IDs after authentication
  Use Flask's secure session management with `SECRET_KEY`

# Session Timeout Implementation:
  Set absolute timeout: 30 minutes
  Set idle timeout: 15 minutes
  Force re-authentication for sensitive operations
  Clear session data after timeout

# Session Invalidation:
  Clear all session data on logout
  Remove session from server-side storage
  Delete session cookies
  Invalidate all active sessions when changing password
  Force logout from all devices option

# Session Fixation Protection:
  Generate new session ID on login
  Validate session origin
  Check IP consistency
  Implement session tokens
  Verify session creation timestamp

# Secure Cookie Configuration:
  Cookie Attributes:
  - Secure: True (HTTPS only)
  - HttpOnly: True (No JS access)
  - SameSite: Strict
  - Domain: Specific to application
  - Path: Limited to application paths
  - Expires: Match session timeout

# Session Storage Security:
  Use server-side session storage
  Encrypt session data
  Implement session versioning
  Regular session cleanup
  Monitor active sessions

# Additional Security Measures:
  Track concurrent sessions
  Implement session fingerprinting
  Log session anomalies
  Rate limit session creation
  Geographic location validation

# Session Monitoring:
  Log all session events
  Track failed session validations
  Monitor session reuse attempts
  Alert on suspicious patterns
  Regular session audit

```

#### Data Exposure
Prevention:
- Encrypt sensitive data
- Access control checks
- Data masking
- Secure backups
- Audit trails
- Data retention policies

```markdown
# Encrypt Sensitive Data
  Use AES-256 encryption for all PII data including names, addresses, phone numbers
  Store encryption keys in a separate secure key management system
  Implement encryption at rest for database fields containing sensitive information
  Use TLS 1.3 for all data in transit
  Never store credit card or financial data

# Access Control Checks
  Implement strict role-based access control (RBAC)
  Create detailed access matrices for each data type
  Log all data access attempts
  Review access permissions quarterly
  Set up data classification levels (Public, Internal, Confidential, Restricted)
  Enforce principle of least privilege

# Data Masking
  Mask phone numbers to show only last 4 digits
  Display only partial email addresses `(e.g., j***@domain.com)`
  Never expose full addresses in public views
  Hash all sensitive data in logs
  Implement view-based masking based on user roles

# Secure Backups
  Encrypt all backup files using AES-256
  Store backups in geographically separate locations
  Implement 3-2-1 backup strategy
  Regular backup testing and verification
  Secure backup access with MFA
  Monitor backup access logs

# Audit Trails
  Log all data modifications
  Track who accessed what data and when
  Record all export/download operations
  Monitor unusual data access patterns
  Set up real-time alerts for suspicious activities
  Maintain audit logs for minimum 1 year

# Data Retention Policies
- Define retention periods for each data type:
    Customer data: 2 years after last activity
    Transaction data: 7 years
    Log files: 1 year
    Session data: 30 days
- Implement automated data purging
- Secure data destruction procedures
- Document all data lifecycle processes

# Additional Measures
  Regular data privacy impact assessments
  Employee training on data handling
  Incident response plan for data breaches
  Data privacy compliance checks
  Third-party data sharing agreements
  Regular security audits
```

#### Server Security
Prevention:
- Regular updates
- Security patches
- Firewall configuration
- Network segmentation
- Service hardening
- Monitoring and alerts

```markdown
# Regular Updates
  Schedule weekly OS updates during off-peak hours (2-4 AM)
  Enable automatic security updates for critical patches
  Maintain dependency update schedule:
    Python packages: Weekly
    System libraries: Bi-weekly
    Database: Monthly
  Document all updates in change log

# Security Patches
  Subscribe to security advisories for all components
  Establish patch testing environment
  Define patch deployment process:
    Test in staging
    Backup before deployment
    Deploy during maintenance window
    Verify functionality post-patch
  Emergency patch procedure for critical vulnerabilities

# Firewall Configuration
  Implement defense-in-depth strategy
  Allow only necessary ports:
    443 (HTTPS)
    22 (SSH) - restricted to VPN IPs
  Set up Web Application Firewall (WAF):
    Block common attack patterns
    Rate limiting rules
    Geolocation restrictions
  Regular firewall rule audit

# Network Segmentation
  Create separate network zones:
    Web zone (public-facing)
    Application zone (internal)
    Database zone (restricted)
    Admin zone (highly restricted)
  Implement jump boxes for admin access
  Use VLANs for isolation
  Restrict inter-zone communication

# Service Hardening
  Disable unnecessary services
  Run services with minimal privileges
  Configure secure defaults:
    Disable root SSH
    Remove default accounts
    Change default ports
  Implement file integrity monitoring
  Set up secure logging

# Monitoring and Alerts
  Real-time monitoring for:
    CPU/Memory usage (alert > 80%)
    Disk space (alert > 85%)
    Failed login attempts (alert > 5/minute)
    Error rates (alert > 5%)
    Response times (alert > 2s)
  Set up intrusion detection:
    Network anomalies
    File system changes
    Privilege escalations
    Unusual process behavior
  Configure alert channels:
    Email for non-critical
    SMS for critical
    Incident response team notification
```


## V. Data storage
### 1. Data in rest state
#### Database Encryption
- Implement AES-256 encryption for sensitive data:
  + Personal information (name, phone, address)
  + Authentication tokens
- Use bcrypt with salt for password hashing
- Store encryption keys in secure hardware module

```markdown
# AES-256 Encryption for Sensitive Data:
- Personal Information:
    Use AES-256-GCM mode for encryption
    Generate unique IV for each encryption
    Store IV alongside encrypted data
    Encrypt fields: name, phone, address separately
    Implement field-level encryption
    Enable searching on encrypted fields using deterministic encryption

- Authentication Tokens:
    Use hardware-based random number generator
    Implement token rotation every 24 hours
    Store tokens with expiration timestamps
    Use separate encryption keys for tokens
    Enable secure token revocation

# Password Hashing with Bcrypt:
  Configure work factor of 12 or higher
  Generate unique salt for each password
  Implement pepper in addition to salt
  Store hash timing information
  Regular work factor assessment and updates
  Implement hash upgrade mechanism

# Encryption Key Management:
  Use Hardware Security Module (HSM)
  Implement key hierarchy
    Master Key
    Data Encryption Keys
    Key Encryption Keys
  Regular key rotation schedule
  Secure key backup procedures
  Access control for key operations
  Key usage auditing
 
# Additional Security Measures:
  Database-level encryption at rest
  Secure connection strings
  Encrypted backups
  Access logging
  Regular security audits
  Compliance monitoring
  Data classification enforcement
```

#### Access Control
- Implement role-based database access
- Database user privileges based on function
- Audit logging for all data access
- Regular access review and cleanup

```markdown
# Role-based Database Access
  Create distinct database roles: admin_role, customer_role, guest_role
  Define specific permissions for each role
  Map application users to database roles
  Implement row-level security where needed
  Use views to restrict data access

# Database User Privileges
- Create separate database users for:
    Application read/write operations
    Backup operations
    Monitoring operations
    Administrative tasks
  Grant minimum required privileges
  Avoid using superuser accounts
  Regularly rotate database credentials

# Audit Logging Requirements
- Log these mandatory fields:
    User ID
    Action type (SELECT, INSERT, UPDATE, DELETE)
    Timestamp
    Source IP
    Affected data
    Success/Failure status
  Store logs in separate secure location
  Implement log rotation
  Set up real-time alerts for suspicious activities
  
# Access Review Process
  Weekly review of admin account activities
  Monthly review of user access patterns
  Quarterly privilege audit
  Immediate revocation process for departed users
  Document all access changes
  Maintain access history for 1 year

# Additional Security Measures
  Implement connection pooling with limits
  Set query timeouts
  Use prepared statements only
  Enable SSL for database connections
  Regular backup verification
  Monitor failed login attempts
```

#### Backup Security
- Encrypted backups using industry-standard algorithms
- Secure offsite storage
- Regular backup testing
- Retention policy:
  + Daily backups: 7 days
  + Weekly backups: 1 month
  + Monthly backups: 1 year

```markdown
# Encryption Requirements
  Use AES-256-GCM for file encryption
  Implement secure key management with HSM or KMS
  Store encryption keys separately from backups
  Rotate encryption keys every 90 days
  Document key rotation procedures

# Storage Security
  Use separate backup servers in different physical locations
  Implement network segmentation for backup infrastructure
  Require VPN access for backup management
  Use SFTP/SCP for backup transfers
  Enable audit logging for all backup access

# Backup Testing Protocol
  Weekly restore tests of random files
  Monthly full restore tests
  Quarterly disaster recovery simulations
  Document all test results and issues
  Maintain restore time objectives (RTO)

# Retention Management Daily Backups (7 days):
  Full database backup
  User uploads
  Configuration files
  System logs

- Weekly Backups (1 month):
    Full system state
    Database with historical data
    Analytics data
    Audit logs
 
- Monthly Backups (1 year):
    Complete system snapshot
    Historical transaction data
    Compliance records
    Security audit trails

# Monitoring Requirements
  Alert on backup failures
  Monitor backup sizes and timing
  Track successful restores
  Report on retention compliance
  Monitor encryption status

# Documentation Requirements
  Backup procedures
  Restoration procedures
  Key management procedures
  Emergency contact information
  Incident response plan
```

#### File System Security
- Store files outside webroot
- Implement secure file permissions
- Regular integrity checks
- Access logging for sensitive files

```markdown
# File Storage Location
  Create dedicated storage directory: /var/www/shop/storage
  Separate directories for different file types:
    /storage/products - Product images
    /storage/temp - Temporary upload processing
    /storage/backups - System backups
    /storage/logs - Security logs
 
# File Permissions
  Set restrictive base permissions:
    Directories: 750 (rwxr-x---)
    Files: 640 (rw-r-----)
  Create dedicated service account 'shop_app'
  Add application user to 'shop_app' group
  Remove all world permissions
  Use ACLs for fine-grained control

# File Integrity Monitoring
  Implement daily hash checks for critical files
  Monitor file modification timestamps
  Track file ownership changes
  Set up alerts for unauthorized modifications
  Keep integrity baseline database
  Regular integrity reports

# Access Control
  Implement file access whitelist
  Use secure temporary file handling
  Sanitize all filenames
  Validate file mime types
  Check file signatures
  Implement download throttling

# Access Logging
- Log all file operations:
    File creation/deletion
    Modifications
    Access attempts
    Permission changes

- Include in logs:
    Timestamp
    User ID
    IP address
    Operation type
    File path
    Success/failure

# Backup Procedures
  Implement versioned backups
  Encrypt backup files
  Secure backup transport
  Regular backup testing
  Retention policy enforcement

# Security Best Practices
  Never store sensitive files in public directories
  Use random file names for uploaded files
  Implement file size limits
  Scan files for malware
  Regular security audits
  Clean temporary files automatically

# Emergency Procedures
  File system compromise response plan
  Backup restoration procedures
  Incident logging requirements
  Communication protocols
  Recovery verification steps
```

### 2. Data in transit state
#### Transport Layer Security
- Enforce TLS 1.3 for all connections
- Configure secure cipher suites:
  + TLS_AES_256_GCM_SHA384
  + TLS_CHACHA20_POLY1305_SHA256
- Enable HSTS with long duration
- Regular SSL certificate management

```markdown
# TLS 1.3 Enforcement
  Configure web server (Nginx/Apache) to only accept TLS 1.3 connections
  Disable all older TLS/SSL versions (1.0, 1.1, 1.2)
  Implement automatic HTTP to HTTPS redirection
  Monitor TLS version usage in logs
 
# Cipher Suite Configuration
  Enable only strong cipher suites in order:
    TLS_AES_256_GCM_SHA384 (primary)
    TLS_CHACHA20_POLY1305_SHA256 (backup)
  Disable weak ciphers and algorithms
  Regular cipher suite audits
  Monitor cipher usage patterns
 
# HSTS Implementation
  Set max-age to at least 1 year (31536000 seconds)
  Include subdomains directive
  Enable preload list submission
  Monitor HSTS errors and browser warnings
  Implement HSTS reporting
 
# Certificate Management
  Use automated certificate renewal (Let's Encrypt)
  Minimum 2048-bit RSA or ECC P-256 keys
  Monitor certificate expiration
  Implement certificate transparency logging
  Regular key rotation schedule
  Backup certificate private keys securely
  Document certificate renewal procedures
 
# Additional Security Measures
  Enable OCSP stapling
  Implement Certificate Authority Authorization (CAA)
  Configure secure TLS session parameters
  Monitor SSL/TLS security headers
  Regular security configuration testing
 
# Monitoring & Maintenance
  Weekly SSL configuration testing
  Monthly cipher suite reviews
  Quarterly security header audits
  Automated certificate monitoring
  SSL/TLS error logging and alerts
```

#### Data Transfer Controls
- Secure file transfer protocols
- End-to-end encryption for sensitive data
- Data integrity verification
- Transfer logging and monitoring

```markdown
# Secure File Transfer Protocols
  Use SFTP/FTPS for all file transfers with minimum TLS 1.2
  Implement strong authentication for file transfer services
  Configure allowed IP ranges for file transfer endpoints
  Set up automatic file integrity checks using SHA-256 checksums
  Establish secure key exchange mechanisms for transfer encryption
 
# End-to-end Encryption
  Implement AES-256 encryption for all sensitive data
  Use secure key management system for encryption keys
  Rotate encryption keys every 90 days
  Store encryption keys in a separate secure location
  Encrypt data both in transit and at rest
 
# Data Integrity Verification
  Generate digital signatures for all transferred files
  Implement checksum verification before and after transfers
  Use hash comparison for file integrity checks
  Set up automated integrity monitoring system
  Create verification logs for all data transfers
 
# Transfer Logging and Monitoring
- Log all file transfer activities including:
    Transfer initiation time
    Source and destination
    File size and type
    User performing transfer
    Transfer completion status
    Integrity check results

- Set up real-time alerts for:
    Failed transfers
    Integrity check failures
    Unauthorized transfer attempts
    Unusual transfer patterns
    Large file transfers
  Retain logs for minimum 90 days
  Implement log rotation and archival
  Create regular transfer audit reports
 
# Additional Security Measures
  Implement data classification based transfer controls
  Set up transfer bandwidth limits
  Configure automatic file encryption before transfer
  Establish secure file deletion after successful transfer
  Create disaster recovery procedures for failed transfers
```

## VI. Log and monitoring
### 1. Security Logging
Log events:
- Authentication attempts
- Admin actions  
- System errors
- File operations
- Database changes
- Log rotation and encryption
- Secure log storage

```markdown
# Authentication Logging
- Log every login attempt with:
    Timestamp in ISO-8601 format
    IP address and geolocation
    User agent details
    Success/failure status
    Username/email used
    Failed attempt counts
    2FA status if applicable
 
# Admin Action Logging
- Track all administrative operations:
    Product management (create/update/delete)
    User management actions
    Configuration changes
    Permission modifications
    Include before/after states
    Record admin ID and role
 
# System Error Logging
- Implement hierarchical error logging:
    Critical system failures
    Security violations
    Performance issues
    Application errors
    Include stack traces securely
    Error categorization and severity
 
# File Operation Logging
- Monitor all file interactions:
    Upload/download events
    File modifications
    Permission changes
    File access attempts
    File integrity checks
    Malware scan results
 
# Database Change Logging
- Track database modifications:
    Schema changes
    Data modifications
    Query performance issues
    Backup operations
    User privilege changes
    Transaction logs
 
# Log Rotation Strategy
- Implement automated rotation:
    Daily rotation for high-volume logs
    Weekly rotation for system logs
    Monthly rotation for audit logs
    Compression of old logs
    Retention period enforcement
    Archive management

# Secure Storage Requirements
- Protect log integrity:
    Write-once storage
    Encryption at rest
    Access control lists
    Backup procedures
    Tamper detection
    Secure deletion policy

# Log Format Standards
- Standardize log entries:
    Consistent timestamp format
    Required field definitions
    Severity levels
    Event categories
    Correlation IDs
    Source identification
 
# Log Analysis Requirements
- Enable effective analysis:
    Search capabilities
    Pattern detection
    Anomaly identification
    Alert thresholds
    Reporting formats
    Compliance mapping
 
# Security Measures
- Protect log data:
    Access restrictions
    Encryption methods
    Integrity verification
    Secure transmission
    Backup encryption
    Deletion procedures
```
```markdown
# Log format
{
  "timestamp": "ISO-8601",
  "level": "INFO|WARN|ERROR",
  "event": "event_name",
  "user": "user_id",
  "ip": "client_ip",
  "data": {}
}
```

### 2. Monitoring
```markdown
# Monitoring metrics
- Failed login attempts
- Resource usage
- Error rates
- Response real-times alert

# Alerts
- Login failures > 5/min
- CPU usage > 80%
- Error rate > 5%
- Response time > 2s
```

### 3. Incident response
```markdown
# Response procedures
1. Detection
2. Analysis  
3. Containment
4. Eradication
5. Recovery
6. Lessons learned

# Communication plan
- Internal notification
- Customer notification
- Authority reporting
```

## VII. Plan to penetration testing and testcase
Will be detail planted after development
```markdown
# Security testing
- Static analysis
- Dynamic testing
- Penetration testing
- Vulnerability scanning

# Test cases
- Authentication bypass
- Authorization bypass  
- SQL injection
- XSS attacks
- CSRF attacks
- File upload bypass
```

##  VIII. Risk Assessment & Treatment
```markdown
Risk Categories:
1. Data breaches
2. Unauthorized access
3. System availability
4. Data integrity
5. Regulatory compliance

Treatment Methods:
- Risk mitigation
- Risk transfer 
- Risk acceptance
- Risk avoidance
```
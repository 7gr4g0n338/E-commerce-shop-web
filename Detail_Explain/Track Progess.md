# Tiến độ xây dựng ứng dụng web trình bày sản phẩm và tư vấn sản phẩm dựa trên thông tin khách hàng cung cấp.
Mục tiêu sau dự án này:
+ Học được tư duy và nâng cao khả năng sử dụng code python.
+ Hiểu được cách 1 trang web hoạt động, cấu trúc, cách build web-serer.
+ Thực hiện design security cho web ngay từ đầu.

Mục lục:<br>
I. [Lên plan và design cho project web trình bày sản phẩm](#i-lên-plan-và-design-cho-project-web-trình-bày-sản-phẩm)
1. [Tìm mã nguồn cơ bản để học hiểu và tiếp tục phát triển](#1-tìm-mã-nguồn-cơ-bản-để-học-hiểu-và-tiếp-tục-phát-triển)<br>
2. [Phân tích mã nguồn, cấu trúc hệ thống](#2-phân-tích-mã-nguồn-cấu-trúc-hệ-thống)<br>
3. [Viết tài liệu thiết kế cho web-server](#3-viết-tài-liệu-thiết-kế-cho-web-server)<br>
4. [Design security cho web-server](#4-design-security-cho-web-server)<br>

II. [Develop web-server](#ii-develop-web-server)
1. [Develop web-server](#1-develop-web-server)<br>
2. [Test web-server](#2-test-web-server)<br>
3. [Test security cho web-server](#3-test-security-cho-web-server)<br>

III. [Deploy web-server](#iii-deploy-web-server)
1. [Biết cách triển khai mã nguồn lên EC2 để chạy như môi trường production](#1-biết-cách-triển-khai-mã-nguồn-lên-ec2-để-chạy-như-môi-trường-production)<br>
2. [Pentest lần cuối cho web-server](#2-pentest-lần-cuối-cho-web-server)<br>

## I. Lên plan và design cho project web trình bày sản phẩm

### 1. Tìm mã nguồn cơ bản để học hiểu và tiếp tục phát triển
Done

Web bán hàng E-commerce:
https://github.com/ChiragSaini/E-Commerce-Using-Flask

+ Web này đang gồm các chức năng:
    + show sản phẩm, nhãn hiệu, danh mục sản phẩm, giỏ hàng, đăng nhập, đăng ký, đăng xuất, tìm kiếm.

+ Web server hoạt động:<br>
    Người dùng:
    + cho phép người dùng thêm những sản phẩm mà họ muốn mua
    + cho phép người dùng tìm kiếm sản phẩm

    Người quản trị:
    + cho phép người quản trị thêm, sửa, xóa sản phẩm, nhãn hàng, danh mục
    

### 2. Phân tích mã nguồn, cấu trúc hệ thống
Done

+ Hiểu web-server cấu trúc, mô hình như thế nào: 
    + MVC- model-view-controller
    + Dùng python là ngôn ngữ lập trình, flask làm framework, sqlite làm database, bootstrap làm giao diện.

+ Hiểu Web-server dùng các thư viện nào:
    + Dùng alembic để quản lý database
    + Dùng sqlalchemy để tương tác với database
    + Dùng jinja để render giao diện
    + Dùng flask-wtf để xử lý form
    + Dùng flask-login để login...

+ Hiểu cách mã nguồn code python:
    + Hiểu các đọc source theo thứ tự lần lượt từ file main rồi cấu hình database tới code backend và frontend
    + Đọc hiểu file cấu hình của database.

### 3. Viết tài liệu thiết kế cho web-server
To do
#### 3.1 tài liệu đặc tả ứng dụng
Đây là các yêu cầu cơ bản cần thiết cho việc thiết kế ứng dụng, cung cấp thông tin chi tiết về các yêu cầu và đặc điểm của ứng dụng

##### 3.1.1. Tổng quan dự án
+ Mục đích của ứng dụng: Lý do tạo ra ứng dụng, vấn đề ứng dụng sẽ giải quyết.
+ Phạm vi dự án: Giới hạn và phạm vi của ứng dụng, bao gồm các tính năng chính.
+ Đối tượng người dùng: Đặc điểm người dùng mục tiêu của ứng dụng (ví dụ: người dùng cá nhân, doanh nghiệp, nhóm tuổi,...).

##### 3.1.2. Các yêu cầu chức năng
+ Chức năng chính: Mô tả chi tiết từng chức năng mà ứng dụng cần có. Ví dụ:
    + Đăng nhập/đăng ký tài khoản
    + Quản lý tài khoản người dùng
    + Các chức năng đặc thù liên quan đến ứng dụng (ví dụ: mua sắm, chat, quản lý tài liệu,...)
+ Tương tác người dùng: Mô tả cách người dùng sẽ tương tác với mỗi chức năng (giao diện, cách thức thao tác,...).

##### 3.1.3. Yêu cầu phi chức năng
+ Hiệu suất: Tốc độ xử lý, độ trễ tối đa chấp nhận được.
+ Khả năng bảo mật: Yêu cầu về bảo mật dữ liệu, quyền truy cập.
+ Khả năng mở rộng: Độ linh hoạt khi thêm mới các tính năng hoặc thay đổi quy mô người dùng.
+ Khả năng tương thích: Yêu cầu về hệ điều hành, trình duyệt, hoặc thiết bị hỗ trợ.
+ Độ tin cậy: Yêu cầu về khả năng phục hồi, dự phòng.

##### 3.1.4. Yêu cầu giao diện người dùng (UI)
+ Bố cục giao diện: Sơ đồ và cấu trúc của các màn hình chính, cách bố trí các thành phần.
+ Phong cách thiết kế: Màu sắc, biểu tượng, font chữ, và các yếu tố giao diện khác.
+ Tiêu chuẩn và hướng dẫn UI: Quy tắc về UX/UI để đảm bảo tính nhất quán và dễ sử dụng.

##### 3.1.5. Kiến trúc hệ thống
+ Mô hình kiến trúc: Các thành phần hệ thống và cách chúng tương tác với nhau (ví dụ: client-server, microservices, MVC).
+ Sơ đồ hệ thống: Lưu đồ mô tả cách dữ liệu và yêu cầu được xử lý trong hệ thống.
+ Yêu cầu hạ tầng: Các yêu cầu về máy chủ, cơ sở dữ liệu, mạng, và các dịch vụ liên quan.

##### 3.1.6. Quy trình xử lý dữ liệu
+ Dữ liệu đầu vào và đầu ra: Loại và định dạng dữ liệu mà ứng dụng xử lý.
+ Luồng xử lý dữ liệu: Mô tả chi tiết cách dữ liệu di chuyển qua các thành phần khác nhau trong ứng dụng.
+ Lưu trữ dữ liệu: Yêu cầu về lưu trữ dữ liệu tạm thời hoặc vĩnh viễn.

##### 3.1.7. Yêu cầu kiểm thử
+ Các trường hợp kiểm thử (Test cases): Các kịch bản kiểm thử để đảm bảo ứng dụng hoạt động đúng với yêu cầu.
+ Phương pháp kiểm thử: Kiểm thử chức năng, kiểm thử bảo mật, kiểm thử hiệu suất,...
+ Tiêu chuẩn chấp nhận: Điều kiện để mỗi chức năng đạt yêu cầu và chấp nhận được.

##### 3.1.8. Yêu cầu bảo mật
+ Bảo vệ dữ liệu người dùng: Chính sách bảo mật dữ liệu, mã hóa, quản lý truy cập.
+ Quyền hạn người dùng: Các cấp quyền truy cập khác nhau, cơ chế xác thực và ủy quyền.
+ Bảo vệ ứng dụng: Yêu cầu về ngăn ngừa các mối đe dọa bảo mật (ví dụ: chống lại tấn công SQL Injection, XSS, DDoS,...).

##### 3.1.9. Rủi ro và kế hoạch dự phòng
+ Xác định rủi ro: Các vấn đề tiềm ẩn có thể ảnh hưởng đến việc phát triển và vận hành ứng dụng.
+ Kế hoạch dự phòng: Các phương pháp đối phó và giải pháp thay thế trong trường hợp rủi ro xảy ra.

##### 3.1.10. Kế hoạch bảo trì và cập nhật
+ Chu kỳ cập nhật: Kế hoạch cho các bản cập nhật tính năng, bảo mật và sửa lỗi.
+ Yêu cầu bảo trì: Yêu cầu về bảo trì hệ thống để đảm bảo hiệu suất và tính bảo mật lâu dài.

#### 3.2 Tài liệu đặc tả kĩ thuật
Đây là các yêu cầu đi sâu vào chi tiết kỹ thuật của hệ thống hoặc ứng dụng mà đội ngũ phát triển sẽ thực hiện - cấu trúc, các thành phần phần mềm, kiến trúc, và giao diện kỹ thuật giữa các thành phần

##### 3.2.1. Mô tả tổng quan kỹ thuật
+ Giới thiệu về hệ thống: Tóm tắt ngắn gọn về kiến trúc tổng thể và mục tiêu kỹ thuật của hệ thống.
+ Các công nghệ sử dụng: Nêu chi tiết các công nghệ, ngôn ngữ lập trình, framework, và công cụ được sử dụng trong dự án (ví dụ: Java, .NET, Spring, Docker,...).
+ Các thành phần chính: Giới thiệu sơ lược các module và thành phần chính của hệ thống.

##### 3.2.2. Kiến trúc hệ thống
+ Mô hình kiến trúc: Mô tả kiến trúc hệ thống (ví dụ: MVC, microservices, serverless, monolithic).
+ Sơ đồ kiến trúc: Sơ đồ chi tiết của hệ thống, mô tả các thành phần và cách thức chúng tương tác.
+ Cấu trúc các tầng (layers): Mô tả chi tiết về các tầng của hệ thống, chẳng hạn như tầng trình bày (presentation layer), tầng dịch vụ (service layer), và tầng dữ liệu (data layer).
+ API và dịch vụ liên quan: Mô tả cách các dịch vụ sẽ tương tác với nhau, bao gồm định dạng API (REST, GraphQL, SOAP) và phương thức truyền tải dữ liệu (JSON, XML).

##### 3.2.3. Chi tiết về các thành phần phần mềm
+ Mô tả các module: Mỗi module sẽ được mô tả về chức năng, đầu vào, đầu ra, và luồng xử lý bên trong.
+ Luồng dữ liệu (Data flow): Mô tả luồng dữ liệu giữa các module, cách thức dữ liệu di chuyển và chuyển đổi qua các phần của hệ thống.
+ Sơ đồ trình tự (Sequence diagrams): Mô tả các trình tự giao tiếp giữa các thành phần trong một luồng xử lý cụ thể.

##### 3.2.4. Giao diện lập trình ứng dụng (API)
+ Đặc tả API: Bao gồm danh sách các endpoint, phương thức HTTP (GET, POST, PUT, DELETE), và thông tin về tham số.
+ Định dạng dữ liệu: Mô tả định dạng dữ liệu gửi và nhận (JSON, XML) và cấu trúc dữ liệu chi tiết.
+ Các mã lỗi (Error codes): Mô tả các mã lỗi và thông báo lỗi sẽ trả về từ API để giúp xử lý lỗi dễ dàng hơn.

##### 3.2.5. Thiết kế cơ sở dữ liệu
+ Sơ đồ cơ sở dữ liệu (Database schema): Cung cấp sơ đồ chi tiết về các bảng, mối quan hệ giữa các bảng, khóa chính và khóa ngoại.
+ Thiết kế bảng và trường dữ liệu: Mô tả cấu trúc các bảng, kiểu dữ liệu, và các ràng buộc (constraints) như NOT NULL, UNIQUE, INDEX.
+ Các quy tắc ràng buộc dữ liệu (Constraints): Quy tắc đảm bảo tính toàn vẹn của dữ liệu, như ràng buộc về tham chiếu (foreign keys), và logic nghiệp vụ.

##### 3.2.6. Yêu cầu hạ tầng và môi trường triển khai
+ Môi trường phát triển, kiểm thử, và triển khai: Yêu cầu về cấu hình hệ thống cho từng môi trường (ví dụ: hệ điều hành, phiên bản phần mềm).
+ Hệ thống mạng và bảo mật: Yêu cầu về cấu hình mạng, firewall, và cách bảo vệ dữ liệu trên môi trường đám mây hoặc máy chủ nội bộ.
+ Công cụ giám sát và logging: Yêu cầu về công cụ giám sát (monitoring) và ghi log để hỗ trợ bảo trì và khắc phục sự cố (ví dụ: Prometheus, Grafana, ELK stack).

##### 3.2.7. Quy trình xử lý lỗi và bảo mật
+ Xử lý lỗi (Error handling): Cách thức phát hiện, ghi nhận, và xử lý các lỗi trong ứng dụng.
+ Biện pháp bảo mật: Các kỹ thuật mã hóa dữ liệu, chính sách xác thực và phân quyền người dùng, và biện pháp ngăn chặn các cuộc tấn công (như SQL Injection, XSS).
+ Quy tắc backup và khôi phục: Quy trình backup dữ liệu và cách thức khôi phục hệ thống khi có sự cố.

##### 3.2.8. Chi tiết về kiểm thử kỹ thuật
+ Các loại kiểm thử: Bao gồm kiểm thử đơn vị (unit testing), kiểm thử tích hợp (integration testing), và kiểm thử hệ thống (system testing).
+ Kịch bản kiểm thử (Test cases): Mô tả từng kịch bản kiểm thử cho các module hoặc chức năng chính, và điều kiện thành công/thất bại.
+ Công cụ kiểm thử: Danh sách các công cụ kiểm thử dự kiến sẽ sử dụng (như Selenium, JUnit, Postman).

##### 3.2.9. Yêu cầu và quy trình triển khai
+ Quy trình triển khai: Mô tả quy trình triển khai từ phát triển sang sản phẩm, bao gồm các bước kiểm tra và xác minh.
+ Script và công cụ tự động hóa: Các script tự động hóa quá trình triển khai, nếu có (như CI/CD với Jenkins, GitLab CI, hoặc Docker).
+ Kế hoạch rollback: Kế hoạch dự phòng khi triển khai thất bại, bao gồm cách hoàn nguyên về phiên bản trước.

##### 3.2.10. Tài liệu phụ trợ và chú thích
+ Tài liệu tham khảo: Danh sách các tài liệu, tiêu chuẩn kỹ thuật hoặc nguồn tham khảo được sử dụng để xây dựng và xác định yêu cầu kỹ thuật.
+ Chú thích: Ghi chú các thuật ngữ chuyên ngành, ký hiệu viết tắt, hoặc các định nghĩa đặc biệt cần giải thích thêm.

### 4. Design security cho web-server
To Do
Đây là các yêu cầu về bảo mật cho web-server, bao gồm các nguyên tắc và kỹ thuật để bảo vệ hệ thống web-server.

#### 4.1. Nguyên tắc bảo mật theo thiết kế (Security by Design Principles)
+ Least Privilege (Nguyên tắc ít quyền nhất): Cấp quyền truy cập tối thiểu cho người dùng, dịch vụ, và quy trình. Chỉ cấp quyền cho những gì thực sự cần thiết.
+ Defense in Depth (Phòng thủ theo lớp): Sử dụng nhiều lớp bảo mật để bảo vệ dữ liệu, cho phép một lớp bảo vệ khác nếu một lớp bị xâm phạm.
+ Fail Securely (Hỏng an toàn): Thiết kế hệ thống sao cho trong trường hợp lỗi, hệ thống vẫn bảo vệ dữ liệu và duy trì bảo mật.
+ Separation of Duties (Phân chia nhiệm vụ): Phân quyền để không một cá nhân hoặc hệ thống nào có quyền truy cập quá rộng rãi.
+ Avoid Security by Obscurity (Tránh bảo mật bằng cách che giấu): Bảo mật không nên dựa vào việc giữ bí mật thông tin thiết kế hoặc mã nguồn; thay vào đó, hãy sử dụng các biện pháp bảo vệ mạnh mẽ.

#### 4.2. Phân tích các mối đe dọa (Threat Modeling)
+ Xác định tài sản (Assets): Xác định dữ liệu và tài sản quan trọng nhất mà hệ thống cần bảo vệ (như thông tin cá nhân, dữ liệu nhạy cảm,...).
+ Xác định các mối đe dọa tiềm ẩn: Liệt kê các kiểu tấn công mà hệ thống có thể gặp phải (ví dụ: SQL injection, XSS, CSRF, tấn công từ chối dịch vụ - DDoS).
+ Đánh giá lỗ hổng: Phân tích các điểm yếu trong thiết kế hệ thống mà kẻ tấn công có thể khai thác.
+ Xây dựng các biện pháp bảo vệ: Đề xuất các biện pháp phòng chống cụ thể để xử lý các mối đe dọa đã xác định.

#### 4.3. Thiết kế và mã hóa an toàn (Secure Coding and Design Practices)
+ Sử dụng mã hóa: Áp dụng mã hóa cho dữ liệu nhạy cảm trong khi lưu trữ và truyền tải (AES, RSA).
+ Kiểm soát truy cập và xác thực: Sử dụng các phương thức xác thực an toàn như OAuth, JWT, hoặc xác thực đa yếu tố (MFA) để bảo vệ quyền truy cập.
+ Sanitization và Validation: Làm sạch và kiểm tra tất cả dữ liệu đầu vào từ người dùng để tránh các tấn công injection.
+ Sử dụng các thư viện và framework an toàn: Áp dụng các thư viện và framework đã được kiểm tra bảo mật, đồng thời thường xuyên cập nhật các bản vá lỗi bảo mật.

#### 4.4. Bảo mật dữ liệu (Data Security)
+ Mã hóa dữ liệu nhạy cảm: Mã hóa dữ liệu ở trạng thái nghỉ (at-rest) và trong quá trình truyền tải (in-transit) để đảm bảo dữ liệu không bị đọc trộm.
+ Bảo vệ API: Đảm bảo rằng tất cả các API được bảo vệ và kiểm tra quyền truy cập trước khi cung cấp dữ liệu.
+ An ninh cơ sở dữ liệu: Sử dụng kiểm soát truy cập mạnh mẽ, mã hóa cơ sở dữ liệu, và thường xuyên kiểm tra để phát hiện truy cập bất thường.

#### 4.5. Bảo vệ giao diện lập trình ứng dụng (API Security)
+ Xác thực và phân quyền mạnh mẽ: Đảm bảo API chỉ cho phép truy cập từ các nguồn đáng tin cậy.
+ Giới hạn tốc độ (Rate Limiting): Áp dụng giới hạn tốc độ để ngăn chặn các cuộc tấn công brute force và từ chối dịch vụ (DoS).
+ Sử dụng token an toàn: Khi dùng token (như JWT), áp dụng các biện pháp bảo mật để ngăn chặn tái sử dụng và thao tác trái phép.

#### 4.6. Đảm bảo tuân thủ (Compliance)
+ Tuân thủ các tiêu chuẩn bảo mật: Đảm bảo hệ thống tuân thủ các tiêu chuẩn bảo mật như ISO 27001, NIST, hoặc PCI-DSS nếu cần.
+ Chính sách lưu trữ dữ liệu và bảo mật: Đảm bảo rằng dữ liệu nhạy cảm được lưu trữ và quản lý theo chính sách bảo mật phù hợp.

#### 4.7. Kiểm thử bảo mật (Security Testing)
+ Kiểm thử xâm nhập (Penetration Testing): Thực hiện kiểm thử xâm nhập để đánh giá khả năng chống chịu của hệ thống trước các cuộc tấn công thực tế.
+ Kiểm thử bảo mật tự động: Sử dụng các công cụ như OWASP ZAP, Burp Suite để tự động phát hiện các lỗ hổng bảo mật phổ biến.
+ Kiểm thử bảo mật định kỳ: Thực hiện kiểm thử bảo mật thường xuyên để phát hiện các lỗ hổng phát sinh trong quá trình phát triển và nâng cấp.

#### 4.8. Giám sát và ứng phó sự cố (Monitoring and Incident Response)
+ Giám sát hệ thống: Sử dụng công cụ giám sát để theo dõi các hoạt động bất thường và các hành vi có dấu hiệu tấn công.
+ Ghi log và phát hiện xâm nhập: Lưu trữ log chi tiết về các hành động trong hệ thống, sử dụng công cụ phát hiện xâm nhập (IDS) để nhận biết sớm các dấu hiệu bất thường.
+ Kế hoạch phản ứng sự cố: Thiết lập quy trình ứng phó khi xảy ra sự cố, bao gồm cách nhận diện, cô lập, và khôi phục sau sự cố an ninh.

#### 4.9. Bảo mật vòng đời phát triển phần mềm (Secure SDLC)
+ Tích hợp bảo mật vào quy trình phát triển: Tạo ra các checkpoint bảo mật trong từng giai đoạn phát triển phần mềm (yêu cầu, thiết kế, mã hóa, kiểm thử, triển khai).
+ Đào tạo bảo mật cho lập trình viên: Đảm bảo rằng đội ngũ phát triển hiểu và áp dụng các thực hành bảo mật trong quá trình phát triển.
+ Quản lý thay đổi bảo mật: Đảm bảo các bản cập nhật và thay đổi trong hệ thống không tạo ra lỗ hổng bảo mật mới.

## II. Develop web-server

### 1. Develop web-server
To Do
+ Lên kế hoạch chỉnh sửa và code thêm các chức năng mới: trong file new_function.txt

### 2. Test web-server 
To Do
+ Kiểm tra các chức năng đặt ra như người dùng thường và admin, xem đã đúng yêu cầu design chưa.

### 3. Test security cho web-server
To Do
+ Pentest web theo check list top 10-owasp:
    + Check các lỗi liên quan tới logic, xác thực
    + Check các lỗi liên quan tới database, thực thi lệnh hệ thống, XSS, CSRF, SSRF
    + Check các lỗi làm lộ thông tin người dùng
    + Check các lỗi cho phép chiếm quyền hệ thống, root.

## III. Deploy web-server

### 1. Biết cách triển khai mã nguồn lên EC2 để chạy như môi trường production
Done
+ Hiểu các thành phần cần để triển khai được mã nguồn lên EC2: Nginx, gunicorn, flask, python, database
+ Biết cách dựng gunicorn service E-commerce trên EC2
+ Biết cách dùng nginx để định tuyến request từ port 80 vào port local đang chạy service E-commerce
+ Biết cách cài các env trước để chạy được các thư viện.

### 2. Pentest lần cuối cho web-server
To Do
+ Check kĩ lại các bug đã test.
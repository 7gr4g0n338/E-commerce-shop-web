### 4. Design security cho web-server - To Do

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

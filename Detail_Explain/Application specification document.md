# Web application specification document

Mục lục:
1. [Tổng quan dự án](#1-tổng-quan-dự-án)
2. [Các yêu cầu chức năng](#2-các-yêu-cầu-chức-năng)
3. [Yêu cầu phi chức năng](#3-yêu-cầu-phi-chức-năng)
4. [Yêu cầu giao diện người dùng (UI)](#4-yêu-cầu-giao-diện-người-dùng-ui)
5. [Kiến trúc hệ thống](#5-kiến-trúc-hệ-thống)
6. [Quy trình xử lý dữ liệu](#6-quy-trình-xử-lý-dữ-liệu)
7. [Yêu cầu kiểm thử](#7-yêu-cầu-kiểm-thử)
8. [Yêu cầu bảo mật](#8-yêu-cầu-bảo-mật)
9. [Rủi ro và kế hoạch dự phòng](#9-rủi-ro-và-kế-hoạch-dự-phòng)
10. [Kế hoạch bảo trì và cập nhật](#10-kế-hoạch-bảo-trì-và-cập-nhật)

## 1. Tổng quan dự án
- Mục đích của ứng dụng: Xây dựng 1 ứng dụng web hiển thị các sản phẩm của cửa hàng cho khách hàng xem. Khi khách hàng thêm sản phẩm vào giỏ quan tâm thì chủ cửa hàng sẽ tư vấn dựa trên các sản phẩm mà khách hàng quan tâm.

- Phạm vi của dự án: Hệ thống trình bày các sản phẩm của cửa hàng, quản lý các sản phẩm, người dùng và sản phẩm khách hàng quan tâm.

- Đối tượng người dùng: Người dùng khách hàng cá nhân, quản trị viên cửa hàng.

## 2. Các yêu cầu chức năng
### 2.1 Chức năng chính
#### 2.1.1 Chức năng người dùng
- Đăng nhập tài khoản:
    + Đăng nhập bằng email và mật khẩu.

- Đăng xuất tài khoản

- Đăng ký tài khoản:
    + Cần điền đủ các thông tin: tên người dùng, tên tài khoản, email, mật khẩu, nhập lại mật khẩu, quốc gia, tỉnh/thành phố, Quận/ huyện/ thị xã, Địa chỉ thường chú và số điện thoại.

- Xem hiển thị các sản phẩm:
    + Hiển thị theo tên danh mục sản phẩm
    + Hiển thị theo ten thương hiệu
    + Hiển thị toàn bộ sản phẩm: Có phân trang, mỗi trang 8 sản phẩm. Mỗi sản phẩm hiển thị trên trang gồm: hình ảnh, tên sản phẩm, giá và 2 nút nhấn là "chi tiết" và "quan tâm".
    + Hiển thị chi tiết của 1 sản phẩm: hình ảnh mẫu - phóng to được hình ảnh, tên sản phẩm, tên thương hiệu, giá, mô tả sản phẩm và số lượng sản phẩm quan tâm để thêm vào giỏ quan tâm.

- Xem được thông tin giới thiệu về cửa hàng trên 1 trang gồm:
    + Lịch sử thành lập
    + Giá trị cốt lõi
    + Lĩnh vực kinh doanh
    + Thông tin liên hệ với cửa hàng

- Giỏ hàng quan tâm - chỉ xem và thêm được sảm phẩm vào giỏ quan tâm khi người dùng đã đăng nhập:
    + Các thông tin cơ bản trong giỏ quan tâm: số thứ tự, Ảnh mẫu, tên sản phẩm, giá, số lượng sản phẩm, nút xóa sản phẩm, tổng giá tiền, nút xem tiếp các sản phẩm, nút xóa toàn bộ sản phẩm.
    + có chức năng xem thêm/xóa/xóa toàn bộ sản phẩm trong giỏ quan tâm
    + Điều chỉnh được số lượng sản phẩm trong giỏ quan tâm ❌
    + xem được chi tiết sản phẩm khi nhấn vào sản phẩm trong giỏ quan tâm

- Tìm kiếm sản phẩm:
    + Tìm kiếm sản phẩm theo tên sản phẩm, thương hiệu, danh mục sản phẩm.
    + Kết quả sau khi tìm kiếm có thể được sắp xếp theo thứ tự thương hiệu, giá.

- Cập nhật thông tin cá nhân

#### 2.1.2 Chức năng quản trị viên
- Đăng nhập tài khoản:
    + Đăng nhập bằng email và mật khẩu.

- Đăng xuất tài khoản

- Quản lý sản phẩm:
    + Xem được toàn bộ danh sách các sản phẩm: 
        + Thông tin cơ bản: số thứ tự, tên sản phẩm, giá, thương hiệu, hình ảnh, nút sửa và xóa sản phẩm
        + Có thể sửa/ xóa sản phẩm.
        + Có phân trang và chỉ hiển thị list 10 sản phẩm trên 1 trang.
    + Xem được toàn bộ danh sách các thương hiệu:
        + Thông tin cơ bản: số thứ tự, tên thương hiệu.
        + Có thể sửa/ xóa thương hiệu.
    + Xem được toàn bộ danh sách các danh mục sản phẩm:
        + Thông tin cơ bản: số thứ tự, tên danh mục sản phẩm.
        + Có thể sửa/ xóa danh mục sản phẩm.
    + Thêm mới sản phẩm:
        + Thông tin cơ bản: tên sản phẩm, giá, số lượng sản phẩm cửa hàng có, thương hiệu, danh mục sản phẩm, hình ảnh.
    + Thêm mới thương hiệu:
        + Thông tin cơ bản: tên thương hiệu.
    + Thêm mới danh mục sản phẩm:
        + Thông tin cơ bản: tên danh mục sản phẩm.

- Quản lý người dùng:
    + Hiển thị danh sách tất cả người dùng đã đăng ký tài khoản:
        + Thông tin cơ bản: tên tài khoản, email, số điện thoại, Địa chỉ đầy đủ, ngày đăng ký, sản phẩm quan tâm(gồm 5 sản phẩm được người dùng quan tâm/ đã xóa khỏi giỏ quan tâm - ưu tiên hiển thị 5 sản phẩm ở trạng thái quan tâm sau đó mới là trạng thái đã xóa), nút xóa người dùng.
    
- Tìm kiếm:
    + tìm kiếm theo sản phẩm, thương hiệu, danh mục, tên người dùng, tên tài khoản, email.

### 2.2 Tương tác người dùng
#### 2.2.1 Tương tác người dùng khách hàng
Trường hợp người dùng khách hàng chưa đăng nhập:
- Khi người dùng mới truy cập vào trang chủ của ứng dụng, sẽ hiển thị ra tất cả các sản phẩm của cửa hàng và thông báo "Vui lòng đăng nhập để thêm các sản phẩm quan tâm vào giỏ quan tâm và được tư vấn! (Nếu quý khách chưa có tài khoản, vui lòng đăng ký và đăng nhập)" trên tất cả các đường dẫn dành cho người dùng khách hàng.

- Khi người dùng nhấn vào thanh logo của cửa hàng thì sẽ được chuyển đến trang chủ của ứng dụng, hiển thị tất cả các sản phẩm.
    + Nếu người dùng nhấn vào nút "Chi tiết" thì sẽ hiển thị chi tiết sản phẩm.
    + Nếu người dùng nhấn vào nút "Quan tâm" thì sẽ được điều hướng tới trang login và thông báo "Vui lòng đăng nhập để thêm sản phẩm quan tâm".

- Khi nhấn vào "Về chúng tôi" thì sẽ được chuyển đến trang giới thiệu về cửa hàng.

- Khi nhấn vào "Thương hiệu" thì trình duyệt vẫn ở nguyên trang hiện tại và chỉ thả thanh menu gồm tên các thương hiệu xuống dưới.
    + Nếu người dùng chọn 1 thương hiệu thì sẽ hiển thị tất cả các sản phẩm của thương hiệu đó.

- Khi nhấn vào "Danh mục sản phẩm" thì trình duyệt vẫn ở nguyên trang hiện tại và chỉ thả thanh menu gồm tên các danh mục sản phẩm xuống dưới.
    + Nếu người dùng chọn 1 danh mục sản phẩm thì sẽ hiển thị tất cả các sản phẩm của danh mục đó.

- Khi nhấn vào "Quan tâm" trên thanh bar thì sẽ hiển thị thông báo "Vui lòng đăng nhập để xem sản phẩm quan tâm ".

- Khi nhấn vào hộp thoại tìm kiếm thì cho phép người dùng nhập từ khóa cần tìm kiếm:
    + Nếu không tìm thấy từ khóa nào khớp thì sẽ trả về thông báo "Không tìm thấy kết quả cho từ khóa: <từ khóa tìm kiếm>". 
    + Nếu tìm thấy kết quả thì sẽ hiển thị ra các sản phẩm có tên sản phẩm, thương hiệu, danh mục chứa từ khóa tìm kiếm và dòng "Kết quả tìm kiếm sắp xếp theo thứ tự: <lựa chọn sắp xếp>". Lựa chọn sắp xếp có thể là "Giá tăng dần", "Giá giảm dần", "Thương hiệu".

- Khi nhấn vào "Đăng nhập" thì sẽ được chuyển đến trang login.
    + Nếu điền sai mật khẩu hoặc username thì sẽ báo lỗi "Sai tên đăng nhập hoặc mật khẩu".

- Khi nhấn vào "Đăng ký" thì sẽ được chuyển đến trang đăng ký(phần này cần nêu kĩ nhất có thể).
    + Hiển thị các trường nhập thông tin cần thiết để đăng ký tài khoản và có gợi ý cụ thể các trường nên điền như thế nào trong hộp thoại đăng ký.

    + Nếu điền sai định dạng và nhấn đăng kí thì sẽ báo lỗi tương ứng.

Trường hợp người dùng khách hàng đã đăng nhập - tương tự như trường hợp người dùng khách hàng chưa đăng nhập nhưng có thêm các chức năng sau:
- Khi nhấn vào "Quan tâm" trên thanh bar thì sẽ được chuyển tới giỏ hàng quan tâm và hiển thị toàn bộ các sản phẩm đã được thêm vào giỏ hàng quan tâm.
    + Nếu người dùng nhấn vào tên hoặc hình ảnh của sản phẩm thì sẽ được điều hướng tới chi tiết sản phẩm.
    + Nếu người dùng nhấn vào nút "Xóa" thì sẽ xóa sản phẩm đó ra khỏi giỏ hàng quan tâm.
    + Nếu người dùng nhấn vào nút xem tiếp các sản phẩm thì sẽ được điều hướng tới trang chủ.
    + Nếu người dùng nhấn xóa toàn bộ các sản phẩm đã quan tâm thì sẽ làm sạch giỏ hàng quan tâm.

- Khi nhấn vào "Tên username" cạnh thanh tìm kiếm thì sẽ thả thanh menu gồm các chức năng:
    + Cập nhật thông tin cá nhân: Khi nhấn vào đây thì sẽ được điều hướng tới trang cập nhật thông tin cá nhân. Người dùng có thể điều chỉnh lại các thông tin và nhấn cập nhật thông tin.

    + Đăng xuất: khi nhấn vào đây sẽ được điều hướng tới trang login

#### 2.2.2 Tương tác người dùng quản trị viên
Khi admin chưa đăng nhập thì mọi trang của admin đều sẽ điều hướng về trang login của admin.

Khi admin đã đăng nhập thì sẽ điều hướng về trang chủ của admin.
- Khi nhấn vào "Trang quản trị" trên thanh bar thì sẽ được điều hướng tới trang chủ của admin.
    + Hiển thị ra tất cả các sản phẩm của cửa hàng, người dùng có thể sửa hoặc xóa sản phẩm
    + Nếu nhấn nút "sửa" thì sẽ được điều hướng tới trang cập nhật sản phẩm
    + Nếu nhấn nút "xóa" thì sẽ xóa sản phẩm đó ra khỏi danh sách sản phẩm.

- Khi admin nhấn vào "Thương hiệu" trên thanh bar thì sẽ được điều hướng tới trang thương hiệu.
    + Hiển thị ra tất cả các thương hiệu của cửa hàng, người dùng có thể sửa hoặc xóa thương hiệu
    + Nếu nhn nút "sửa" thì sẽ được điều hướng tới trang cập nhật thương hiệu
    + Nếu nhấn nút "xóa" thì sẽ xóa thương hiệu đó ra khỏi danh sách thương hiệu.

- Khi admin nhấn vào "Danh mục sản phẩm" trên thanh bar thì sẽ được điều hướng tới trang danh mục sản phẩm.
    + Hiển thị ra tất cả các danh mục sản phẩm của cửa hàng, người dùng có thể sửa hoặc xóa danh mục sản phẩm
    + Nếu nhấn nút "sửa" thì sẽ được điều hướng tới trang cập nhật danh mục sản phẩm
    + Nếu nhấn nút "xóa" thì sẽ xóa danh mục sản phẩm đó ra khỏi danh sách danh mục sản phẩm.

- Khi nhấn vào "Quản lý sản phẩm" trên thanh bar thì trình duyệt vẫn ở nguyên trang đó và sẽ thả xuống menu gồm "thêm danh mục sản phẩm", "thêm thương hiệu", "thêm sản phẩm". 
    + Nếu nhấn vào "thêm danh mục sản phẩm" thì sẽ được điều hướng tới trang thêm danh mục sản phẩm.
    + Nếu nhấn vào "thêm thương hiệu" thì sẽ được điều hướng tới trang thêm thương hiệu.
    + Nếu nhấn vào "thêm sản phẩm" thì sẽ được điều hướng tới trang thêm sản phẩm.

- Khi nhấn vào "Quản lý người dùng" trên thanh bar thì sẽ được điều hướng tới trang quản lý người dùng.
    + Hiển thị ra tất cả các tài khoản của cửa hàng, admin có thể xóa tài khoản người dùng.

- Khi nhấn vào "Tìm kiếm" trên thanh bar thì sẽ có 2 lựa chọn là tìm kiếm theo người dùng hoặc sản phẩm. 
    + Nếu điền từ khóa và chọn tìm kiếm theo người dùng thì sẽ hiển thị ra tất cả các tài khoản của cửa hàng có tên tài khoản, tên người dùng và email chứa từ khóa tìm kiếm.
    + Nếu điền từ khóa và chọn tìm kiếm theo sản phẩm thì sẽ hiển thị ra tất cả các sản phẩm của cửa hàng có tên sản phẩm, thương hiệu, danh mục chứa từ khóa tìm kiếm.

- Khi nhấn vào "Đăng xuất" trên thanh bar thì sẽ được điều hướng tới trang login của admin và thông báo đăng xuất thành công.

## 3. Yêu cầu phi chức năng
+ Hiệu suất: Độ trễ tối đa của trang web là 3 giây.
+ Khả năng bảo mật: Đảm bảo không lộ dữ liệu cá nhân của người dùng, không truy cập được quyền của admin nếu không phải admin
+ Khả năng mở rộng: Có thể mở rộng thêm các chức năng mới trong tương lai.
+ Khả năng tương thích: Có thể chạy trên nhiều nền tảng khác nhau.
+ Độ tin cậy: ...

## 4. Yêu cầu giao diện người dùng (UI)
+ Bố cục giao diện: Dễ sử dụng cho cả người dùng điện thoại và laptop.
+ Phong cách thiết kế: Màu đỏ và trắng là tông màu chủ đạo, font chữa sử dụng là font chữ "Roboto". Chân trang được thiết kế đơn giản, dễ nhìn, chữ trắng, nền đen.
+ Tiêu chuẩn và hướng dẫn UI: Quy tắc về UX/UI để đảm bảo tính nhất quán và dễ sử dụng.

## 5. Kiến trúc hệ thống
### 5.1 Mô hình kiến trúc
- Các thành phần hệ thống tổ chức theo mô hình MVC gồm:
    + Client: Trình duyêt web của người dùng.
    + Server: Máy chủ web để lưu trữ dữ liệu và xử lý các yêu cầu từ client.
    + Database: Cơ sở dữ liệu để lưu trữ dữ liệu của hệ thống.

- Sơ đồ hệ thống:
Client <----> Server <----> Database

- Yêu cầu hạ tầng:
    + Cấu hình máy chủ: Dùng gunicorn để chạy ứng dụng Flask. Cấu hình máy chủ cần có ít nhất 1GB RAM, 1 CPU. Nginx để làm proxy server.
    + Cơ sở dữ liệu: Dùng Sqlite3 để lưu trữ dữ liệu.

## 6. Quy trình xử lý dữ liệu
+ Dữ liệu đầu vào và đầu ra: Dữ liệu đầu vào là các thông tin nhập từ người dùng, dữ liệu đầu ra là các thông tin hiển thị trên trang web.

+ Luồng xử lý dữ liệu: Dữ liệu đầu vào sẽ được xử lý bởi máy chủ web, sau đó được lưu trữ trong cơ sở dữ liệu.

+ Lưu trữ dữ liệu: Dữ liệu được lưu trữ trong cơ sở dữ liệu.

## 7. Yêu cầu kiểm thử
### 7.1. Các trường hợp kiểm thử (test cases)
+ Kiểm thử tính đúng đắn: Kiểm tra xem hệ thống có hoạt động đúng theo yêu cầu hay không.
+ Kiểm thử bảo mật: Kiểm tra xem hệ thống có bảo mật dữ liệu người dùng hay không, có lỗ hỏng nào không.
+ Kiểm thử hiệu năng: Kiểm tra xem hệ thống có hoạt động có đáp ứng được số lượng người dùng đồng thời hay không, độ trễ có đáp ứng yêu cầu hay không, có hoạt động ổn định không
+ Tiêu chuẩn chấp nhận: Đạt điều kiện để mỗi chức năng đạt yêu cầu và chấp nhận được:
    + Độ trễ khi load 1 trang tối đa 60s.
    + Độ trễ khi thêm, sửa, xóa 1 sản phẩm tối đa 3s.

## 8. Yêu cầu bảo mật
+ Bảo vệ dữ liệu người dùng: Tuân thủ chính sách bảo mật dữ liệu theo chuẩn ISO 27001.
+ Quyền hạn người dùng: Đảm bảo người dùng có đúng quyền hạn truy cập vào các tài nguyên của hệ thống.
+ Bảo vệ ứng dụng: Yêu cầu về ngăn ngừa các mối đe dọa bảo mật (ví dụ: chống lại tấn công SQL Injection, XSS, DDoS,...).

## 9. Rủi ro và kế hoạch dự phòng
- Xác định rủi ro: 
    + Dữ liệu có thể bị đánh cắp hoặc mất => cần có kế hoạch mã hóa dữ liệu và backup dữ liệu thường xuyên.
    + Kế họach dự phòng: Có kế hoạch dự phòng cho các tình huống bất thường như sự cố mất điện, mất kết nối mạng, ...

## 10. Kế hoạch bảo trì và cập nhật
- Chu kì cập nhật: Mỗi tháng 1 lần, cập nhật các bản cập nhật và cập nhật các tính năng mới.
- Yêu cầu bảo trì: Kiểm tra tính ổn định, hiệu suất và bảo mật của hệ thống.



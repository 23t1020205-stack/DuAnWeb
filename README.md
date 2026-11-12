# 📚 BookNest – Ứng dụng quản lý sách

**BookNest** là một ứng dụng web nhỏ được xây dựng bằng **Python Flask** và **SQLite**, giúp quản lý sách và phân loại sách theo danh mục. Dự án tập trung vào các thao tác CRUD cơ bản, giao diện gọn gàng và cách tổ chức mã nguồn dễ theo dõi.

## ✨ Chức năng chính

- **Tổng quan:** xem tổng số danh mục, tổng số đầu sách và số đầu sách của từng danh mục.
- **Quản lý danh mục:** thêm, xem chi tiết, chỉnh sửa và xóa danh mục.
- **Quản lý sách:** thêm sách, xem thông tin, cập nhật hoặc xóa sách.
- **Lọc sách:** hiển thị danh sách sách theo danh mục đã chọn.
- **Kiểm tra dữ liệu:** yêu cầu thông tin bắt buộc, kiểm tra giá và số lượng hợp lệ; ngăn xóa danh mục còn sách liên kết.

> Lưu ý: “Tổng số sách” trên Dashboard đếm **đầu sách**, không phải tổng số lượng tồn kho.

## 🧰 Công nghệ sử dụng

| Thành phần | Công nghệ |
| --- | --- |
| Backend | Python, Flask |
| Cơ sở dữ liệu | SQLite |
| Giao diện | HTML, CSS, Jinja2 |
| Quản lý thư viện | pip, `requirements.txt` |

## 🚀 Cài đặt và chạy dự án

**Yêu cầu:** Python 3.10 trở lên và pip.

**Bước 1.** Tải dự án về máy (hoặc clone repository), sau đó mở terminal trong thư mục có tệp `app.py`.

**Bước 2.** Tạo môi trường ảo và cài các thư viện cần thiết.

Trên **Windows PowerShell**:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

Trên **macOS / Linux**:

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
```

**Bước 3.** Khởi tạo bảng dữ liệu và khởi chạy website.

Trên **Windows PowerShell**:

```powershell
.\.venv\Scripts\python.exe init_db.py
.\.venv\Scripts\python.exe app.py
```

Trên **macOS / Linux**:

```bash
.venv/bin/python init_db.py
.venv/bin/python app.py
```

**Bước 4.** Mở trình duyệt tại **http://127.0.0.1:5001**.

Để bắt đầu sử dụng, hãy tạo một **danh mục** trước, rồi vào trang **Sách** để thêm sách. Nhấn `Ctrl + C` trong terminal để dừng server.

*Ghi chú:* `init_db.py` chỉ tạo bảng nếu chưa tồn tại, không xóa dữ liệu cũ. Dự án có sẵn tệp `data/books.db`; SQLite được sử dụng trực tiếp, không cần cài server cơ sở dữ liệu riêng.

## 📁 Cấu trúc thư mục

```text
baikiemtra-main/
├── app.py                  # Routes và xử lý chức năng
├── database.py             # Kết nối SQLite
├── init_db.py              # Khởi tạo các bảng
├── requirements.txt        # Danh sách thư viện
├── data/
│   └── books.db            # Cơ sở dữ liệu
├── static/
│   └── style.css           # Giao diện CSS
└── templates/
    ├── base.html           # Bố cục chung và menu
    ├── dashboard.html      # Trang tổng quan
    ├── categories.html     # Danh sách danh mục
    ├── category_detail.html
    ├── category_form.html
    ├── books.html          # Danh sách và bộ lọc sách
    ├── book_detail.html
    └── book_form.html
```

## 🎨 Giao diện

BookNest sử dụng tông **xanh tím – trắng**, thanh điều hướng rõ ràng, các thẻ thống kê và biểu mẫu được thiết kế thống nhất. Giao diện có điều chỉnh để hiển thị thuận tiện trên màn hình nhỏ.

## 📝 Thông tin thêm

Đây là dự án thực hành lập trình web với Flask và SQLite, phù hợp để tìm hiểu cách kết nối giao diện với cơ sở dữ liệu, xử lý biểu mẫu và thực hiện các thao tác **Create – Read – Update – Delete (CRUD)**.

Ứng dụng hiện chạy ở môi trường local, chưa tích hợp đăng nhập hoặc phân quyền người dùng.

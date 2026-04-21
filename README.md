# G-Scores - Web Intern Assignment Implementation

Ứng dụng web tra cứu điểm thi THPT 2024, thống kê phổ điểm theo môn, và hiển thị top 10 thí sinh khối A.

## Tính năng đã làm

### Must have
- Import dữ liệu CSV `dataset/diem_thi_thpt_2024.csv` vào database SQLite thông qua script seed (`init_db.py`).
- Tra cứu điểm theo số báo danh (SBD).
- Báo cáo phổ điểm theo 4 mức cho từng môn:
  - `>= 8`
  - `6 - < 8`
  - `4 - < 6`
  - `< 4`
- Top 10 thí sinh khối A (Toán, Vật lý, Hóa học).

### OOP requirement
- Logic quản lý môn học và báo cáo được tổ chức qua lớp `SubjectManager` trong `models.py`.

## Tech stack
- Backend: Flask + Flask-SQLAlchemy
- Database: SQLite
- Frontend: HTML/CSS + vanilla JS + Chart.js

## Cấu trúc chính

- `app.py`: Flask app và các routes.
- `models.py`: ORM model `StudentScore` + OOP class `SubjectManager`.
- `init_db.py`: tạo bảng + seed CSV.
- `templates/`: giao diện.
- `static/style.css`: styling.

## Chạy local

### 1) Tạo môi trường và cài dependencies

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 2) Khởi tạo database + seed data

```bash
python init_db.py
```

### 3) Chạy ứng dụng

```bash
python app.py
```

Mở trình duyệt tại: `http://127.0.0.1:5000`

## Endpoints

- `GET /` - Trang tra cứu điểm
- `GET /lookup?sbd=<so_bao_danh>` - API tra cứu điểm
- `GET /report` - Trang báo cáo phổ điểm (chart)
- `GET /top10-group-a` - Trang top 10 khối A

## Validation

- `sbd` bắt buộc.
- `sbd` chỉ chấp nhận ký tự số.
- Không tìm thấy dữ liệu theo SBD trả về `404`.

## Ghi chú

- Dữ liệu điểm trống trong CSV được quy đổi thành `NULL` trong database.
- Chưa dockerize/deploy trong version này.

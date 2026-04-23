# G-Scores — Tra cứu Điểm Thi THPT 2024

Ứng dụng web tra cứu điểm thi THPT Quốc gia 2024, thống kê phổ điểm theo môn và xếp hạng top 10 thí sinh khối A.

## Giao diện

Project hiện dùng **Django + custom dashboard UI**. Frontend được xây bằng:

- HTML template
- CSS thuần
- Vanilla JavaScript
- Chart.js

Backend đã được chuyển từ Flask sang **Django**. Giao diện được làm lại theo hướng nhẹ hơn, ít phụ thuộc hơn và đồng nhất hơn giữa các trang.

## Screenshots

### Trang tra cứu điểm
![Trang tra cứu điểm](./screenshots/01-home.png)

### Kết quả tra cứu
![Kết quả tra cứu](./screenshots/02-search-results.png)

### Báo cáo phổ điểm
![Báo cáo phổ điểm](./screenshots/03-report.png)

### Top 10 khối A
![Top 10 khối A](./screenshots/04-top10.png)

## Tính năng

- Tra cứu điểm theo số báo danh
- Báo cáo phổ điểm 4 mức theo từng môn
- Top 10 thí sinh khối A
- Import CSV vào SQLite
- API JSON cho frontend

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | Django 5.2 |
| Database | SQLite |
| Frontend | Custom UI + HTML/CSS + Vanilla JS + Chart.js 4 |
| Production | Gunicorn + Docker |

## Cấu trúc chính

```text
├── config/                         # Django project settings/urls/wsgi
├── scores/                         # Django app: models, views, services, urls
├── templates/                      # Django templates
├── static/                         # Static assets
├── dataset/                        # CSV dataset (không track git)
├── manage.py                       # Django CLI entrypoint
├── init_db.py                      # Wrapper migrate + seed để tương thích command cũ
├── deploy/                         # entrypoint + gunicorn config
├── Dockerfile
├── docker-compose.yml
└── requirements.txt
```

## Chạy local

### 1) Cài dependencies

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 2) Chuẩn bị dataset

Tải file `diem_thi_thpt_2024.csv` và đặt vào `dataset/diem_thi_thpt_2024.csv`.

### 3) Migrate database

```bash
python manage.py migrate
```

### 4) Import dữ liệu

```bash
python manage.py seed_scores --reset
```

Hoặc giữ tương thích command cũ:

```bash
python init_db.py
```

### 5) Chạy server

```bash
python manage.py runserver
```

Mở `http://127.0.0.1:8000`

## API Endpoints

| Method | Endpoint | Mô tả |
|--------|----------|-------|
| `GET` | `/` | Trang tra cứu điểm |
| `GET` | `/report` | Trang báo cáo phổ điểm |
| `GET` | `/top10-group-a` | Trang top 10 khối A |
| `GET` | `/api/lookup?sbd=<sbd>` | API tra cứu điểm theo SBD |
| `GET` | `/api/report` | API dữ liệu phổ điểm |
| `GET` | `/api/top10` | API top 10 khối A |

## Docker

```bash
docker compose up --build -d
```

Container sẽ:

- cài dependencies và collect static ở build time
- chạy `migrate` khi container start
- tự seed dữ liệu nếu database còn trống và dataset tồn tại
- serve bằng Gunicorn tại cổng `5000`

### Biến môi trường deploy

| Biến | Mặc định | Mô tả |
|------|----------|-------|
| `DJANGO_DEBUG` | `false` trong Docker | Bật/tắt debug |
| `DJANGO_ALLOWED_HOSTS` | `localhost,127.0.0.1` | Danh sách host hợp lệ |
| `GSCORES_DATASET_PATH` | `dataset/diem_thi_thpt_2024.csv` | Đường dẫn file CSV |
| `GSCORES_AUTO_MIGRATE` | `true` | Tự chạy migrate khi start |
| `GSCORES_AUTO_SEED` | `true` | Tự seed nếu DB đang rỗng |

### Script deploy

```bash
./deploy.sh
```

Script sẽ rebuild container, chờ healthcheck HTTP và in log nếu deploy lỗi.

## Ghi chú

- Dữ liệu được import từ `dataset/diem_thi_thpt_2024.csv`
- ORM sử dụng Django ORM
- Logic quản lý môn học được tổ chức theo OOP trong `scores/services.py`

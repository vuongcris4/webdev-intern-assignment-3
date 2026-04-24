# G-Scores — Tra cứu Điểm Thi THPT Quốc gia 2024

> Ứng dụng web tra cứu điểm thi THPT Quốc gia 2024 với hơn **1 triệu bản ghi**, hỗ trợ tra cứu cá nhân, thống kê phổ điểm theo môn và xếp hạng top 10 thí sinh khối A.

🔗 **Live demo:** [gscores.dongnama.app](https://gscores.dongnama.app)

---

## ✨ Tính năng

| # | Tính năng | Mô tả |
|---|-----------|-------|
| 1 | **Tra cứu điểm** | Nhập số báo danh → hiển thị điểm 9 môn + mã ngoại ngữ |
| 2 | **Báo cáo phổ điểm** | Biểu đồ stacked bar thống kê 4 ngưỡng (≥8, 6–8, 4–6, <4) cho tất cả các môn |
| 3 | **Top 10 khối A** | Bảng xếp hạng 10 thí sinh có tổng điểm Toán + Lý + Hoá cao nhất |
| 4 | **API JSON** | 3 endpoint RESTful phục vụ frontend bất đồng bộ |
| 5 | **Docker one-command** | `./deploy.sh` — build, migrate, seed và healthcheck tự động |

---

## 📸 Giao diện

### Trang tra cứu điểm
![Trang tra cứu điểm](./screenshots/01-home.png)

### Kết quả tra cứu
![Kết quả tra cứu](./screenshots/02-search-results.png)

### Báo cáo phổ điểm
![Báo cáo phổ điểm](./screenshots/03-report.png)

### Top 10 khối A
![Top 10 khối A](./screenshots/04-top10.png)

---

## 🛠 Tech Stack

| Layer | Công nghệ |
|-------|-----------|
| **Backend** | Django 5.2, Gunicorn, WhiteNoise |
| **Database** | SQLite (1M+ records, auto-seed từ CSV) |
| **Frontend** | daisyUI 5 + Tailwind CSS 4 (CDN), Vanilla JS, Chart.js 4 |
| **Fonts** | Rubik (Google Fonts) |
| **Icons** | Font Awesome 6 |
| **Deploy** | Docker, docker-compose, healthcheck script |

---

## 📐 Kiến trúc OOP

Quản lý môn thi được thiết kế theo hướng OOP trong `scores/services.py`:

```
Subject (dataclass)              — Đại diện 1 môn thi, tự tính band phân loại
  └── count_bands()              — Aggregate Django ORM → dict 4 ngưỡng

SubjectManager                   — Coordinator quản lý toàn bộ Subject
  ├── find_by_sbd(sbd)           — Tra cứu thí sinh
  ├── build_subject_report()     — Tổng hợp phổ điểm toàn bộ môn (cached)
  ├── dashboard_stats()          — Thống kê tổng quan (cached)
  └── top10_group_a()            — Xếp hạng khối A
```

---

## 📁 Cấu trúc dự án

```text
webdev-intern-assignment-3/
├── config/                  # Django settings, urls, wsgi
├── scores/                  # Django app chính
│   ├── models.py            #   StudentScore ORM model
│   ├── services.py          #   Subject + SubjectManager (OOP)
│   ├── views.py             #   Page views + API views
│   ├── urls.py              #   URL routing
│   └── management/          #   Custom command: seed_scores
├── templates/               # Django templates (daisyUI components)
│   ├── base.html            #   Layout: sidebar + navbar + drawer
│   ├── index.html           #   Trang tra cứu
│   ├── report.html          #   Trang phổ điểm + Chart.js
│   └── top10.html           #   Trang top 10 khối A
├── dataset/                 # CSV dataset (không track git)
├── deploy/                  # entrypoint.sh + gunicorn.conf.py
├── screenshots/             # Ảnh chụp giao diện
├── Dockerfile
├── docker-compose.yml
├── deploy.sh                # Script deploy one-command
├── manage.py
├── init_db.py               # Wrapper tương thích lệnh cũ
└── requirements.txt
```

---

## 🚀 Chạy local

### 1. Cài dependencies

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 2. Chuẩn bị dataset

Đặt file CSV vào `dataset/diem_thi_thpt_2024.csv`.

### 3. Migrate & seed

```bash
python manage.py migrate
python manage.py seed_scores --reset
```

### 4. Chạy server

```bash
python manage.py runserver
```

Truy cập: **http://127.0.0.1:8000**

---

## 🐳 Docker

### Quick start

```bash
./deploy.sh
```

Script sẽ tự động: rebuild image → start container → chờ healthcheck HTTP 200 → in kết quả.

### Hoặc chạy thủ công

```bash
docker compose up --build -d
```

Container sẽ:
- Cài dependencies & collect static ở build time
- Chạy `migrate` khi start
- Tự seed dữ liệu nếu DB còn trống và dataset tồn tại
- Serve bằng Gunicorn tại cổng **5000**

### Biến môi trường

| Biến | Mặc định | Mô tả |
|------|----------|-------|
| `DJANGO_DEBUG` | `false` | Bật/tắt debug mode |
| `DJANGO_ALLOWED_HOSTS` | `localhost,127.0.0.1` | Danh sách host hợp lệ |
| `DJANGO_CSRF_TRUSTED_ORIGINS` | — | Origins cho CSRF (production) |
| `GSCORES_DATASET_PATH` | `dataset/diem_thi_thpt_2024.csv` | Đường dẫn file CSV |
| `GSCORES_AUTO_MIGRATE` | `true` | Tự chạy migrate khi start |
| `GSCORES_AUTO_SEED` | `true` | Tự seed nếu DB đang rỗng |

---

## 🔌 API Endpoints

| Method | Endpoint | Response |
|--------|----------|----------|
| `GET` | `/` | Trang tra cứu điểm (HTML) |
| `GET` | `/report` | Trang báo cáo phổ điểm (HTML) |
| `GET` | `/top10-group-a` | Trang top 10 khối A (HTML) |
| `GET` | `/api/lookup?sbd=<sbd>` | JSON — điểm 9 môn + mã ngoại ngữ |
| `GET` | `/api/report` | JSON — phổ điểm 4 band × 9 môn |
| `GET` | `/api/top10` | JSON — top 10 thí sinh khối A |

---

## 📝 Ghi chú kỹ thuật

- **ORM:** Django ORM với `StudentScore` model, index trên `sbd`
- **Caching:** `@lru_cache` cho dashboard stats và subject report (tránh query lặp)
- **Static files:** WhiteNoise serve trực tiếp, không cần Nginx riêng
- **UI framework:** daisyUI 5 + Tailwind CSS 4 qua CDN — không cần build step cho frontend
- **Font:** Rubik (Google Fonts), load qua `preconnect` để tối ưu
- **Charts:** Chart.js 4, stacked bar với tooltip tùy chỉnh
- **Responsive:** Drawer layout — sidebar cố định trên desktop, hamburger trên mobile

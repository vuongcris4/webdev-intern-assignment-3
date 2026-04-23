"""Database initialization and CSV data seeding script.

Reads the raw CSV dataset and inserts records into SQLite
using batch inserts for memory efficiency.
"""
import csv
import sys
from pathlib import Path

from app import create_app
from models import StudentScore, db

CSV_PATH = Path("DE-BAI/dataset/diem_thi_thpt_2024.csv")
BATCH_SIZE = 5000


def parse_float(value: str):
    """Parse a string to float, returning None for empty/missing values."""
    value = (value or "").strip()
    if value == "":
        return None
    return float(value)


def seed_data():
    """Seed the database from the CSV file with batch inserts."""
    if not CSV_PATH.exists():
        raise FileNotFoundError(f"Dataset not found: {CSV_PATH}")

    # Count total lines for progress
    total_lines = sum(1 for _ in CSV_PATH.open(encoding="utf-8")) - 1
    print(f"📊 Found {total_lines:,} records to import...")

    with CSV_PATH.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        batch = []
        count = 0

        for row in reader:
            batch.append(
                StudentScore(
                    sbd=row["sbd"].strip(),
                    toan=parse_float(row.get("toan")),
                    ngu_van=parse_float(row.get("ngu_van")),
                    ngoai_ngu=parse_float(row.get("ngoai_ngu")),
                    vat_li=parse_float(row.get("vat_li")),
                    hoa_hoc=parse_float(row.get("hoa_hoc")),
                    sinh_hoc=parse_float(row.get("sinh_hoc")),
                    lich_su=parse_float(row.get("lich_su")),
                    dia_li=parse_float(row.get("dia_li")),
                    gdcd=parse_float(row.get("gdcd")),
                    ma_ngoai_ngu=(row.get("ma_ngoai_ngu") or "").strip() or None,
                )
            )

            if len(batch) >= BATCH_SIZE:
                db.session.bulk_save_objects(batch)
                db.session.commit()
                count += len(batch)
                pct = count / total_lines * 100
                sys.stdout.write(f"\r⏳ Importing... {count:,}/{total_lines:,} ({pct:.1f}%)")
                sys.stdout.flush()
                batch = []

        # Insert remaining records
        if batch:
            db.session.bulk_save_objects(batch)
            db.session.commit()
            count += len(batch)

    print(f"\n✅ Successfully imported {count:,} records.")


if __name__ == "__main__":
    app = create_app()
    with app.app_context():
        print("🗄️  Initializing database...")
        db.drop_all()
        db.create_all()
        seed_data()
        print("🎉 Database initialized and seeded successfully!")

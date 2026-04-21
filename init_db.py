import csv
from pathlib import Path

from app import create_app
from models import StudentScore, db


CSV_PATH = Path("dataset/diem_thi_thpt_2024.csv")


def parse_float(value: str):
    value = (value or "").strip()
    if value == "":
        return None
    return float(value)


def seed_data():
    if not CSV_PATH.exists():
        raise FileNotFoundError(f"Dataset not found: {CSV_PATH}")

    with CSV_PATH.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        records = []
        for row in reader:
            records.append(
                StudentScore(
                    sbd=row["sbd"].strip(),
                    toan=parse_float(row["toan"]),
                    ngu_van=parse_float(row["ngu_van"]),
                    ngoai_ngu=parse_float(row["ngoai_ngu"]),
                    vat_li=parse_float(row["vat_li"]),
                    hoa_hoc=parse_float(row["hoa_hoc"]),
                    sinh_hoc=parse_float(row["sinh_hoc"]),
                    lich_su=parse_float(row["lich_su"]),
                    dia_li=parse_float(row["dia_li"]),
                    gdcd=parse_float(row["gdcd"]),
                    ma_ngoai_ngu=(row["ma_ngoai_ngu"] or "").strip() or None,
                )
            )
    db.session.bulk_save_objects(records)
    db.session.commit()


if __name__ == "__main__":
    app = create_app()
    with app.app_context():
        db.drop_all()
        db.create_all()
        seed_data()
        print("Database initialized and seeded successfully.")

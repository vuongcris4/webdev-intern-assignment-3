"""Seed the database from the THPT exam CSV dataset."""
import csv

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from scores.models import StudentScore

BATCH_SIZE = 5000
CSV_COLUMNS = (
    "toan",
    "ngu_van",
    "ngoai_ngu",
    "vat_li",
    "hoa_hoc",
    "sinh_hoc",
    "lich_su",
    "dia_li",
    "gdcd",
)


def parse_float(value: str):
    value = (value or "").strip()
    if value == "":
        return None
    try:
        return float(value)
    except ValueError:
        return None


class Command(BaseCommand):
    help = "Import diem_thi_thpt_2024.csv into the database."

    def add_arguments(self, parser):
        parser.add_argument("--reset", action="store_true", help="Delete existing score data before import.")
        parser.add_argument("--batch-size", type=int, default=BATCH_SIZE, help="Bulk insert batch size.")

    def handle(self, *args, **options):
        csv_path = settings.DATASET_PATH
        batch_size = options["batch_size"]

        if not csv_path.exists():
            raise CommandError(
                f"Dataset not found: {csv_path}. "
                "Please place diem_thi_thpt_2024.csv in the dataset/ directory."
            )

        total_lines = sum(1 for _ in csv_path.open(encoding="utf-8")) - 1
        self.stdout.write(f"Found {total_lines:,} records to import...")

        batch = []
        imported = 0

        with transaction.atomic():
            if options["reset"]:
                StudentScore.objects.all().delete()

            with csv_path.open(newline="", encoding="utf-8") as dataset:
                reader = csv.DictReader(dataset)

                for row in reader:
                    score_data = {column: parse_float(row.get(column)) for column in CSV_COLUMNS}
                    batch.append(
                        StudentScore(
                            sbd=row["sbd"].strip(),
                            ma_ngoai_ngu=(row.get("ma_ngoai_ngu") or "").strip() or None,
                            **score_data,
                        )
                    )

                    if len(batch) >= batch_size:
                        StudentScore.objects.bulk_create(batch, batch_size=batch_size)
                        imported += len(batch)
                        pct = imported / total_lines * 100
                        self.stdout.write(
                            f"Imported {imported:,}/{total_lines:,} records ({pct:.1f}%)",
                            ending="\r",
                        )
                        batch = []

            if batch:
                StudentScore.objects.bulk_create(batch, batch_size=batch_size)
                imported += len(batch)

        self.stdout.write("")
        self.stdout.write(self.style.SUCCESS(f"Successfully imported {imported:,} records."))

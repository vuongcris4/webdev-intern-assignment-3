"""Business logic for score lookup, analytics, and ranking."""
from __future__ import annotations

from dataclasses import dataclass
from functools import cached_property, lru_cache

from django.db.models import Case, Count, F, Q, Value, When

from .models import StudentScore

BAND_EXCELLENT = "ge_8"
BAND_GOOD = "ge_6_lt_8"
BAND_AVERAGE = "ge_4_lt_6"
BAND_WEAK = "lt_4"


@dataclass(frozen=True)
class Subject:
    """Represents a single exam subject with metadata and scoring logic."""

    column: str
    display_name: str

    def count_bands(self) -> dict:
        result = StudentScore.objects.filter(**{f"{self.column}__isnull": False}).aggregate(
            ge_8=Count(Case(When(**{f"{self.column}__gte": 8}, then=Value(1)))),
            ge_6_lt_8=Count(
                Case(
                    When(
                        Q(**{f"{self.column}__gte": 6}) & Q(**{f"{self.column}__lt": 8}),
                        then=Value(1),
                    )
                )
            ),
            ge_4_lt_6=Count(
                Case(
                    When(
                        Q(**{f"{self.column}__gte": 4}) & Q(**{f"{self.column}__lt": 6}),
                        then=Value(1),
                    )
                )
            ),
            lt_4=Count(Case(When(**{f"{self.column}__lt": 4}, then=Value(1)))),
        )

        return {
            "display_name": self.display_name,
            BAND_EXCELLENT: result[BAND_EXCELLENT],
            BAND_GOOD: result[BAND_GOOD],
            BAND_AVERAGE: result[BAND_AVERAGE],
            BAND_WEAK: result[BAND_WEAK],
        }


class SubjectManager:
    """Coordinates subject lookup, reporting, and top-10 ranking logic."""

    SUBJECTS = (
        Subject("toan", "Toán"),
        Subject("ngu_van", "Ngữ văn"),
        Subject("ngoai_ngu", "Ngoại ngữ"),
        Subject("vat_li", "Vật lý"),
        Subject("hoa_hoc", "Hóa học"),
        Subject("sinh_hoc", "Sinh học"),
        Subject("lich_su", "Lịch sử"),
        Subject("dia_li", "Địa lý"),
        Subject("gdcd", "GDCD"),
    )

    @property
    def subjects(self) -> tuple[Subject, ...]:
        return self.SUBJECTS

    @cached_property
    def subject_map(self) -> dict[str, Subject]:
        return {subject.column: subject for subject in self.subjects}

    def get_subject(self, column_name: str) -> Subject | None:
        return self.subject_map.get(column_name)

    def find_by_sbd(self, sbd: str) -> StudentScore | None:
        return StudentScore.objects.filter(sbd=sbd).first()

    @lru_cache(maxsize=1)
    def build_subject_report(self) -> dict[str, dict]:
        return {subject.column: subject.count_bands() for subject in self.subjects}

    @lru_cache(maxsize=1)
    def dashboard_stats(self) -> dict[str, int]:
        return {
            "total_records": StudentScore.objects.count(),
            "subject_count": len(self.subjects),
            "group_a_candidates": StudentScore.objects.filter(
                toan__isnull=False,
                vat_li__isnull=False,
                hoa_hoc__isnull=False,
            ).count(),
        }

    def top10_group_a(self) -> list[dict]:
        students = (
            StudentScore.objects.filter(
                toan__isnull=False,
                vat_li__isnull=False,
                hoa_hoc__isnull=False,
            )
            .annotate(total=F("toan") + F("vat_li") + F("hoa_hoc"))
            .order_by("-total")[:10]
        )

        return [
            {
                "sbd": student.sbd,
                "toan": student.toan,
                "vat_li": student.vat_li,
                "hoa_hoc": student.hoa_hoc,
                "total": round(student.total, 2),
            }
            for student in students
        ]

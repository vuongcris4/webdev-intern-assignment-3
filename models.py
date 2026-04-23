"""OOP models for G-Scores exam score management.

Demonstrates:
- Encapsulation: Subject encapsulates column metadata and scoring logic.
- Composition: SubjectManager manages a collection of Subject objects.
- Single Responsibility: Each class has one clear purpose.
"""
from __future__ import annotations

from typing import Dict, List, Optional

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import case, func

db = SQLAlchemy()


class StudentScore(db.Model):
    """ORM model representing a student's national exam scores."""

    __tablename__ = "student_scores"

    id = db.Column(db.Integer, primary_key=True)
    sbd = db.Column(db.String(20), unique=True, nullable=False, index=True)
    toan = db.Column(db.Float, nullable=True)
    ngu_van = db.Column(db.Float, nullable=True)
    ngoai_ngu = db.Column(db.Float, nullable=True)
    vat_li = db.Column(db.Float, nullable=True)
    hoa_hoc = db.Column(db.Float, nullable=True)
    sinh_hoc = db.Column(db.Float, nullable=True)
    lich_su = db.Column(db.Float, nullable=True)
    dia_li = db.Column(db.Float, nullable=True)
    gdcd = db.Column(db.Float, nullable=True)
    ma_ngoai_ngu = db.Column(db.String(10), nullable=True)

    def to_dict(self) -> dict:
        """Serialize student scores to a dictionary."""
        return {
            "sbd": self.sbd,
            "toan": self.toan,
            "ngu_van": self.ngu_van,
            "ngoai_ngu": self.ngoai_ngu,
            "vat_li": self.vat_li,
            "hoa_hoc": self.hoa_hoc,
            "sinh_hoc": self.sinh_hoc,
            "lich_su": self.lich_su,
            "dia_li": self.dia_li,
            "gdcd": self.gdcd,
            "ma_ngoai_ngu": self.ma_ngoai_ngu,
        }


# ── Score Band Constants ─────────────────────────────────────
BAND_EXCELLENT = "ge_8"       # >= 8
BAND_GOOD = "ge_6_lt_8"      # 6 — <8
BAND_AVERAGE = "ge_4_lt_6"   # 4 — <6
BAND_WEAK = "lt_4"           # < 4


class Subject:
    """Represents a single exam subject with its metadata and scoring logic.

    Encapsulates the column name, display name, and provides methods
    to query score distributions for this specific subject.

    Attributes:
        column: Database column name (e.g., 'toan', 'vat_li').
        display_name: Human-readable Vietnamese name (e.g., 'Toán', 'Vật lý').
    """

    def __init__(self, column: str, display_name: str) -> None:
        self.column = column
        self.display_name = display_name

    @property
    def orm_column(self):
        """Get the SQLAlchemy column object for this subject."""
        return getattr(StudentScore, self.column)

    def count_bands(self) -> dict:
        """Count students in each of the 4 score bands for this subject.

        Uses SQL CASE expressions for efficient aggregation on 1M+ records
        without loading data into Python memory.

        Returns:
            Dict with keys: display_name, ge_8, ge_6_lt_8, ge_4_lt_6, lt_4.
        """
        col = self.orm_column

        result = db.session.query(
            func.count(case((col >= 8, 1))).label(BAND_EXCELLENT),
            func.count(case((db.and_(col >= 6, col < 8), 1))).label(BAND_GOOD),
            func.count(case((db.and_(col >= 4, col < 6), 1))).label(BAND_AVERAGE),
            func.count(case((col < 4, 1))).label(BAND_WEAK),
        ).filter(col.isnot(None)).first()

        return {
            "display_name": self.display_name,
            BAND_EXCELLENT: result.ge_8,
            BAND_GOOD: result.ge_6_lt_8,
            BAND_AVERAGE: result.ge_4_lt_6,
            BAND_WEAK: result.lt_4,
        }

    def __repr__(self) -> str:
        return f"Subject(column={self.column!r}, display_name={self.display_name!r})"


class SubjectManager:
    """Manages a collection of Subject objects and provides analytics.

    Demonstrates OOP composition: SubjectManager owns and coordinates
    multiple Subject instances. All business logic for score lookup,
    reporting, and ranking is encapsulated here.

    Attributes:
        subjects: List of all Subject objects.
    """

    def __init__(self) -> None:
        self.subjects: List[Subject] = [
            Subject("toan", "Toán"),
            Subject("ngu_van", "Ngữ văn"),
            Subject("ngoai_ngu", "Ngoại ngữ"),
            Subject("vat_li", "Vật lý"),
            Subject("hoa_hoc", "Hóa học"),
            Subject("sinh_hoc", "Sinh học"),
            Subject("lich_su", "Lịch sử"),
            Subject("dia_li", "Địa lý"),
            Subject("gdcd", "GDCD"),
        ]
        self._subject_map: Dict[str, Subject] = {
            s.column: s for s in self.subjects
        }

        # Cache for report data (invalidated on app restart)
        self._report_cache: Optional[Dict[str, dict]] = None

    def get_subject(self, column_name: str) -> Optional[Subject]:
        """Look up a Subject by its column name."""
        return self._subject_map.get(column_name)

    def find_by_sbd(self, sbd: str) -> Optional[StudentScore]:
        """Find a student by their registration number (SBD)."""
        return StudentScore.query.filter_by(sbd=sbd).first()

    def build_subject_report(self) -> Dict[str, dict]:
        """Build score distribution report for all subjects.

        Delegates to each Subject's count_bands() method (composition).
        Results are cached since exam data is static.

        Returns:
            Dict mapping subject column name to band counts + display_name.
        """
        if self._report_cache is not None:
            return self._report_cache

        report = {}
        for subject in self.subjects:
            report[subject.column] = subject.count_bands()

        self._report_cache = report
        return report

    def top10_group_a(self) -> List[dict]:
        """Get top 10 students by Group A total score (Math + Physics + Chemistry).

        Uses SQL-level sorting and limiting for optimal performance.
        """
        total_expr = StudentScore.toan + StudentScore.vat_li + StudentScore.hoa_hoc

        students = (
            StudentScore.query
            .filter(
                StudentScore.toan.isnot(None),
                StudentScore.vat_li.isnot(None),
                StudentScore.hoa_hoc.isnot(None),
            )
            .order_by(total_expr.desc())
            .limit(10)
            .all()
        )

        return [
            {
                "sbd": s.sbd,
                "toan": s.toan,
                "vat_li": s.vat_li,
                "hoa_hoc": s.hoa_hoc,
                "total": round(s.toan + s.vat_li + s.hoa_hoc, 2),
            }
            for s in students
        ]

from __future__ import annotations

from dataclasses import dataclass, asdict
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


@dataclass
class ScoreBand:
    """Score distribution for a single subject across 4 bands."""
    ge_8: int = 0
    ge_6_lt_8: int = 0
    ge_4_lt_6: int = 0
    lt_4: int = 0


class SubjectManager:
    """OOP manager for subject-related analytics and queries.

    Encapsulates all business logic for score lookup, reporting,
    and ranking. Uses SQL-level aggregation for performance on 1M+ records.
    """

    SUBJECT_COLUMNS = [
        "toan",
        "ngu_van",
        "ngoai_ngu",
        "vat_li",
        "hoa_hoc",
        "sinh_hoc",
        "lich_su",
        "dia_li",
        "gdcd",
    ]

    SUBJECT_DISPLAY_NAMES = {
        "toan": "Toán",
        "ngu_van": "Ngữ văn",
        "ngoai_ngu": "Ngoại ngữ",
        "vat_li": "Vật lý",
        "hoa_hoc": "Hóa học",
        "sinh_hoc": "Sinh học",
        "lich_su": "Lịch sử",
        "dia_li": "Địa lý",
        "gdcd": "GDCD",
    }

    def find_by_sbd(self, sbd: str) -> Optional[StudentScore]:
        """Find a student by their registration number (SBD)."""
        return StudentScore.query.filter_by(sbd=sbd).first()

    def _band_for_score(self, value: float) -> str:
        """Classify a score into one of 4 bands."""
        if value >= 8:
            return "ge_8"
        if value >= 6:
            return "ge_6_lt_8"
        if value >= 4:
            return "ge_4_lt_6"
        return "lt_4"

    def build_subject_report(self) -> Dict[str, dict]:
        """Build score distribution report for all subjects using SQL aggregation.

        Returns a dict mapping subject column name to a dict with band counts
        and display_name.
        """
        report: Dict[str, dict] = {}

        for subject in self.SUBJECT_COLUMNS:
            col = getattr(StudentScore, subject)

            # Use SQL CASE for counting each band — much faster than Python loop
            result = db.session.query(
                func.count(case((col >= 8, 1))).label("ge_8"),
                func.count(case((db.and_(col >= 6, col < 8), 1))).label("ge_6_lt_8"),
                func.count(case((db.and_(col >= 4, col < 6), 1))).label("ge_4_lt_6"),
                func.count(case((col < 4, 1))).label("lt_4"),
            ).filter(col.isnot(None)).first()

            report[subject] = {
                "display_name": self.SUBJECT_DISPLAY_NAMES[subject],
                "ge_8": result.ge_8,
                "ge_6_lt_8": result.ge_6_lt_8,
                "ge_4_lt_6": result.ge_4_lt_6,
                "lt_4": result.lt_4,
            }

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

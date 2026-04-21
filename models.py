from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Iterable, List, Optional

from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


class StudentScore(db.Model):
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


@dataclass
class ScoreBand:
    ge_8: int = 0
    ge_6_lt_8: int = 0
    ge_4_lt_6: int = 0
    lt_4: int = 0


class SubjectManager:
    """OOP manager for subject-related analytics and queries."""

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

    def find_by_sbd(self, sbd: str) -> Optional[StudentScore]:
        return StudentScore.query.filter_by(sbd=sbd).first()

    def _band_for_score(self, value: float) -> str:
        if value >= 8:
            return "ge_8"
        if value >= 6:
            return "ge_6_lt_8"
        if value >= 4:
            return "ge_4_lt_6"
        return "lt_4"

    def build_subject_report(self) -> Dict[str, ScoreBand]:
        report: Dict[str, ScoreBand] = {s: ScoreBand() for s in self.SUBJECT_COLUMNS}
        students: Iterable[StudentScore] = StudentScore.query.all()
        for student in students:
            for subject in self.SUBJECT_COLUMNS:
                value = getattr(student, subject)
                if value is None:
                    continue
                band = self._band_for_score(value)
                setattr(report[subject], band, getattr(report[subject], band) + 1)
        return report

    def top10_group_a(self) -> List[dict]:
        students: Iterable[StudentScore] = StudentScore.query.all()
        payload: List[dict] = []
        for student in students:
            if student.toan is None or student.vat_li is None or student.hoa_hoc is None:
                continue
            total = student.toan + student.vat_li + student.hoa_hoc
            payload.append(
                {
                    "sbd": student.sbd,
                    "toan": student.toan,
                    "vat_li": student.vat_li,
                    "hoa_hoc": student.hoa_hoc,
                    "total": round(total, 2),
                }
            )
        payload.sort(key=lambda x: x["total"], reverse=True)
        return payload[:10]

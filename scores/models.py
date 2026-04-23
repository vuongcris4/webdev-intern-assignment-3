"""ORM models for G-Scores exam score management."""
from django.db import models


class StudentScore(models.Model):
    """ORM model representing a student's national exam scores."""

    SUBJECT_FIELDS = (
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

    sbd = models.CharField(max_length=20, unique=True, db_index=True)
    toan = models.FloatField(null=True, blank=True)
    ngu_van = models.FloatField(null=True, blank=True)
    ngoai_ngu = models.FloatField(null=True, blank=True)
    vat_li = models.FloatField(null=True, blank=True)
    hoa_hoc = models.FloatField(null=True, blank=True)
    sinh_hoc = models.FloatField(null=True, blank=True)
    lich_su = models.FloatField(null=True, blank=True)
    dia_li = models.FloatField(null=True, blank=True)
    gdcd = models.FloatField(null=True, blank=True)
    ma_ngoai_ngu = models.CharField(max_length=10, null=True, blank=True)

    class Meta:
        db_table = "student_scores"

    def to_dict(self) -> dict:
        data = {"sbd": self.sbd, "ma_ngoai_ngu": self.ma_ngoai_ngu}
        data.update({field: getattr(self, field) for field in self.SUBJECT_FIELDS})
        return data

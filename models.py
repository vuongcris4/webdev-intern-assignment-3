"""Legacy compatibility exports for the Django-backed data layer."""

from scores.models import StudentScore
from scores.services import Subject, SubjectManager

__all__ = ["StudentScore", "Subject", "SubjectManager"]

from django.contrib import admin

from .models import StudentScore


@admin.register(StudentScore)
class StudentScoreAdmin(admin.ModelAdmin):
    list_display = ("sbd", "toan", "vat_li", "hoa_hoc", "ma_ngoai_ngu")
    search_fields = ("sbd",)

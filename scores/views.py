"""Page and API views for G-Scores."""
from django.http import JsonResponse
from django.shortcuts import render

from .services import SubjectManager


manager = SubjectManager()


def home(request):
    context = {"active": "search", **manager.dashboard_stats()}
    return render(request, "index.html", context)


def report_page(request):
    return render(request, "report.html", {"active": "report"})


def top10_page(request):
    return render(request, "top10.html", {"active": "top10"})


def api_lookup(request):
    sbd = request.GET.get("sbd", "").strip()
    error = validate_sbd(sbd)
    if error:
        return JsonResponse({"error": error}, status=400)

    student = manager.find_by_sbd(sbd)
    if not student:
        return JsonResponse({"error": f"Không tìm thấy thí sinh với SBD {sbd}."}, status=404)

    return JsonResponse(student.to_dict())


def api_report(request):
    return JsonResponse(manager.build_subject_report())


def api_top10(request):
    return JsonResponse(manager.top10_group_a(), safe=False)


def validate_sbd(sbd: str) -> str | None:
    if not sbd:
        return "Vui lòng nhập số báo danh."
    if not sbd.isdigit():
        return "Số báo danh chỉ được chứa chữ số."
    if len(sbd) > 20:
        return "Số báo danh không hợp lệ."
    return None

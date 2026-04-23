from flask import Flask, jsonify, render_template, request

from models import SubjectManager, db


def create_app() -> Flask:
    """Application factory for the G-Scores Flask app."""
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///g_scores.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)
    manager = SubjectManager()

    # ── Page Routes ──────────────────────────────────────────

    @app.get("/")
    def home():
        """Main search page."""
        return render_template("index.html")

    @app.get("/report")
    def report_page():
        """Score distribution report page."""
        return render_template("report.html")

    @app.get("/top10-group-a")
    def top10_page():
        """Top 10 Group A students page."""
        return render_template("top10.html")

    # ── API Routes ───────────────────────────────────────────

    @app.get("/api/lookup")
    def api_lookup():
        """API: Look up a student's scores by registration number (SBD).

        Query params:
            sbd (str): Student registration number (digits only).

        Returns:
            200: Student score data as JSON.
            400: Invalid or missing SBD.
            404: Student not found.
        """
        sbd = request.args.get("sbd", "").strip()

        # Validation
        if not sbd:
            return jsonify({"error": "Vui lòng nhập số báo danh."}), 400
        if not sbd.isdigit():
            return jsonify({"error": "Số báo danh chỉ được chứa chữ số."}), 400

        student = manager.find_by_sbd(sbd)
        if not student:
            return jsonify({"error": f"Không tìm thấy thí sinh với SBD {sbd}."}), 404

        return jsonify(student.to_dict())

    @app.get("/api/report")
    def api_report():
        """API: Get score distribution report for all subjects."""
        report = manager.build_subject_report()
        return jsonify(report)

    @app.get("/api/top10")
    def api_top10():
        """API: Get top 10 Group A students."""
        top10 = manager.top10_group_a()
        return jsonify(top10)

    # ── Legacy redirect (backward compat) ────────────────────

    @app.get("/lookup")
    def lookup_redirect():
        """Backward-compatible redirect for old lookup endpoint."""
        return api_lookup()

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)

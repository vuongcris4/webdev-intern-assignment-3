from flask import Flask, jsonify, render_template, request

from models import SubjectManager, db


def create_app() -> Flask:
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///g_scores.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)
    manager = SubjectManager()

    @app.get("/")
    def home():
        return render_template("index.html")

    @app.get("/lookup")
    def lookup_score():
        sbd = request.args.get("sbd", "").strip()
        if not sbd:
            return jsonify({"error": "Số báo danh là bắt buộc."}), 400
        if not sbd.isdigit():
            return jsonify({"error": "Số báo danh chỉ được chứa chữ số."}), 400

        student = manager.find_by_sbd(sbd)
        if not student:
            return jsonify({"error": f"Không tìm thấy thí sinh với SBD {sbd}."}), 404

        return jsonify(
            {
                "sbd": student.sbd,
                "toan": student.toan,
                "ngu_van": student.ngu_van,
                "ngoai_ngu": student.ngoai_ngu,
                "vat_li": student.vat_li,
                "hoa_hoc": student.hoa_hoc,
                "sinh_hoc": student.sinh_hoc,
                "lich_su": student.lich_su,
                "dia_li": student.dia_li,
                "gdcd": student.gdcd,
                "ma_ngoai_ngu": student.ma_ngoai_ngu,
            }
        )

    @app.get("/report")
    def report_page():
        report = manager.build_subject_report()
        return render_template("report.html", report=report)

    @app.get("/top10-group-a")
    def top10_page():
        top10 = manager.top10_group_a()
        return render_template("top10.html", top10=top10)

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)

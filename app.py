from flask import Flask, request, render_template
from utils import analyze_resume

app = Flask(__name__)


# =============================
# HOME PAGE
# =============================
@app.route("/")
def home():
    return render_template("index.html")


# =============================
# ANALYZE ROUTE
# =============================
@app.route("/analyze", methods=["POST"])
def analyze():
    try:
        file = request.files.get("resume")

        job_role = request.form.get("job_role", "")
        experience_level = request.form.get("experience_level", "")
        jd_text = request.form.get("job_description", "")
        jd_skills = request.form.get("jd_skills", "")

        jd_skills_list = [s.strip() for s in jd_skills.split(",") if s.strip()]

        result = analyze_resume(
            file,
            job_role,
            experience_level,
            jd_text,
            jd_skills_list
        )

        # =============================
        # SAFETY FALLBACK (FULL COVERAGE)
        # =============================
        if not isinstance(result, dict):
            result = {}

        result.setdefault("ats_score", 0)
        result.setdefault("semantic_similarity", 0)
        result.setdefault("skills_found", [])
        result.setdefault("matched_skills", [])
        result.setdefault("missing_skills", [])
        result.setdefault("experience_years", 0)
        result.setdefault("education", [])
        result.setdefault("feedback", {
            "strengths": [],
            "weaknesses": [],
            "improvements": [],
            "keyword_gaps": []
        })

        return render_template("result.html", data=result)

    except Exception as e:
        return render_template("result.html", data={
            "ats_score": 0,
            "semantic_similarity": 0,
            "skills_found": [],
            "matched_skills": [],
            "missing_skills": [],
            "experience_years": 0,
            "education": [],
            "feedback": {
                "strengths": [],
                "weaknesses": [],
                "improvements": [
                    "Fix backend error: " + str(e)
                ],
                "keyword_gaps": []
            }
        })


# =============================
# RUN APP
# =============================
if __name__ == "__main__":
    app.run(debug=True)
import pdfplumber
import re
import os
import json
from dotenv import load_dotenv
from openai import OpenAI

from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

from skills import SKILLS_DB, ROLE_SKILLS

# =============================
# ENV LOAD
# =============================
load_dotenv()

# =============================
# SEMANTIC MODEL (ONLY AI MATCHING)
# =============================
semantic_model = SentenceTransformer('all-MiniLM-L6-v2')


# =============================
# OPENAI CLIENT
# =============================
def get_client():
    api_key = os.getenv("OPENROUTER_API_KEY")

    if not api_key:
        raise ValueError("OPENROUTER_API_KEY not found in .env file")

    return OpenAI(
        api_key=api_key,
        base_url="https://openrouter.ai/api/v1"
    )


# =============================
# TEXT EXTRACTION
# =============================
def extract_text(file):
    text = ""
    with pdfplumber.open(file) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    return text.lower().strip()


# =============================
# SKILL EXTRACTION
# =============================
def extract_skills(text):
    found = set()

    for skill, variants in SKILLS_DB.items():
        for v in variants:
            if re.search(r'\b' + re.escape(v) + r'\b', text):
                found.add(skill)

    return list(found)


# =============================
# EXPERIENCE EXTRACTION
# =============================
def extract_experience(text):
    matches = re.findall(r'(\d+)\+?\s+(years|year)', text)
    if matches:
        return max([int(x[0]) for x in matches])
    return 0


# =============================
# EDUCATION EXTRACTION
# =============================
def extract_education(text):
    degrees = ["b.tech", "bachelor", "bsc", "m.tech", "master", "msc", "phd"]
    return list(set([d for d in degrees if d in text]))


# =============================
# ROLE SKILLS
# =============================
def get_role_skills(role):
    return ROLE_SKILLS.get(role.lower(), ["communication", "problem solving"])


# =============================
# SEMANTIC SIMILARITY (ONLY AI UNDERSTANDING)
# =============================
def compute_semantic_similarity(resume_text, jd_text):
    if not jd_text.strip() or not resume_text.strip():
        return 0

    embeddings = semantic_model.encode([resume_text, jd_text])

    score = cosine_similarity(
        [embeddings[0]],
        [embeddings[1]]
    )[0][0]

    return round(score * 100, 2)


# =============================
# SKILL MATCHING
# =============================
def match_skills(resume_skills, jd_skills):
    jd_skills = [s.lower().strip() for s in jd_skills if s.strip()]

    if not jd_skills:
        return 0, [], []

    matched = list(set(resume_skills) & set(jd_skills))
    missing = list(set(jd_skills) - set(resume_skills))

    score = (len(matched) / len(jd_skills)) * 100
    return round(score, 2), matched, missing


# =============================
# EXPERIENCE SCORE
# =============================
def experience_score(actual, level):
    expected_map = {
        "entry": 1,
        "moderate": 3,
        "experienced": 5
    }

    expected = expected_map.get(level, 3)

    if actual >= expected:
        return 100
    return round((actual / expected) * 100, 2)


# =============================
# ROLE WEIGHTS
# =============================
ROLE_WEIGHTS = {
    "data analyst": {
        "skills": 0.45,
        "similarity": 0.25,
        "experience": 0.20,
        "education": 0.10
    },
    "software developer": {
        "skills": 0.40,
        "similarity": 0.20,
        "experience": 0.30,
        "education": 0.10
    },
    "machine learning engineer": {
        "skills": 0.50,
        "similarity": 0.20,
        "experience": 0.20,
        "education": 0.10
    },
    "data scientist": {
        "skills": 0.50,
        "similarity": 0.20,
        "experience": 0.20,
        "education": 0.10
    }
}


# =============================
# FINAL ATS SCORE CALCULATION
# =============================
def calculate_ats(skill_score, similarity, exp_score, education_score, role):
    weights = ROLE_WEIGHTS.get(role.lower(), ROLE_WEIGHTS["data analyst"])

    score = (
        skill_score * weights["skills"] +
        similarity * weights["similarity"] +
        exp_score * weights["experience"] +
        education_score * weights["education"]
    )

    return round(score, 2)


# =============================
# LLM FEEDBACK ENGINE
# =============================
def generate_llm_feedback(resume_text, job_role, jd_text, missing_skills):

    prompt = f"""
You are an expert ATS resume reviewer.

Return STRICT JSON ONLY.

Schema:
{{
  "strengths": ["..."],
  "weaknesses": ["..."],
  "improvements": ["..."],
  "keyword_gaps": ["..."]
}}

Rules:
- Return all 4 keys
- No markdown, no explanation

Resume:
{resume_text}

Job Role:
{job_role}

Job Description:
{jd_text}

Missing Skills:
{missing_skills}
"""

    client = get_client()

    response = client.chat.completions.create(
        model="openai/gpt-4o-mini",
        messages=[
            {"role": "system", "content": "Return ONLY valid JSON."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.2,
        response_format={"type": "json_object"}
    )

    content = response.choices[0].message.content

    try:
        return json.loads(content)
    except json.JSONDecodeError:
        return {
            "strengths": [],
            "weaknesses": [],
            "improvements": [],
            "keyword_gaps": missing_skills
        }


# =============================
# MAIN ATS FUNCTION (SEMANTIC ONLY)
# =============================
def analyze_resume(file, job_role, experience_level, jd_text, jd_skills):

    text = extract_text(file)

    resume_skills = extract_skills(text)
    experience = extract_experience(text)
    education = extract_education(text)

    jd_provided = bool(jd_text.strip())

    if not jd_skills:
        jd_skills = get_role_skills(job_role)

    # =============================
    # SEMANTIC MATCH ONLY
    # =============================
    semantic_similarity = compute_semantic_similarity(text, jd_text) if jd_provided else 0

    skill_score, matched, missing = match_skills(resume_skills, jd_skills)

    exp_score = experience_score(experience, experience_level)
    education_score = 100 if education else 0

    ats_score = calculate_ats(
        skill_score,
        semantic_similarity,
        exp_score,
        education_score,
        job_role
    )

    feedback = generate_llm_feedback(
        resume_text=text,
        job_role=job_role,
        jd_text=jd_text,
        missing_skills=missing
    )

    return {
        "job_role": job_role,
        "experience_level": experience_level,

        "ats_score": ats_score,
        "semantic_similarity": semantic_similarity,

        "skills_found": resume_skills,
        "matched_skills": matched,
        "missing_skills": missing,

        "experience_years": experience,
        "education": education,

        "feedback": feedback
    }
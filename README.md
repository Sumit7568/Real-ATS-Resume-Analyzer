🚀 Real-ATS-Resume-Analyzer

An AI-powered Resume Analyzer that evaluates resumes based on ATS (Applicant Tracking System) standards, job roles, and skills matching. It provides actionable insights including ATS score, keyword gaps, strengths, weaknesses, and improvement suggestions.

📌 Features
📊 ATS Score Calculation (Role-based)
🔍 Skill Matching using TF-IDF + Regex
🤖 AI Feedback using LLM (OpenRouter)
📈 Semantic Similarity Analysis
📝 Resume Summary Generation
⚡ Keyword Gap Identification
🎯 Role-based Evaluation (Data Analyst, ML Engineer, etc.)
📌 Experience Level Weighting
Entry Level → 0.6
Moderate → 0.8
Experienced → 1.0
🧠 How It Works
Upload your resume (PDF)
Enter:
Job Role
Experience Level
(Optional) Job Description
System performs:
Skill extraction
Role-based matching
Semantic similarity scoring
AI-based evaluation
Outputs:
ATS Score
Strengths & Weaknesses
Improvement Suggestions
Missing Keywords
🏗️ Tech Stack
Backend: Flask
Frontend: HTML, CSS (Glass UI, Poppins)
AI/ML:
TF-IDF (Scikit-learn)
Cosine Similarity
Optional Sentence Transformers
LLM Integration: OpenRouter API
PDF Processing: pdfplumber
Database (optional): MySQL
📂 Project Structure
Real-ATS-Resume-Analyzer/
│
├── app.py
├── analyze_resume.py
├── templates/
│   └── index.html
├── static/
│   └── styles.css
├── utils/
│   ├── skills_db.py
│   └── role_skills.py
├── uploads/
├── .env
├── requirements.txt
└── README.md
⚙️ Installation
# Clone the repository
git clone https://github.com/Sumit7568/Real-ATS-Resume-Analyzer.git

# Navigate to project
cd Real-ATS-Resume-Analyzer

# Create virtual environment
python -m venv venv

# Activate environment
# Windows
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
🔑 Environment Variables

Create a .env file:

OPENROUTER_API_KEY=your_api_key_here
▶️ Run the Application
python app.py

Visit:
👉 http://127.0.0.1:5000

📊 Scoring Logic
Component	Weight
Skill Matching	30%
LLM Feedback	35%
Role-based ATS Score	40%
📸 UI Highlights
Modern Glass UI
Clean input layout (row-wise)
Interactive result dashboard
🚧 Future Improvements
✅ Add Resume Parsing with NLP
✅ Improve keyword extraction using embeddings
🔄 Add Resume Download with suggestions
🔄 Multi-role comparison
🔄 Dashboard analytics
🤝 Contributing

Contributions are welcome! Feel free to fork the repo and submit a PR.

📜 License

This project is open-source and available under the MIT License.

👨‍💻 Author

Sumit Raj
🔗 GitHub: https://github.com/Sumit7568

⭐ Support

If you like this project, give it a ⭐ on GitHub!

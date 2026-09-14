# AI-Powered Resume Analyzer 

https://repository-images.githubusercontent.com/1024648272/c2f784fc-d220-452c-a2b2-f1601abdd536

An ATS (Applicant Tracking System) style resume analyzer that compares a resume against a job description, scores the match, and highlights missing keywords/skills so you can improve your resume before applying.

> **Note:** This README assumes a Python + Streamlit + NLP stack (spaCy/NLTK, PyPDF2/python-docx). Update the sections below if your actual stack differs.

---

## Features

- 📄 Parse resumes in PDF and DOCX format
- 🧠 NLP-based keyword and skill extraction
- 🎯 ATS match score against a target job description
- 💡 Suggestions to improve keyword coverage
- 🖥️ Simple web interface (Streamlit)

---

## Installation & Setup

**[Install Python]** https://www.python.org/downloads/

**[Install pip]**

```bash
curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
```

```bash
python3 get-pip.py
```

Ensure pip is installed by running the following command

```bash
pip --version
```

If you have Python & pip installed then check their version in the terminal or command line tools

```bash
python3 --version
```

```bash
pip --version
```

---

## Clone the Repository

```bash
git clone https://github.com/<your-username>/Real-ATS-Resume-Analyzer.git
cd Real-ATS-Resume-Analyzer
```

---

## Install Dependencies

```bash
pip install -r requirements.txt
```

If you're using spaCy, download the language model:

```bash
python3 -m spacy download en_core_web_sm
```

---

## Usage

Run the app locally:

```bash
streamlit run app.py
```

Then open the local URL shown in your terminal (usually `http://localhost:8501`).

### Basic Workflow

1. Upload your resume (PDF/DOCX)
2. Paste the job description you're applying for
3. Click **Analyze**
4. View your ATS match score and keyword suggestions

---

## Project Structure

```
Real-ATS-Resume-Analyzer/
├── app.py                 # Main Streamlit app
├── resume_parser.py       # Resume text extraction logic
├── ats_scorer.py          # Matching & scoring logic
├── utils/                 # Helper functions
├── requirements.txt
└── README.md
```

---

## Tech Stack

- **Language:** Python
- **NLP:** spaCy / NLTK
- **Resume Parsing:** PyPDF2, python-docx
- **Interface:** Streamlit

---

## Contributing

Contributions are welcome! Please open an issue or submit a pull request.

1. Fork the repo
2. Create your feature branch (`git checkout -b feature/your-feature`)
3. Commit your changes
4. Push and open a PR

---

## License

This project is licensed under the MIT License.

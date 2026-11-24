# 💼 AI Career Copilot

> **Elevate your career search with an intelligent, SaaS-style resume analyzer, ATS optimizer, and interview preparation dashboard powered by Google Gemini and LangChain.**

AI Career Copilot is a state-of-the-art career preparation platform. It parses resumes, extracts candidate profiles, evaluates them against industry standard ATS parsers, matches them to target job descriptions, suggests quantitative bullet point improvements using the Google X-Y-Z formula, conducts interactive RAG-based conversations, and generates custom mock interview question banks with suggested answer frameworks.

---

## ✨ Key Features

AI Career Copilot is organized into an interactive console containing **six core modules**:

1. **📊 General Resume Assessment**
   * **Recruiter Rating**: Overall rating calculations calibrated against standard technical recruiter standards.
   * **SWOT Analysis**: Identifies clear *Strengths* and critical *Areas to Improve* in your CV.
   * **Detailed Appraisal**: Real-time qualitative assessment highlighting formatting, density, and clarity.

2. **🎯 ATS Score Analyzer & Keyword Match**
   * **Dual Inputs**: Paste raw job descriptions or upload PDF copies.
   * **Visual Scorecard**: Shows overall ATS score breakdowns, keyword density meters, and technical skill alignments.
   * **Missing Keywords & Skills**: Proactively identifies missing terminology, frameworks, and technical keywords.
   * **Plotly Visuals**: Beautiful horizontal charts illustrating matching metrics dynamically.

3. **🤝 Job Match Analysis**
   * **Hiring Verdict**: Clear recommendation flags (*Strongly Recommend*, *Recommend*, *Proceed with Caution*, or *Do Not Recommend*).
   * **Alignment Profiler**: Quantitative and qualitative breakdowns of role-candidate compatibility.
   * **Discrepancy Tracker**: Lists technical, educational, or experience gaps.

4. **✍️ Phrasing & Bullet Rewriter**
   * **Google X-Y-Z Formula**: Rewrites descriptive resume bullet points into high-impact, quantitative accomplishments (*"Accomplished [X] as measured by [Y], by doing [Z]"*).
   * **Before-and-After Comparisons**: Side-by-side original and improved phrasing cards.
   * **Recruiter Rationale**: Explains the exact reason and strategy behind the rewrite.

5. **🗣️ Interview Coach**
   * **Large Question Bank**: Automatically generates 20+ personalized mock questions based on your resume and target job details.
   * **Difficulty & Type Filters**: Filter questions by difficulty (*Easy*, *Medium*, *Hard*) and type (*Technical*, *HR*, *Behavioral*, *Project-Based*).
   * **Ideal Answer Frameworks**: Toggle expandable cards to view structured outline guides for constructing replies.

6. **🤖 Interactive Resume Chat (RAG)**
   * **RAG-Powered Chatbot**: Asks and answers questions directly based on the contents of your uploaded resume.
   * **Frosted-Glass UI**: Clean ChatGPT-style layout with alternating colors.
   * **Citations & Sources**: An expandable citations drawer displays the exact chunks of text retrieved from the CV for verification.

---

## 🛠️ Technology Stack

* **Frontend & Dashboard**: [Streamlit](https://streamlit.io/) (with custom CSS styling overrides)
* **LLM Orchestration**: [LangChain](https://www.langchain.com/) (LangChain-Community, LangChain-Core)
* **Vector Store**: [FAISS-CPU](https://github.com/facebookresearch/faiss) (In-memory similarity retrieval)
* **Generative AI Provider**: [Google GenAI (Gemini)](https://aistudio.google.com/)
* **Document Extraction**: [PyPDF](https://pypi.org/project/pypdf/)
* **Visualizations**: [Plotly Express](https://plotly.com/)
* **Environment Management**: [Python Dotenv](https://pypi.org/project/python-dotenv/)

---

## Live Demo

https://ai-career-copilot-manivarma-lokani.streamlit.app/

---

## 📂 Project Architecture

```directory
Career Copilot/
│
├── .env                  # API configuration keys (git-ignored)
├── .env.example          # Template for environment keys
├── .gitignore            # Git exclusion patterns
├── app.py                # Main Streamlit dashboard script
├── requirements.txt      # Python package dependencies
│
├── src/                  # Core application logic
│   ├── __init__.py
│   ├── config.py         # App configuration & CSS styling variables
│   ├── llm_service.py    # Google Gemini & Pydantic structured schemas
│   ├── parser.py         # PDF text parsing & profile schema generation
│   ├── rag_engine.py     # FAISS vector store creation & text chunking
│   ├── ui_components.py  # Frosted glass headers, cards, and UI components
│   └── verify_api.py     # Gemini API verification helper
│
└── tests/                # Automated testing suite
    ├── __pycache__/
    ├── test_analyses.py  # Tests general analysis & ATS modules
    ├── test_coaching.py  # Tests bullet rewriter & interview coach
    ├── test_parser.py    # Tests profile parsing
    └── test_rag.py       # Tests FAISS RAG chatbot query loop
```

---

## 🎨 Design System & Aesthetics

AI Career Copilot features a modern, premium **SaaS-inspired design system** implemented via custom CSS style overrides in `src/config.py`:

* **Typography**: Custom-imported Google Fonts featuring **Outfit** for headers/titles and **Plus Jakarta Sans** for body copy.
* **Glassmorphism**: Semi-transparent frosted-glass cards (`rgba(255, 255, 255, 0.75)`) with blurred backdrops (`backdrop-filter`) and violet-indigo borders on hover.
* **Vibrant Accents**: Tailored HSL theme colors: Violet (`#7C3AED`), Indigo (`#6366F1`), Teal (`#14B8A6`), Emerald (`#10B981`), and Pink (`#EC4899`).
* **Micro-Animations**: Hover card offsets, scaling badge chips, and smooth keyframe fade-in transitions.
* **Sticky Navigation**: A custom-designed sticky header navbar that locks to the top of the browser on scroll.

---

## 🚀 Installation & Setup

### Prerequisites

Make sure you have **Python 3.9+** installed on your system.

### 1. Clone & Navigate
Clone the repository to your local machine:
```bash
git clone https://github.com/yourusername/career-copilot.git
cd career-copilot
```

### 2. Create Virtual Environment
Create and activate a Python virtual environment:

**On Windows (Command Prompt/PowerShell):**
```powershell
python -m venv venv
venv\Scripts\activate
```

**On macOS / Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
Install all required packages from `requirements.txt`:
```bash
pip install -r requirements.txt
```

### 4. Setup Environment Variables
Duplicate the example env file and rename it to `.env`:
```bash
cp .env.example .env
```
Open the `.env` file and enter your Gemini API Key:
```env
GEMINI_API_KEY="your_actual_gemini_api_key_here"
```
> 💡 *Note: If you do not have a Gemini API key, you can get one for free at [Google AI Studio](https://aistudio.google.com/). You can also input the key directly inside the app's secure login panel.*

### 5. Run the Application
Start the Streamlit application server:
```bash
streamlit run app.py
```
A browser tab will open automatically at `http://localhost:8501`.

---

## 🧪 Running Automated Tests

The application contains comprehensive tests for parsing, embedding, LLM schemas, and RAG retrieval.

Make sure you have your `.env` configured, then execute any of the following script commands directly:

* **Test Profile Parsing**:
  ```bash
  python tests/test_parser.py
  ```
* **Test RAG Chunks & FAISS**:
  ```bash
  python tests/test_rag.py
  ```
* **Test Resume Improvements & Coaching**:
  ```bash
  python tests/test_coaching.py
  ```
* **Test ATS Matching & SWOT Appraisals**:
  ```bash
  python tests/test_analyses.py
  ```

---

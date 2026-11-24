import os
import sys
from dotenv import load_dotenv

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.llm_service import analyze_resume, analyze_ats, analyze_job_match

# Define mock resume text
MOCK_RESUME_TEXT = """
Jane Doe
Email: jane.doe@example.com | Phone: (123) 456-7890 | Website: github.com/janedoe

Professional Summary:
Enthusiastic and results-driven Software Engineer with 2+ years of experience building scalable web applications.

Skills:
- Languages: Python, JavaScript, HTML/CSS, SQL
- Frameworks: React, Flask, FastAPI, Tailwind CSS
- Tools/Tech: Git, Docker, AWS (S3, EC2), PostgreSQL

Experience:
Software Engineer | TechCorp Inc. | June 2022 - Present
- Developed a high-performance analytics dashboard using React and FastAPI, reducing query latency by 40%.
- Integrated AWS S3 for secure file uploads, handling over 10,000 files daily.
- Collaborated with UX designers to rewrite front-end modules, boosting accessibility compliance.

Projects:
AI Interview Assistant (GitHub) | Python, Flask, OpenAI API
- Developed an interactive chatbot that conducts mock interviews.
- Implemented real-time audio parsing and evaluation.
"""

# Define mock job description text
MOCK_JOB_DESCRIPTION = """
Position: Senior Python Web Developer
Requirements:
- 5+ years of experience in Python backend development.
- Deep expertise in FastAPI, Flask, and relational databases (PostgreSQL).
- Hands-on experience with AWS (S3, EC2, ECS, Lambda, IAM).
- Familiarity with frontend frameworks like React.
- Mandatory experience in Docker, CI/CD pipelines, and Kubernetes.
- Excellent communication and code optimization skills.
"""

def test_core_analyses():
    print("Loading environment variables...")
    load_dotenv()
    
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("[ERROR] GEMINI_API_KEY is not configured in .env file.")
        sys.exit(1)
        
    print("\n=======================================================")
    print("1. Testing Standalone Resume Quality Analysis...")
    print("=======================================================")
    try:
        resume_analysis = analyze_resume(MOCK_RESUME_TEXT, api_key)
        print(f"Overall Score: {resume_analysis.score}/100")
        print(f"Strengths: {', '.join(resume_analysis.strengths[:3])}")
        print(f"Weaknesses: {', '.join(resume_analysis.weaknesses[:3])}")
        print(f"Recruiter Feedback: {resume_analysis.recruiter_feedback[:150]}...")
        
        assert 0 <= resume_analysis.score <= 100
        assert len(resume_analysis.strengths) > 0
        print("[SUCCESS] Resume Quality Analysis Test Passed.")
    except Exception as e:
        print(f"[ERROR] Resume Quality Analysis failed: {str(e)}")
        sys.exit(1)

    print("\n=======================================================")
    print("2. Testing ATS Match Analysis...")
    print("=======================================================")
    try:
        ats_analysis = analyze_ats(MOCK_RESUME_TEXT, MOCK_JOB_DESCRIPTION, api_key)
        print(f"Overall ATS Match Score: {ats_analysis.score}/100")
        print(f"- Skill Match: {ats_analysis.skill_match_score}/100")
        print(f"- Keyword Match: {ats_analysis.keyword_match_score}/100")
        print(f"- Experience Relevance: {ats_analysis.experience_relevance_score}/100")
        print(f"- Education Relevance: {ats_analysis.education_relevance_score}/100")
        print(f"Missing Skills: {', '.join(ats_analysis.missing_skills)}")
        print(f"Missing Keywords: {', '.join(ats_analysis.missing_keywords)}")
        print(f"Suggestions: {ats_analysis.improvement_suggestions[0] if ats_analysis.improvement_suggestions else 'None'}")
        
        assert 0 <= ats_analysis.score <= 100
        assert 0 <= ats_analysis.skill_match_score <= 100
        assert "CI/CD" in ats_analysis.missing_skills or "Kubernetes" in ats_analysis.missing_skills or "ECS" in ats_analysis.missing_skills or len(ats_analysis.missing_skills) > 0
        print("[SUCCESS] ATS Match Analysis Test Passed.")
    except Exception as e:
        print(f"[ERROR] ATS Match Analysis failed: {str(e)}")
        sys.exit(1)

    print("\n=======================================================")
    print("3. Testing Job Compatibility Analysis...")
    print("=======================================================")
    try:
        job_match = analyze_job_match(MOCK_RESUME_TEXT, MOCK_JOB_DESCRIPTION, api_key)
        print(f"Match Percentage: {job_match.match_percentage}%")
        print(f"Skill Gaps: {', '.join(job_match.skill_gap_analysis[:4])}")
        print(f"Role Compatibility Summary: {job_match.role_compatibility[:150]}...")
        print(f"Hiring Recommendation: {job_match.hiring_recommendation}")
        
        assert 0 <= job_match.match_percentage <= 100
        assert len(job_match.skill_gap_analysis) > 0
        print("[SUCCESS] Job Compatibility Analysis Test Passed.")
    except Exception as e:
        print(f"[ERROR] Job Compatibility Analysis failed: {str(e)}")
        sys.exit(1)

    print("\n[SUCCESS] All Phase 4 core analysis verification tests completed successfully!")

if __name__ == "__main__":
    test_core_analyses()

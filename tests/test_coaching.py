import os
import sys
from dotenv import load_dotenv

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.llm_service import generate_improvements, generate_interview_questions

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

def test_coaching_features():
    print("Loading environment variables...")
    load_dotenv()
    
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("[ERROR] GEMINI_API_KEY is not configured in .env file.")
        sys.exit(1)
        
    print("\n=======================================================")
    print("1. Testing Resume Improvement Suggestions & Bullet Rewriter...")
    print("=======================================================")
    try:
        suggestions = generate_improvements(MOCK_RESUME_TEXT, api_key)
        print("Visual/Content improvements suggestions:")
        for idx, imp in enumerate(suggestions.improvements[:3]):
            print(f"- {imp}")
            
        print("\nSample Bullet Point Rewrites:")
        for rewrite in suggestions.bullet_rewrites:
            print(f"\n* Original: \"{rewrite.original}\"")
            print(f"  * Improved: \"{rewrite.improved}\"")
            print(f"  * Reasoning: {rewrite.reasoning}")
            
        assert len(suggestions.bullet_rewrites) >= 2
        print("\n[SUCCESS] Resume Improvements & Bullet Rewriter Test Passed.")
    except Exception as e:
        print(f"[ERROR] Resume Improvements failed: {str(e)}")
        sys.exit(1)

    print("\n=======================================================")
    print("2. Testing Interview Coach (At least 20 questions)...")
    print("=======================================================")
    try:
        coach_output = generate_interview_questions(MOCK_RESUME_TEXT, MOCK_JOB_DESCRIPTION, api_key)
        questions = coach_output.questions
        print(f"Total Questions Generated: {len(questions)}")
        
        # Display breakdown by difficulty and type
        difficulties = {}
        q_types = {}
        
        for q in questions:
            difficulties[q.difficulty] = difficulties.get(q.difficulty, 0) + 1
            q_types[q.question_type] = q_types.get(q.question_type, 0) + 1
            
        print("Breakdown by Difficulty:")
        for diff, count in difficulties.items():
            print(f"- {diff}: {count}")
            
        print("Breakdown by Type:")
        for q_type, count in q_types.items():
            print(f"- {q_type}: {count}")
            
        print("\nSample Questions generated:")
        for idx, q in enumerate(questions[:4]):
            print(f"\nQ{idx+1} [{q.question_type} - {q.difficulty}]: {q.question}")
            print(f"Ideal Answer Outline: {q.ideal_answer_outline}")
            
        # Assert at least 20 questions are generated as per product spec
        assert len(questions) >= 20
        print("\n[SUCCESS] Interview Coach Question Generator Test Passed.")
    except Exception as e:
        print(f"[ERROR] Interview Coach Question Generator failed: {str(e)}")
        sys.exit(1)

    print("\n[SUCCESS] All Phase 5 coaching and suggestion validation tests passed successfully!")

if __name__ == "__main__":
    test_coaching_features()

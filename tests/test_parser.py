import os
import sys
from dotenv import load_dotenv

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.parser import extract_profile_from_text

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

Education:
M.S. in Computer Science | Stanford University | 2022 - 2024
B.S. in Computer Science | State University | 2018 - 2022

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

def test_structured_parsing():
    print("Loading environment variables...")
    load_dotenv()
    
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("[ERROR] GEMINI_API_KEY is not configured in .env file.")
        sys.exit(1)
        
    print("Testing extract_profile_from_text with mock resume data...")
    try:
        profile = extract_profile_from_text(MOCK_RESUME_TEXT, api_key)
        
        print("\n=== Parsed Profile Output ===")
        print(f"Name: {profile.name}")
        print(f"Email: {profile.email}")
        print(f"Phone: {profile.phone}")
        print(f"Skills: {', '.join(profile.skills)}")
        
        print("\nEducation Details:")
        for edu in profile.education:
            print(f"- {edu.degree} at {edu.institution} ({edu.year})")
            
        print("\nWork Experience:")
        for exp in profile.experience:
            print(f"- {exp.role} at {exp.company} ({exp.duration})")
            for desc in exp.description:
                print(f"  * {desc}")
                
        print("\nProjects:")
        for proj in profile.projects:
            print(f"- {proj.title} (Tech: {', '.join(proj.technologies)})")
            print(f"  Description: {proj.description}")
            
        # Basic validation checks
        assert profile.name == "Jane Doe"
        assert profile.email == "jane.doe@example.com"
        assert len(profile.skills) > 0
        assert len(profile.education) > 0
        assert len(profile.experience) > 0
        assert len(profile.projects) > 0
        
        print("\n[SUCCESS] Parser test passed successfully!")
        
    except AssertionError:
        print("\n[ERROR] Parser returned output, but some assertion validations failed.")
        sys.exit(1)
    except Exception as e:
        print(f"\n[ERROR] Parser test failed with exception: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    test_structured_parsing()

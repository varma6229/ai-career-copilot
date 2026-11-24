import os
import sys
from dotenv import load_dotenv

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.rag_engine import create_vector_store, retrieve_context

# Reuse the mock resume text from the parser test
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

def test_rag_pipeline():
    print("Loading environment variables...")
    load_dotenv()
    
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("[ERROR] GEMINI_API_KEY is not configured in .env file.")
        sys.exit(1)
        
    print("Initializing FAISS vector store and generating embeddings...")
    try:
        vector_store = create_vector_store(MOCK_RESUME_TEXT, api_key)
        print("Vector store created successfully.")
        
        # Test Query 1
        query_1 = "FastAPI React query latency reduction"
        print(f"\nQuerying vector store for: '{query_1}'...")
        results_1 = retrieve_context(vector_store, query_1, k=1)
        
        print(f"Retrieved {len(results_1)} chunks.")
        for idx, doc in enumerate(results_1):
            print(f"\nMatch {idx+1} content:\n{doc.page_content}")
            print(f"Metadata: {doc.metadata}")
            
        assert len(results_1) > 0
        assert "FastAPI" in results_1[0].page_content
        assert "latency" in results_1[0].page_content
        
        # Test Query 2
        query_2 = "AI Interview Assistant chatbot"
        print(f"\nQuerying vector store for: '{query_2}'...")
        results_2 = retrieve_context(vector_store, query_2, k=1)
        
        print(f"Retrieved {len(results_2)} chunks.")
        for idx, doc in enumerate(results_2):
            print(f"\nMatch {idx+1} content:\n{doc.page_content}")
            
        assert len(results_2) > 0
        assert "Interview Assistant" in results_2[0].page_content
        
        print("\n[SUCCESS] RAG FAISS pipeline test completed and passed successfully!")
        
    except AssertionError:
        print("\n[ERROR] RAG query completed, but assertion validations failed.")
        sys.exit(1)
    except Exception as e:
        print(f"\n[ERROR] RAG pipeline test failed with exception: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    test_rag_pipeline()

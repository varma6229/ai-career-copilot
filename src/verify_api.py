import os
import sys
from dotenv import load_dotenv

# Add current directory to path to ensure modules can be imported
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def verify_gemini_connection():
    print("Loading environment variables...")
    load_dotenv()
    
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("[ERROR] GEMINI_API_KEY not found in environment or .env file.")
        print("Please copy .env.example to .env and insert your real Gemini API key.")
        return False
        
    print(f"API Key found (starts with: {api_key[:6]}...)")
    
    try:
        print("Importing langchain-google-genai...")
        from langchain_google_genai import ChatGoogleGenerativeAI
        
        print("Initializing ChatGoogleGenerativeAI with model 'gemini-3.8-flash'...")
        llm = ChatGoogleGenerativeAI(
            model="gemini-3.8-flash",
            google_api_key=api_key,
            temperature=0.0
        )
        
        print("Sending test prompt: 'Say hello and confirm you are online!'...")
        response = llm.invoke("Say hello and confirm you are online!")
        
        from src.llm_service import extract_text_from_content
        
        print("\n--- Model Response ---")
        print(extract_text_from_content(response.content))
        print("----------------------\n")
        print("[SUCCESS] Gemini 3.8 Flash is connected and responding correctly.")
        return True
        
    except Exception as e:
        print(f"[ERROR] Connection check failed with error: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    verify_gemini_connection()

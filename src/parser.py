import io
from typing import List, Optional
from pydantic import BaseModel, Field
from pypdf import PdfReader
from langchain_google_genai import ChatGoogleGenerativeAI

# =====================================================================
# Pydantic Schemas for Structured Profile Representation
# =====================================================================

class EducationItem(BaseModel):
    degree: str = Field(description="Degree title, major, or certification. E.g., B.S. in Computer Science")
    institution: str = Field(description="Name of university, college, or platform. E.g., Stanford University")
    year: Optional[str] = Field(default=None, description="Completion year or date range. E.g., 2024 or 2020 - 2024")

class ProjectItem(BaseModel):
    title: str = Field(description="Project title or name.")
    description: str = Field(description="Short summary of contributions, impact, or goals achieved.")
    technologies: List[str] = Field(default=[], description="Key technical stack and libraries used in this project.")

class ExperienceItem(BaseModel):
    role: str = Field(description="Job title/position. E.g., Senior Software Engineer")
    company: str = Field(description="Company or organization name.")
    duration: Optional[str] = Field(default=None, description="Start to end date. E.g., June 2022 - Present")
    description: List[str] = Field(default=[], description="List of contributions, bullet points, or achievements.")

class ResumeProfile(BaseModel):
    name: str = Field(description="Full name of the candidate.")
    email: Optional[str] = Field(default=None, description="Email address extracted from resume.")
    phone: Optional[str] = Field(default=None, description="Contact phone number extracted from resume.")
    skills: List[str] = Field(default=[], description="Core technical and soft skills listed or inferred.")
    education: List[EducationItem] = Field(default=[], description="List of educational qualifications.")
    projects: List[ProjectItem] = Field(default=[], description="List of relevant side-projects or work projects.")
    experience: List[ExperienceItem] = Field(default=[], description="Professional work history list.")

# =====================================================================
# Extraction & Parsing Logic
# =====================================================================

def extract_text_from_pdf(pdf_source) -> str:
    """
    Extracts plain text from a PDF file. 
    Accepts both file paths (str) and file-like objects (e.g., io.BytesIO from Streamlit file uploader).
    """
    try:
        if isinstance(pdf_source, str):
            reader = PdfReader(pdf_source)
        else:
            # Handle BytesIO and custom file-like objects
            reader = PdfReader(pdf_source)
            
        text = ""
        for i, page in enumerate(reader.pages):
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
        return text.strip()
    except Exception as e:
        raise ValueError(f"Failed to parse PDF file: {str(e)}")

def extract_profile_from_text(text: str, api_key: str) -> ResumeProfile:
    """
    Leverages Gemini 3.8 Flash to convert raw resume text into structured Pydantic schema.
    """
    try:
        # Initialize Gemini via LangChain
        llm = ChatGoogleGenerativeAI(
            model="gemini-3.8-flash",
            google_api_key=api_key,
            temperature=0.0
        )
        
        # Configure model with structured output mapping to ResumeProfile Pydantic class
        structured_llm = llm.with_structured_output(ResumeProfile)
        
        prompt = f"""
        You are an expert AI recruiter and parsing agent.
        Analyze the raw resume text below and extract candidate information into the requested JSON schema.
        Ensure you capture all skills, education instances, projects, and work experience details accurately.
        If a field (like email or phone) is missing, return null.
        
        Resume text:
        ---
        {text}
        ---
        """
        
        # Invoke and return schema instance
        profile = structured_llm.invoke(prompt)
        return profile
    except Exception as e:
        raise RuntimeError(f"Error parsing profile metadata using Gemini: {str(e)}")

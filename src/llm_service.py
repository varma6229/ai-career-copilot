from typing import List, Optional, Any, Union
from pydantic import BaseModel, Field
from langchain_google_genai import ChatGoogleGenerativeAI

def extract_text_from_content(content: Any) -> str:
    """
    Extracts clean plain text from LLM response content, stripping away
    metadata blocks, dictionaries, extras, and cryptographic signatures.
    Handles plain strings, lists of blocks/dicts, and stringified representations.
    """
    if isinstance(content, str):
        trimmed = content.strip()
        if trimmed.startswith("[{") and ("'text':" in trimmed or '"text":' in trimmed):
            import ast
            try:
                parsed = ast.literal_eval(trimmed)
                if isinstance(parsed, list):
                    return extract_text_from_content(parsed)
            except Exception:
                pass
        return content

    if isinstance(content, list):
        text_parts = []
        for part in content:
            if isinstance(part, str):
                text_parts.append(part)
            elif isinstance(part, dict):
                if "text" in part:
                    text_parts.append(str(part["text"]))
                elif "content" in part:
                    text_parts.append(str(part["content"]))
            elif hasattr(part, "text"):
                text_parts.append(str(getattr(part, "text", "")))
        if text_parts:
            return "".join(text_parts).strip()

    if isinstance(content, dict):
        if "text" in content:
            return str(content["text"]).strip()
        if "content" in content:
            return str(content["content"]).strip()

    return str(content)

# =====================================================================
# Pydantic Schemas for Structured Outputs
# =====================================================================

class ResumeAnalysis(BaseModel):
    score: int = Field(description="Overall resume score from 0 to 100 based on structure, content, impact, and standard recruiter metrics.")
    strengths: List[str] = Field(description="Key strengths noticed in the resume.")
    weaknesses: List[str] = Field(description="Key weaknesses or areas of concern in the resume.")
    recruiter_feedback: str = Field(description="Detailed recruiter-style feedback and overall appraisal of the resume.")
    reasoning: str = Field(description="Detailed breakdown of how the score was calculated.")

class ATSAnalysis(BaseModel):
    score: int = Field(description="Overall ATS match score from 0 to 100 indicating overall compatibility with the job description.")
    skill_match_score: int = Field(description="Score from 0 to 100 representing how well the technical and soft skills match the job description.")
    keyword_match_score: int = Field(description="Score from 0 to 100 representing keyword density matching the job description.")
    experience_relevance_score: int = Field(description="Score from 0 to 100 representing how relevant the work history is to the job description.")
    education_relevance_score: int = Field(description="Score from 0 to 100 representing education relevance to the job description.")
    missing_skills: List[str] = Field(description="Key skills mentioned or implied in the job description that are missing from the resume.")
    missing_keywords: List[str] = Field(description="Important industry keywords, tools, or terminology missing from the resume.")
    improvement_suggestions: List[str] = Field(description="Actionable steps to optimize the resume specifically for this job description.")

class JobMatchAnalysis(BaseModel):
    match_percentage: int = Field(description="Overall match percentage from 0 to 100 between candidate profile and job description.")
    skill_gap_analysis: List[str] = Field(description="Detailed analysis of specific technical or soft skill gaps identified.")
    role_compatibility: str = Field(description="Explanation of why the candidate is or isn't compatible with this role.")
    hiring_recommendation: str = Field(description="Overall hiring recommendation (e.g., Strongly Recommend, Recommend, Proceed with Caution, Do Not Recommend).")

class BulletPointRewrite(BaseModel):
    original: str = Field(description="The original bullet point from the resume.")
    improved: str = Field(description="The rewritten bullet point containing stronger action verbs, metrics, and quantitative impact.")
    reasoning: str = Field(description="Explanation of why this rewrite is better and what ATS rule it satisfies.")

class ResumeImprovement(BaseModel):
    strengths: List[str] = Field(description="Core strengths of the resume formatting or phrasing.")
    weaknesses: List[str] = Field(description="Core weaknesses of the resume formatting or phrasing.")
    improvements: List[str] = Field(description="Actionable improvement suggestions.")
    bullet_rewrites: List[BulletPointRewrite] = Field(description="Examples of original bullet points rewritten for high-impact metrics and phrasing.")

class InterviewQuestion(BaseModel):
    question: str = Field(description="The interview question.")
    difficulty: str = Field(description="Difficulty level: Easy, Medium, or Hard.")
    question_type: str = Field(description="Type: Technical, HR, Behavioral, or Project-Based.")
    ideal_answer_outline: str = Field(description="Key points that should be in the candidate's answer.")

class InterviewPrep(BaseModel):
    questions: List[InterviewQuestion] = Field(description="List of at least 20 high-quality interview questions covering all categories and difficulties.")

# =====================================================================
# Service Functions calling Gemini 3.8 Flash
# =====================================================================

def analyze_resume(resume_text: str, api_key: str) -> ResumeAnalysis:
    """
    Performs standalone resume quality assessment using Gemini.
    """
    llm = ChatGoogleGenerativeAI(
        model="gemini-3.8-flash",
        google_api_key=api_key,
        temperature=0.2
    )
    structured_llm = llm.with_structured_output(ResumeAnalysis)
    
    prompt = f"""
    You are an expert recruiter and resume consultant.
    Analyze the following resume text and assess its quality. Generate an overall score (0-100), identify key strengths and weaknesses, and provide detailed feedback and reasoning.
    
    Resume Text:
    ---
    {resume_text}
    ---
    """
    return structured_llm.invoke(prompt)

def analyze_ats(resume_text: str, job_description: str, api_key: str) -> ATSAnalysis:
    """
    Analyzes how well the resume matches a target job description for ATS systems.
    """
    llm = ChatGoogleGenerativeAI(
        model="gemini-3.8-flash",
        google_api_key=api_key,
        temperature=0.1
    )
    structured_llm = llm.with_structured_output(ATSAnalysis)
    
    prompt = f"""
    You are an ATS (Applicant Tracking System) optimization expert.
    Compare the following resume text against the job description text.
    Perform a granular score breakdown for Skill Match, Keyword Match, Experience Relevance, and Education Relevance.
    List missing skills, missing keywords, and detailed improvement suggestions.
    
    Resume Text:
    ---
    {resume_text}
    ---
    
    Job Description Text:
    ---
    {job_description}
    ---
    """
    return structured_llm.invoke(prompt)

def analyze_job_match(resume_text: str, job_description: str, api_key: str) -> JobMatchAnalysis:
    """
    Analyzes candidate-role compatibility and skill gaps.
    """
    llm = ChatGoogleGenerativeAI(
        model="gemini-3.8-flash",
        google_api_key=api_key,
        temperature=0.2
    )
    structured_llm = llm.with_structured_output(JobMatchAnalysis)
    
    prompt = f"""
    You are an experienced hiring manager.
    Analyze the compatibility between the candidate's resume and the job description.
    Provide a match percentage, detail the specific skill gaps, assess role compatibility, and make a clear hiring recommendation.
    
    Resume Text:
    ---
    {resume_text}
    ---
    
    Job Description Text:
    ---
    {job_description}
    ---
    """
    return structured_llm.invoke(prompt)

def generate_improvements(resume_text: str, api_key: str) -> ResumeImprovement:
    """
    Suggests resume improvements and rewrites original bullet points into high-impact metrics-driven points.
    """
    llm = ChatGoogleGenerativeAI(
        model="gemini-3.8-flash",
        google_api_key=api_key,
        temperature=0.3
    )
    structured_llm = llm.with_structured_output(ResumeImprovement)
    
    prompt = f"""
    You are an expert resume writer and technical recruiter.
    Analyze the resume text and suggest specific visual/content improvements.
    Identify weak bullet points (e.g., those without quantitative metrics or impact, or starting with weak verbs) and rewrite them to follow the X-Y-Z formula: "Accomplished [X] as measured by [Y], by doing [Z]".
    Provide at least 3 bullet point rewrite examples.
    
    Resume Text:
    ---
    {resume_text}
    ---
    """
    return structured_llm.invoke(prompt)

def generate_interview_questions(resume_text: str, job_description: str, api_key: str) -> InterviewPrep:
    """
    Generates at least 20 structured interview questions based on the candidate's background and target job description.
    """
    llm = ChatGoogleGenerativeAI(
        model="gemini-3.8-flash",
        google_api_key=api_key,
        temperature=0.4
    )
    structured_llm = llm.with_structured_output(InterviewPrep)
    
    prompt = f"""
    You are a technical interviewer and HR coach.
    Based on the candidate's resume and target job description, generate a list of at least 20 high-quality interview questions.
    The list must include:
    - Difficulty levels: Easy, Medium, and Hard.
    - Question types: Technical, HR, Behavioral, and Project-Based.
    For each question, provide a structured outline of the ideal answer.
    
    Resume Text:
    ---
    {resume_text}
    ---
    
    Job Description Text:
    ---
    {job_description}
    ---
    """
    return structured_llm.invoke(prompt)

def answer_query_with_context(query: str, context_docs: list, api_key: str) -> str:
    """
    Answers a candidate's or recruiter's query using only the retrieved resume content chunks.
    """
    try:
        llm = ChatGoogleGenerativeAI(
            model="gemini-3.8-flash",
            google_api_key=api_key,
            temperature=0.2
        )
        
        # Combine the content of the top-matching documents
        context_text = "\n\n".join([
            f"--- Chunk {i+1} ---\n{doc.page_content}"
            for i, doc in enumerate(context_docs)
        ])
        
        prompt = f"""
        You are an intelligent Career Copilot chatbot. Your job is to answer questions about the candidate's resume based ONLY on the provided context chunks.
        
        If the answer cannot be directly found or reasonably inferred from the provided context, clearly reply: "I cannot find this information in the resume context."
        Do NOT assume or generate facts outside the context. Keep your response professional, helpful, and concise.
        
        Context Chunks:
        {context_text}
        
        Question: {query}
        
        Answer:
        """
        response = llm.invoke(prompt)
        return extract_text_from_content(response.content)
    except Exception as e:
        return f"Error executing RAG query: {str(e)}"

import os
import time
import streamlit as st
import plotly.express as px
from dotenv import load_dotenv

# Import project modules
from src.config import (
    APP_TITLE, 
    APP_ICON, 
    PRIMARY_PURPLE, 
    PRIMARY_INDIGO, 
    PRIMARY_LIGHT,
    ACCENT_TEAL, 
    ACCENT_EMERALD, 
    ACCENT_PINK
)
from src.parser import extract_text_from_pdf, extract_profile_from_text
from src.rag_engine import create_vector_store, retrieve_context
from src.llm_service import (
    analyze_resume,
    analyze_ats,
    analyze_job_match,
    generate_improvements,
    generate_interview_questions,
    answer_query_with_context,
    extract_text_from_content
)
from src.ui_components import (
    inject_custom_css,
    render_sticky_header,
    render_hero_section,
    render_profile_card,
    render_feature_grid,
    render_score_card,
    render_loader_card
)

# Load environment variables
load_dotenv()

# Streamlit page configuration
st.set_page_config(
    page_title=APP_TITLE,
    page_icon=APP_ICON,
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Inject modern style overrides (Jakarta Font, Glassmorphic cards, CSS Header position adjustments)
inject_custom_css()

# Render Sticky Frosted Glass Header
render_sticky_header()

# Retrieve API key
api_key = st.secrets.get(
    "GEMINI_API_KEY",
    os.getenv("GEMINI_API_KEY")
)
if not api_key:
    st.error(
        "GEMINI_API_KEY is not configured. "
        "Please add it in Streamlit Cloud Secrets."
    )
    st.stop()

# =====================================================================
# State Management Initialization
# =====================================================================

if "resume_text" not in st.session_state:
    st.session_state.resume_text = None
if "profile" not in st.session_state:
    st.session_state.profile = None
if "vector_store" not in st.session_state:
    st.session_state.vector_store = None
if "chat_history" not in st.session_state:
    st.session_state.chat_history = [
        {
            "role": "assistant", 
            "content": "Hi! I am your Career Copilot chatbot. I can search, summarize, or query details about your resume. Ask me anything!", 
            "sources": []
        }
    ]

# Navigation State
if "active_section" not in st.session_state:
    st.session_state.active_section = "Resume Analysis"

# Job description states
if "job_desc_text" not in st.session_state:
    st.session_state.job_desc_text = ""
if "job_desc_pdf_name" not in st.session_state:
    st.session_state.job_desc_pdf_name = ""

# Analysis caches to prevent repeat queries on navigation clicks
if "resume_analysis" not in st.session_state:
    st.session_state.resume_analysis = None
if "ats_analysis" not in st.session_state:
    st.session_state.ats_analysis = None
if "job_match_analysis" not in st.session_state:
    st.session_state.job_match_analysis = None
if "resume_improvements" not in st.session_state:
    st.session_state.resume_improvements = None
if "interview_coach" not in st.session_state:
    st.session_state.interview_coach = None

# Helper to clear state on new upload
def reset_resume_state():
    st.session_state.resume_text = None
    st.session_state.profile = None
    st.session_state.vector_store = None
    st.session_state.resume_analysis = None
    st.session_state.ats_analysis = None
    st.session_state.job_match_analysis = None
    st.session_state.resume_improvements = None
    st.session_state.interview_coach = None
    st.session_state.chat_history = [
        {
            "role": "assistant", 
            "content": "Hi! I am your Career Copilot chatbot. I can search, summarize, or query details about your resume. Ask me anything!", 
            "sources": []
        }
    ]

# =====================================================================
# STEP 1: Upload Resume Flow (Always Visible at Top)
# =====================================================================

# Active landing page class for scroll lock if no resume parsed yet
if st.session_state.resume_text is None:
    st.markdown("<div class='landing-page-active'></div>", unsafe_allow_html=True)

# Render Hero section at the top
render_hero_section()

with st.container(border=True):
    uploaded_file = st.file_uploader(
        "Upload PDF", 
        type=["pdf"], 
        label_visibility="collapsed",
        key="resume_uploader_selector"
    )

    st.markdown(
        """
        <div style="text-align: center; margin-top: 15px;">
            <div style="font-size: 24px; color: #6B7280; margin-bottom: 5px;">↑</div>
            <div style="font-weight: 700; font-size: 16px; color: #111827;">Upload your resume (PDF)</div>
            <div style="font-size: 12px; color: #6B7280; margin-top: 3px;">Drag &amp; drop or click to browse</div>
        </div>
        """,
        unsafe_allow_html=True
    )

# If user clears the uploader
if uploaded_file is None and st.session_state.resume_text is not None:
    reset_resume_state()
    st.rerun()
# If user uploads a new/different file
elif uploaded_file is not None and st.session_state.resume_text is not None:
    if "current_file_name" not in st.session_state:
        st.session_state.current_file_name = uploaded_file.name
    elif st.session_state.current_file_name != uploaded_file.name:
        reset_resume_state()
        st.session_state.current_file_name = uploaded_file.name
        st.rerun()

# Render Preview & Run Button if uploaded but not analyzed yet
if uploaded_file is not None and st.session_state.resume_text is None:
    size_kb = len(uploaded_file.getvalue()) / 1024
    st.markdown(
        f"""
        <div class="file-preview-card" style="margin-top: 0; margin-bottom: 15px;">
            <div style="font-size: 30px;">📄</div>
            <div style="flex-grow: 1;">
                <div style="font-weight: 700; color: #111827; font-size: 14px;">{uploaded_file.name}</div>
                <div style="font-size: 11px; color: #6B7280; font-weight: 600; margin-top: 2px;">{size_kb:.1f} KB</div>
            </div>
            <div style="background: rgba(16, 185, 129, 0.1); color: {ACCENT_EMERALD}; padding: 4px 10px; border-radius: 20px; font-size: 11px; font-weight: 700;">Ready</div>
        </div>
        """, 
        unsafe_allow_html=True
    )
    
    st.markdown("<div style='margin-top: 15px;'></div>", unsafe_allow_html=True)
    if st.button("✨ Analyze Resume", key="btn_run_parser_flow", use_container_width=True):
        loader_placeholder = st.empty()
        progress_bar = st.progress(0)
        
        try:
            loader_placeholder.empty()
            with loader_placeholder:
                render_loader_card("🔍 Reading Resume")
            progress_bar.progress(20)
            time.sleep(0.5)
            
            raw_text = extract_text_from_pdf(uploaded_file)
            st.session_state.resume_text = raw_text
            
            loader_placeholder.empty()
            with loader_placeholder:
                render_loader_card("📑 Extracting Content")
            progress_bar.progress(40)
            time.sleep(0.5)
            
            loader_placeholder.empty()
            with loader_placeholder:
                render_loader_card("🧠 Understanding Profile")
            progress_bar.progress(60)
            profile = extract_profile_from_text(raw_text, api_key)
            st.session_state.profile = profile
            
            loader_placeholder.empty()
            with loader_placeholder:
                render_loader_card("📊 Building Analysis")
            progress_bar.progress(80)
            vector_store = create_vector_store(raw_text, api_key)
            st.session_state.vector_store = vector_store
            time.sleep(0.5)
            
            loader_placeholder.empty()
            with loader_placeholder:
                render_loader_card("✨ Preparing Insights")
            progress_bar.progress(100)
            st.session_state.current_file_name = uploaded_file.name
            time.sleep(0.5)
            
            loader_placeholder.empty()
            progress_bar.empty()
            st.rerun()
            
        except Exception as e:
            loader_placeholder.empty()
            progress_bar.empty()
            st.error(f"❌ Parsing failed: {str(e)}")
            reset_resume_state()

# =====================================================================
# DASHBOARD SCREEN: Interactive Feature Console (After upload)
# =====================================================================

if st.session_state.resume_text is not None:
    # STEP 2: Profile details card
    st.markdown("<div style='font-size: 12px; color: #6B7280; font-weight: 700; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 8px; margin-top: 25px;'>STEP 2 &mdash;</div>", unsafe_allow_html=True)
    render_profile_card(st.session_state.profile)
    
    # STEP 3: Clickable 3x2 Feature Navigation Console
    render_feature_grid()
    
    st.markdown("<div style='font-size: 12px; color: #6B7280; font-weight: 700; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 8px; margin-top: 25px;'>STEP 4 &mdash;</div>", unsafe_allow_html=True)
    
    active_section = st.session_state.get("active_section", "Resume Analysis")
    
    st.markdown("<div style='margin-bottom: 15px;'></div>", unsafe_allow_html=True)
    
    # -----------------------------------------------------------------
    # Tab 1: Resume Quality Analysis
    # -----------------------------------------------------------------
    if active_section == "Resume Analysis":
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        st.markdown("<h3>📊 General Resume Assessment</h3>", unsafe_allow_html=True)
        st.markdown("Review the overall quality, structure, and readability rating of your resume.")
        
        if st.session_state.resume_analysis is None:
            if st.button("⚡ Run Quality Review", key="btn_run_quality_section"):
                with st.spinner("Analyzing resume content..."):
                    try:
                        st.session_state.resume_analysis = analyze_resume(
                            st.session_state.resume_text, 
                            api_key
                        )
                        st.rerun()
                    except Exception as e:
                        st.error(f"Analysis failed: {str(e)}")
                        
        if st.session_state.resume_analysis is not None:
            analysis = st.session_state.resume_analysis
            
            # Display premium scorecard
            render_score_card(
                score=analysis.score, 
                title="Overall Resume Score", 
                subtitle="Calculated against standard tech recruiter templates"
            )
            
            col_str, col_weak = st.columns(2)
            with col_str:
                st.markdown("##### 🟢 Strengths")
                for s in analysis.strengths:
                    st.markdown(f"- {s}")
            with col_weak:
                st.markdown("##### 🔴 Areas to Improve")
                for w in analysis.weaknesses:
                    st.markdown(f"- {w}")
            
            st.markdown("<div style='margin-bottom: 20px;'></div>", unsafe_allow_html=True)
            st.markdown("##### 📝 Detailed Recruiter Appraisal")
            st.info(analysis.recruiter_feedback)
            
            st.markdown("##### 🔍 Score Calculation & Reasoning Breakdown")
            st.write(analysis.reasoning)
            
        st.markdown("</div>", unsafe_allow_html=True)

    # -----------------------------------------------------------------
    # Tab 2: ATS Score Analyzer
    # -----------------------------------------------------------------
    elif active_section == "ATS Score Analyzer":
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        st.markdown("<h3>🎯 ATS Match Score & Keyword Analyzer</h3>", unsafe_allow_html=True)
        st.caption(
            "⚠️ ATS scores are AI-generated estimates based on the job description "
            "and resume content. They do not represent scores from actual ATS systems."
        )
        st.markdown("Analyze how well your resume matches target qualifications using keywords and relevance calculations.")
        
        # Dual input methods: upload PDF or paste text
        st.markdown("##### Choose Job Description Input Method:")
        jd_input_method = st.radio(
            "Input Method", 
            ["Paste JD Text", "Upload JD PDF"], 
            horizontal=True,
            label_visibility="collapsed",
            key="ats_jd_method_selector"
        )
        
        # Extract Job Description text based on selected method
        if jd_input_method == "Upload JD PDF":
            uploaded_jd = st.file_uploader(
                "Upload Job Description PDF", 
                type=["pdf"], 
                key="jd_pdf_uploader"
            )
            if uploaded_jd is not None:
                # Cache parsed text if name changed
                if st.session_state.job_desc_pdf_name != uploaded_jd.name:
                    with st.spinner("Extracting Job Description text..."):
                        try:
                            st.session_state.job_desc_text = extract_text_from_pdf(uploaded_jd)
                            st.session_state.job_desc_pdf_name = uploaded_jd.name
                            st.success(f"Successfully loaded {uploaded_jd.name}")
                        except Exception as e:
                            st.error(f"Failed to parse PDF: {str(e)}")
        else:
            # Pasting JD
            st.session_state.job_desc_text = st.text_area(
                "Paste Job Description Text",
                value=st.session_state.job_desc_text,
                placeholder="Paste the target job description requirements here...",
                height=200,
                key="jd_paste_area"
            )
            
        # Prioritize showing the job description preview
        if st.session_state.job_desc_text.strip():
            with st.expander("📄 View Job Description Preview"):
                st.text(st.session_state.job_desc_text[:1200] + "..." if len(st.session_state.job_desc_text) > 1200 else st.session_state.job_desc_text)
        
        st.markdown("<div style='margin-top: 15px;'></div>", unsafe_allow_html=True)
        
        if st.button("🎯 Analyze ATS Compatibility", key="btn_run_ats_section"):
            if not st.session_state.job_desc_text.strip():
                st.warning("Please provide a Job Description (either paste or upload PDF) first.")
            else:
                with st.spinner("Comparing credentials against requirements..."):
                    try:
                        st.session_state.ats_analysis = analyze_ats(
                            st.session_state.resume_text,
                            st.session_state.job_desc_text,
                            api_key
                        )
                        st.rerun()
                    except Exception as e:
                        st.error(f"ATS analysis failed: {str(e)}")
                        
        if st.session_state.ats_analysis is not None:
            ats = st.session_state.ats_analysis
            
            # Step 4 Two-column layout matching wireframe
            st.markdown(
                f"""
                <div class="ats-results-grid">
                    <div class="ats-score-col-left">
                        <div class="ats-score-num">{ats.score}<span class="ats-score-denom">/100</span></div>
                        <div class="ats-score-label">Overall score</div>
                    </div>
                    <div class="ats-score-col-right">
                        <div class="ats-progress-label">Skill match</div>
                        <div class="ats-progress-track">
                            <div class="ats-progress-bar skill-match-bar" style="width: {ats.skill_match_score}%;"></div>
                        </div>
                        <div class="ats-progress-label">Keyword match</div>
                        <div class="ats-progress-track">
                            <div class="ats-progress-bar keyword-match-bar" style="width: {ats.keyword_match_score}%;"></div>
                        </div>
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )
            
            # Modern sub-score cards (Experience and Education)
            st.markdown("<div style='margin-top: 15px;'></div>", unsafe_allow_html=True)
            col_sc3, col_sc4 = st.columns(2)
            with col_sc3:
                st.markdown(f"<div style='text-align:center; padding:10px; background:rgba(20,184,166,0.05); border-radius:10px; border-top:3px solid {ACCENT_TEAL};'><div style='font-size:20px; font-weight:800; color:#14B8A6;'>{ats.experience_relevance_score}%</div><div style='font-size:10px; color:#6B7280; font-weight:700; text-transform:uppercase;'>Experience Relevance</div></div>", unsafe_allow_html=True)
            with col_sc4:
                st.markdown(f"<div style='text-align:center; padding:10px; background:rgba(236,72,153,0.05); border-radius:10px; border-top:3px solid {ACCENT_PINK};'><div style='font-size:20px; font-weight:800; color:#EC4899;'>{ats.education_relevance_score}%</div><div style='font-size:10px; color:#6B7280; font-weight:700; text-transform:uppercase;'>Education Relevance</div></div>", unsafe_allow_html=True)
            
            # Plotly breakdown chart
            st.markdown("<div style='margin-top: 25px;'></div>", unsafe_allow_html=True)
            fig = px.bar(
                x=[ats.skill_match_score, ats.keyword_match_score, ats.experience_relevance_score, ats.education_relevance_score],
                y=["Skills Fit", "Keyword Density", "Experience Rel.", "Education Rel."],
                orientation='h',
                labels={"x": "Score (%)", "y": "Category"},
                range_x=[0, 100],
                color=[ats.skill_match_score, ats.keyword_match_score, ats.experience_relevance_score, ats.education_relevance_score],
                color_continuous_scale="Purples"
            )
            fig.update_layout(
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                margin=dict(l=10, r=10, t=10, b=10),
                height=220,
                coloraxis_showscale=False
            )
            st.plotly_chart(fig, use_container_width=True)
            
            # Gaps displays
            col_m_skills, col_m_kws = st.columns(2)
            with col_m_skills:
                st.markdown("##### 🛠️ Identified Missing Skills:")
                if ats.missing_skills:
                    for skill in ats.missing_skills:
                        st.markdown(f'<span class="saas-badge" style="background-color:#FEE2E2; color:#B91C1C; border-color:rgba(185,28,28,0.1);">{skill}</span>', unsafe_allow_html=True)
                else:
                    st.success("No missing technical skills identified!")
            with col_m_kws:
                st.markdown("##### 🏷️ Missing Keywords:")
                if ats.missing_keywords:
                    for kw in ats.missing_keywords:
                        st.markdown(f'<span class="saas-badge" style="background-color:#FEF3C7; color:#B45309; border-color:rgba(180,83,9,0.1);">{kw}</span>', unsafe_allow_html=True)
                else:
                    st.success("No missing keyword flags found!")
            
            st.markdown("<div style='margin-bottom: 20px;'></div>", unsafe_allow_html=True)
            st.markdown("##### 💡 ATS Suggestions & Actions")
            for idx, sugg in enumerate(ats.improvement_suggestions):
                st.markdown(f"**{idx+1}.** {sugg}")
                
        st.markdown("</div>", unsafe_allow_html=True)

    # -----------------------------------------------------------------
    # Tab 3: Job Match Analysis
    # -----------------------------------------------------------------
    elif active_section == "Job Match Analysis":
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        st.markdown("<h3>💼 Role Compatibility & Hiring Recommendation</h3>", unsafe_allow_html=True)
        st.markdown("Analyze candidate compatibility and gap metrics relative to target job post specifications.")
        
        # Share Job Description
        st.session_state.job_desc_text = st.text_area(
            "Target Job Description", 
            value=st.session_state.job_desc_text,
            placeholder="Paste target job qualifications here...",
            height=200,
            key="match_jd_paste"
        )
        
        if st.button("🤝 Run Compatibility Review", key="btn_run_match_section"):
            if not st.session_state.job_desc_text.strip():
                st.warning("Please provide a Job Description first.")
            else:
                with st.spinner("Reviewing candidate compatibility..."):
                    try:
                        st.session_state.job_match_analysis = analyze_job_match(
                            st.session_state.resume_text,
                            st.session_state.job_desc_text,
                            api_key
                        )
                        st.rerun()
                    except Exception as e:
                        st.error(f"Compatibility review failed: {str(e)}")
                        
        if st.session_state.job_match_analysis is not None:
            match = st.session_state.job_match_analysis
            
            render_score_card(
                score=match.match_percentage,
                title="Job Compatibility Match",
                subtitle="Overall candidate-role alignment profile fit"
            )
            
            rec_color = {
                "Strongly Recommend": ACCENT_EMERALD,
                "Recommend": "#059669",
                "Proceed with Caution": "#F59E0B",
                "Do Not Recommend": "#EF4444"
            }.get(match.hiring_recommendation, PRIMARY_PURPLE)
            
            st.markdown(
                f"""
                <div style="background-color: rgba(255,255,255,0.8); border-radius: 12px; padding: 20px; border-left: 6px solid {rec_color}; box-shadow: 0 4px 15px rgba(0,0,0,0.01); margin-bottom: 25px;">
                    <div style="font-size: 11px; text-transform: uppercase; font-weight: 700; color: #6B7280; letter-spacing: 0.5px;">Recruiter Verdict</div>
                    <div style="font-size: 20px; font-weight: 800; color: {rec_color}; margin-top: 4px;">{match.hiring_recommendation}</div>
                </div>
                """,
                unsafe_allow_html=True
            )
            
            st.markdown("##### 📝 Role Compatibility Review")
            st.write(match.role_compatibility)
            
            st.markdown("##### ⚠️ Key Gaps & Discrepancies")
            for gap in match.skill_gap_analysis:
                st.markdown(f"- {gap}")
                
        st.markdown("</div>", unsafe_allow_html=True)

    # -----------------------------------------------------------------
    # Tab 4: Resume Improvement Suggestions
    # -----------------------------------------------------------------
    elif active_section == "Resume Improvement":
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        st.markdown("<h3>✨ Phrasing & Bullet Rewriter</h3>", unsafe_allow_html=True)
        st.markdown("Enhance descriptions using quantitative recruiter achievements (Google X-Y-Z formula).")
        
        if st.session_state.resume_improvements is None:
            if st.button("💡 Generate Suggestions & Bullet Rewrites", key="btn_run_imp_section"):
                with st.spinner("Analyzing phrasing metrics..."):
                    try:
                        st.session_state.resume_improvements = generate_improvements(
                            st.session_state.resume_text, 
                            api_key
                        )
                        st.rerun()
                    except Exception as e:
                        st.error(f"Rewriter failed: {str(e)}")
                        
        if st.session_state.resume_improvements is not None:
            imp = st.session_state.resume_improvements
            
            col_str, col_weak = st.columns(2)
            with col_str:
                st.markdown("##### 🟢 Formatting Strengths")
                for s in imp.strengths:
                    st.markdown(f"- {s}")
            with col_weak:
                st.markdown("##### 🔴 Formatting Weaknesses")
                for w in imp.weaknesses:
                    st.markdown(f"- {w}")
            
            st.markdown("<div style='margin-bottom: 25px;'></div>", unsafe_allow_html=True)
            st.markdown("##### ✍️ Metric-Driven Bullet Rewrites (Google X-Y-Z Formula)")
            
            for index, rewrite in enumerate(imp.bullet_rewrites):
                st.markdown(
                    f"""
                    <div style="background: rgba(255,255,255,0.7); border: 1px solid rgba(229, 231, 235, 0.6); border-radius: 12px; padding: 18px; margin-bottom: 15px; box-shadow: 0 4px 15px rgba(0,0,0,0.01);">
                        <div style="font-weight: 800; color: #6B7280; font-size: 11px; text-transform: uppercase; margin-bottom: 8px; letter-spacing: 0.5px;">Example {index+1}</div>
                        <div style="margin-bottom: 8px; font-size: 13.5px; line-height: 1.4;">
                            <span style="color: #EF4444; font-weight: 700;">Original:</span> <span style="color: #4B5563; font-style: italic;">"{rewrite.original}"</span>
                        </div>
                        <div style="margin-bottom: 10px; font-size: 13.5px; line-height: 1.4;">
                            <span style="color: #10B981; font-weight: 700;">Improved:</span> <span style="color: #111827; font-weight: 600;">"{rewrite.improved}"</span>
                        </div>
                        <div style="font-size: 12px; border-top: 1px dashed rgba(229, 231, 235, 0.8); padding-top: 8px; color: #6B7280; font-weight: 500;">
                            💡 <strong>Recruiter Rationale:</strong> {rewrite.reasoning}
                        </div>
                    </div>
                    """, 
                    unsafe_allow_html=True
                )
                
        st.markdown("</div>", unsafe_allow_html=True)

    # -----------------------------------------------------------------
    # Tab 5: Interview Coach
    # -----------------------------------------------------------------
    elif active_section == "Interview Coach":
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        st.markdown("<h3>🎤 Interview Question Guide</h3>", unsafe_allow_html=True)
        st.markdown("Generate custom mock questions categorized by difficulty and type based on job details.")
        
        # Share Job Description
        st.session_state.job_desc_text = st.text_area(
            "Target Job Description", 
            value=st.session_state.job_desc_text,
            placeholder="Paste target job qualifications here...",
            height=200,
            key="coach_jd_paste"
        )
        
        if st.button("🗣️ Generate Interview Bank", key="btn_run_coach_section"):
            if not st.session_state.job_desc_text.strip():
                st.warning("Please paste target job qualifications first.")
            else:
                with st.spinner("Generating 20+ interview questions..."):
                    try:
                        st.session_state.interview_coach = generate_interview_questions(
                            st.session_state.resume_text,
                            st.session_state.job_desc_text,
                            api_key
                        )
                        st.rerun()
                    except Exception as e:
                        st.error(f"Failed to generate questions: {str(e)}")
                        
        if st.session_state.interview_coach is not None:
            questions = st.session_state.interview_coach.questions
            
            # Show question stats breakdown
            difficulties = {"Easy": 0, "Medium": 0, "Hard": 0}
            types = {"Technical": 0, "HR": 0, "Behavioral": 0, "Project-Based": 0}
            
            for q in questions:
                if q.difficulty in difficulties:
                    difficulties[q.difficulty] += 1
                if q.question_type in types:
                    types[q.question_type] += 1
                    
            st.markdown("##### 📊 Prep Statistics")
            col_stat1, col_stat2 = st.columns(2)
            with col_stat1:
                st.markdown("**Difficulty Distribution:**")
                st.write(f"🟢 Easy: {difficulties['Easy']} | 🟡 Medium: {difficulties['Medium']} | 🔴 Hard: {difficulties['Hard']}")
            with col_stat2:
                st.markdown("**Category Distribution:**")
                st.write(f"💻 Tech: {types['Technical']} | 🤝 Behavior: {types['Behavioral']} | 📁 Project: {types['Project-Based']} | 👤 HR: {types['HR']}")
                
            st.markdown("<hr style='margin: 15px 0; border: 0.5px solid #F3F4F6;'>", unsafe_allow_html=True)
            st.markdown("##### 📁 Interactive Question Bank")
            
            # Render filters
            col_filt1, col_filt2 = st.columns(2)
            with col_filt1:
                selected_difficulty = st.selectbox("Filter by Difficulty", ["All", "Easy", "Medium", "Hard"])
            with col_filt2:
                selected_type = st.selectbox("Filter by Question Type", ["All", "Technical", "HR", "Behavioral", "Project-Based"])
            
            filtered_questions = [
                q for q in questions
                if (selected_difficulty == "All" or q.difficulty == selected_difficulty) and
                   (selected_type == "All" or q.question_type == selected_type)
            ]
            
            if not filtered_questions:
                st.info("No questions match the selected parameters.")
            else:
                for idx, q in enumerate(filtered_questions):
                    diff_color = {
                        "Easy": "background-color: #E8F5E9; color: #2E7D32;",
                        "Medium": "background-color: #FFFDE7; color: #F57F17;",
                        "Hard": "background-color: #FFEBEE; color: #C62828;"
                    }.get(q.difficulty, "background-color: #F3F4F6; color: #4B5563;")
                    
                    header_label = f"Q{idx+1} [{q.question_type} - {q.difficulty}]: {q.question}"
                    
                    with st.expander(header_label):
                        st.markdown(
                            f"""
                            <div style="padding: 5px 0;">
                                <div style="margin-bottom: 12px;">
                                    <span style="{diff_color} padding: 4px 10px; border-radius: 6px; font-size: 11px; font-weight: 700; margin-right: 10px;">{q.difficulty}</span>
                                    <span style="background-color: #FAF5FF; color: #7C3AED; padding: 4px 10px; border-radius: 6px; font-size: 11px; font-weight: 700;">{q.question_type}</span>
                                </div>
                                <div style="font-weight: 700; color: #374151; font-size: 13px; margin-bottom: 5px;">Copyable Question Text:</div>
                            </div>
                            """,
                            unsafe_allow_html=True
                        )
                        
                        # Copy button code wrapper
                        st.code(q.question, language="text")
                        
                        st.markdown(
                            f"""
                            <div style="margin-top: 10px;">
                                <div style="font-weight: 700; color: #374151; font-size: 13px; margin-bottom: 5px;">Ideal Answer Framework:</div>
                                <div style="color: #4B5563; font-size: 13.5px; background: white; padding: 15px; border-radius: 8px; border: 1px solid rgba(229, 231, 235, 0.6); border-left: 4px solid #7C3AED;">
                                    {q.ideal_answer_outline}
                                </div>
                            </div>
                            """,
                            unsafe_allow_html=True
                        )
                        
        st.markdown("</div>", unsafe_allow_html=True)

    # -----------------------------------------------------------------
    # Tab 6: Resume Chat (RAG)
    # -----------------------------------------------------------------
    elif active_section == "Resume Chat":
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        st.markdown("<h3>🤖 Interactive Resume RAG Chat</h3>", unsafe_allow_html=True)
        st.markdown("Query credentials or summarize items. The AI assistant extracts matches and presents citations.")
        
        # Render scrollable ChatGPT style chat logs
        chat_box = st.container(height=350)
        with chat_box:
            for msg in st.session_state.chat_history:
                bubble_class = "chat-bubble-user" if msg["role"] == "user" else "chat-bubble-assistant"
                clean_content = extract_text_from_content(msg["content"])
                
                # Check for RAG sources
                st.markdown(f'<div class="{bubble_class}">{clean_content}</div>', unsafe_allow_html=True)
                
                # Render context drawers underneath assistant messages
                if msg["role"] == "assistant" and msg["sources"]:
                    with st.expander("🔍 View Context Sources & Citations"):
                        for i, doc in enumerate(msg["sources"]):
                            st.markdown(f"**Source {i+1}** (Start Index: {doc['metadata'].get('start_index', 'N/A')}):")
                            st.code(doc["page_content"], language="text")
                            
        # Input prompt box
        if prompt := st.chat_input("Ask a question about your resume..."):
            with chat_box:
                st.markdown(f'<div class="chat-bubble-user">{prompt}</div>', unsafe_allow_html=True)
            
            # Record user prompt
            st.session_state.chat_history.append({
                "role": "user", 
                "content": prompt, 
                "sources": []
            })
            
            # Trigger chatbot search
            with st.spinner("🤖 AI is reading chunks..."):
                try:
                    # Retrieve context
                    context = retrieve_context(
                        st.session_state.vector_store,
                        prompt,
                        k=3
                    )
                    # Query Gemini
                    response = answer_query_with_context(
                        prompt,
                        context,
                        api_key
                    )
                    
                    doc_serial = [
                        {"page_content": d.page_content, "metadata": d.metadata}
                        for d in context
                    ]
                    
                    clean_response = extract_text_from_content(response)
                    
                    with chat_box:
                        st.markdown(f'<div class="chat-bubble-assistant">{clean_response}</div>', unsafe_allow_html=True)
                        with st.expander("🔍 View Context Sources & Citations"):
                            for i, doc in enumerate(doc_serial):
                                st.markdown(f"**Source {i+1}** (Start Index: {doc['metadata'].get('start_index', 'N/A')}):")
                                st.code(doc["page_content"], language="text")
                                
                    # Record assistant response
                    st.session_state.chat_history.append({
                        "role": "assistant",
                        "content": clean_response,
                        "sources": doc_serial
                    })
                except Exception as e:
                    st.error(f"Error answering query: {str(e)}")
                    
        st.markdown("</div>", unsafe_allow_html=True)

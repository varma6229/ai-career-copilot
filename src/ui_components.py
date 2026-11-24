import streamlit as st
from src.config import PRIMARY_PURPLE, PRIMARY_INDIGO, ACCENT_TEAL, ACCENT_EMERALD, ACCENT_PINK

def inject_custom_css():
    """
    Injects custom typography, responsive gradients, and visual card classes.
    """
    from src.config import CUSTOM_CSS
    st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

def render_sticky_header():
    """
    Renders a sticky frosted-glass navigation header at the top of the page.
    Attaches a JS listener to parent/local window to toggle scroll classes.
    """
    st.markdown(
        """
        <div class="sticky-header">
            <div class="sticky-title">AI Career Copilot</div>
            <div class="sticky-subtitle">AI-Powered Resume Intelligence Platform</div>
        </div>
        
        <script>
            // We run a scroll listener on parent/self window to toggle header opacity on scroll
            const scrollTarget = window.parent || window;
            const handleScroll = () => {
                const doc = window.parent ? window.parent.document : document;
                const header = doc.querySelector('.sticky-header');
                const scrollY = window.parent ? window.parent.scrollY : window.scrollY;
                if (header) {
                    if (scrollY > 50) {
                        header.classList.add('scrolled');
                    } else {
                        header.classList.remove('scrolled');
                    }
                }
            };
            scrollTarget.addEventListener('scroll', handleScroll);
            // Run initial check
            handleScroll();
        </script>
        """,
        unsafe_allow_html=True
    )

def render_hero_section():
    """
    Renders a premium visual landing hero section.
    """
    st.markdown(
        f"""
        <div style="text-align: center; padding: 15px 0 10px 0; animation: fadeIn 0.6s ease-out;">
            <span style="background: rgba(124, 58, 237, 0.1); color: {PRIMARY_PURPLE}; padding: 6px 16px; border-radius: 20px; font-size: 11px; font-weight: 700; text-transform: uppercase; letter-spacing: 1px; display: inline-block; margin-bottom: 12px;">
                ✨ RAG Platform
            </span>
            <h1 style="font-size: 46px; font-weight: 800; background: linear-gradient(135deg, #7C3AED 0%, #6366F1 50%, #EC4899 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin-bottom: 10px; letter-spacing: -1.5px; line-height: 1.15;">
                AI Career Copilot
            </h1>
            <p style="font-size: 14.5px; color: #4B5563; max-width: 600px; margin: 0 auto; line-height: 1.4; font-weight: 500;">
                Analyze resumes, improve ATS compatibility, compare job descriptions, generate interview questions, and chat with your profile using custom RAG.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )
    st.markdown("<div style='margin-bottom: 15px;'></div>", unsafe_allow_html=True)

def render_profile_card(profile_data):
    """
    Renders the parsed candidate profile data in a sleek glassmorphic card matching the wireframe.
    """
    # Extract initials
    parts = profile_data.name.strip().split()
    if len(parts) >= 2:
        initials = (parts[0][0] + parts[-1][0]).upper()
    elif parts:
        initials = parts[0][:2].upper()
    else:
        initials = "JD"
        
    email_phone = f"{profile_data.email or ''}"
    if profile_data.email and profile_data.phone:
        email_phone += f" &middot; {profile_data.phone}"
    elif profile_data.phone:
        email_phone = profile_data.phone
        
    if not email_phone:
        email_phone = "No contact details provided"

    skills_badges = "".join([
        f'<span class="profile-skill-chip">{s}</span>'
        for s in profile_data.skills[:8] # Show top skills as chips
    ])
    
    st.markdown(
        f"""
        <div class="profile-card">
            <div class="profile-header">
                <div class="profile-avatar">{initials}</div>
                <div class="profile-info">
                    <div class="profile-name">{profile_data.name}</div>
                    <div class="profile-contact">{email_phone}</div>
                </div>
            </div>
            <div class="profile-skills-row">
                {skills_badges}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

def render_feature_grid():
    """
    Renders a 3x2 responsive card grid matching the wireframe features.
    Makes the entire card clickable by overlaying an invisible Streamlit button.
    """
    active = st.session_state.get("active_section", "Resume Analysis")
    
    st.markdown("<div style='font-size: 12px; color: #6B7280; font-weight: 700; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 12px; margin-top: 15px;'>STEP 3 &mdash; FEATURE CARDS (UNLOCKED AFTER UPLOAD)</div>", unsafe_allow_html=True)
    
    # Grid items data based on wireframe
    features = [
        {"icon": "📄", "title": "Resume analysis", "desc": "Score &middot; strengths &middot; feedback", "section": "Resume Analysis"},
        {"icon": "🎯", "title": "ATS score", "desc": "Keyword + skill match", "section": "ATS Score Analyzer"},
        {"icon": "🔗", "title": "Job match", "desc": "Compatibility &middot; skill gaps", "section": "Job Match Analysis"},
        {"icon": "✨", "title": "Improvements", "desc": "Rewritten bullets", "section": "Resume Improvement"},
        {"icon": "🎙️", "title": "Interview coach", "desc": "20+ questions by tier", "section": "Interview Coach"},
        {"icon": "💬", "title": "Resume chat (RAG)", "desc": "Chat with your resume", "section": "Resume Chat"}
    ]
    
    # Render grid columns in Streamlit
    row1_cols = st.columns(3)
    row2_cols = st.columns(3)
    
    for idx, feat in enumerate(features):
        col = row1_cols[idx] if idx < 3 else row2_cols[idx - 3]
        
        with col:
            is_active = active == feat["section"]
            active_class = "active" if is_active else ""
            
            # Wrap the card inside the clickable-card-container
            st.markdown(
                f"""
                <div class="clickable-card-container">
                    <div class="feature-nav-card {active_class}">
                        <div style="font-size: 24px; margin-bottom: 6px;">{feat["icon"]}</div>
                        <div style="font-weight: 600; font-size: 13px; color: #111827;">{feat["title"]}</div>
                        <div style="font-size: 11px; color: #6B7280; margin-top: 4px; text-align: center; line-height: 1.3;">{feat["desc"]}</div>
                    </div>
                """,
                unsafe_allow_html=True
            )
            
            # Invisible Streamlit button overlayed on top
            if st.button("", key=f"btn_nav_overlay_{feat['section'].lower().replace(' ', '_')}", use_container_width=True):
                st.session_state.active_section = feat["section"]
                st.rerun()
                
            st.markdown("</div>", unsafe_allow_html=True)

def render_score_card(score: int, title: str, subtitle: str):
    """
    Renders an eye-catching scorecard component with gradient borders and responsive text.
    """
    score_color = ACCENT_EMERALD if score >= 80 else (PRIMARY_INDIGO if score >= 60 else "#EF4444")
    
    st.markdown(
        f"""
        <div class="glass-card" style="text-align: center; border-top: 4px solid {score_color} !important; animation: fadeIn 0.4s ease-out;">
            <div style="font-size: 46px; font-weight: 800; color: {score_color}; font-family: 'Outfit', sans-serif;">{score}%</div>
            <div style="font-size: 14px; font-weight: 700; color: #374151; text-transform: uppercase; letter-spacing: 0.5px; margin-top: 5px;">{title}</div>
            <div style="font-size: 12px; color: #6B7280; margin-top: 4px;">{subtitle}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

def render_loader_card(stage_title: str):
    """
    Renders an animated loading card with frosted borders and clean typography.
    """
    st.markdown(
        f"""
        <div class="glass-card" style="text-align: center; border-top: 4px solid #7C3AED !important; animation: fadeIn 0.3s ease-out;">
            <div style="font-size: 44px; display: inline-block; margin-bottom: 15px; animation: pulse 1.5s infinite;">🧠</div>
            <div style="font-family: 'Outfit', sans-serif; font-size: 18px; font-weight: 800; color: #7C3AED;">{stage_title}</div>
            <div style="font-size: 12px; color: #6B7280; margin-top: 5px; font-weight: 500;">
                Processing credentials & synthesizing RAG vector index...
            </div>
        </div>
        <style>
            @keyframes pulse {{
                0% {{ transform: scale(1); opacity: 0.8; }}
                50% {{ transform: scale(1.1); opacity: 1; }}
                100% {{ transform: scale(1); opacity: 0.8; }}
            }}
        </style>
        """,
        unsafe_allow_html=True
    )

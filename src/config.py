import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# App general settings
APP_TITLE = "AI Career Copilot"
APP_ICON = "💼"

# Gemini Model settings
DEFAULT_MODEL = "gemini-3.8-flash"
EMBEDDING_MODEL = "models/gemini-embedding-001"

# Design Styling Colors
PRIMARY_PURPLE = "#7C3AED"     # Violet
PRIMARY_LIGHT = "#8B5CF6"      # Light Purple
PRIMARY_INDIGO = "#6366F1"     # Indigo
ACCENT_TEAL = "#14B8A6"        # Teal
ACCENT_EMERALD = "#10B981"     # Emerald
ACCENT_PINK = "#EC4899"        # Pink

# Custom CSS to force a stunning SaaS look and feel
CUSTOM_CSS = """
<style>
    /* Google Fonts import */
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap');

    /* Global page styling overrides */
    .stApp {
        background: linear-gradient(135deg, #F5F3FF 0%, #EEF2FF 50%, #ECFEFF 100%) !important;
        color: #1F2937 !important;
        font-family: 'Plus Jakarta Sans', sans-serif !important;
    }

    /* Enforce zero scrollbar on the landing page state */
    .stApp:has(.landing-page-active) {
        overflow: hidden !important;
        height: 100vh !important;
    }
    .stApp:has(.landing-page-active) .main .block-container {
        padding-top: 30px !important;
        height: 100vh !important;
        display: flex;
        flex-direction: column;
        justify-content: center;
    }
    
    /* Hide default Streamlit header and adjust main spacing */
    [data-testid="stHeader"] {
        display: none !important;
    }
    
    .main .block-container {
        padding-top: 85px !important;
        padding-bottom: 50px !important;
        max-width: 850px !important;
    }
    
    /* Custom Sticky frosted navbar */
    .sticky-header {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        background: rgba(255, 255, 255, 0.7);
        backdrop-filter: blur(16px) saturate(180%);
        -webkit-backdrop-filter: blur(16px) saturate(180%);
        z-index: 999999;
        border-bottom: 1px solid rgba(255, 255, 255, 0.4);
        box-shadow: 0 4px 30px rgba(0, 0, 0, 0.03);
        padding: 12px 30px;
        display: flex;
        align-items: center;
        justify-content: center;
        flex-direction: column;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        opacity: 0;
        transform: translateY(-100%);
        pointer-events: none;
    }
    .sticky-header.scrolled {
        opacity: 1;
        transform: translateY(0);
        pointer-events: auto;
    }
    
    .sticky-title {
        font-family: 'Outfit', sans-serif !important;
        font-size: 22px;
        font-weight: 800;
        background: linear-gradient(135deg, #7C3AED 0%, #6366F1 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 0;
        letter-spacing: -0.5px;
    }
    
    .sticky-subtitle {
        font-size: 11px;
        color: #6B7280;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 1.5px;
        margin-top: 2px;
    }

    /* Typography styles */
    h1, h2, h3, h4, h5, h6 {
        font-family: 'Outfit', sans-serif !important;
        color: #111827 !important;
        font-weight: 700 !important;
    }

    /* Glassmorphic Dashboard Cards */
    .glass-card {
        background: rgba(255, 255, 255, 0.75) !important;
        border: 1px solid rgba(255, 255, 255, 0.45) !important;
        border-radius: 16px !important;
        padding: 24px !important;
        box-shadow: 0 10px 30px rgba(31, 38, 135, 0.03) !important;
        backdrop-filter: blur(8px) !important;
        -webkit-backdrop-filter: blur(8px) !important;
        margin-bottom: 20px !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        animation: fadeIn 0.5s ease-out;
    }
    
    .glass-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 15px 35px rgba(124, 58, 237, 0.07) !important;
        border-color: rgba(124, 58, 237, 0.2) !important;
    }
    
    /* Hero Badge / Header stats container */
    .hero-stat-card {
        background: rgba(255, 255, 255, 0.6);
        border: 1px solid rgba(255, 255, 255, 0.4);
        border-radius: 12px;
        padding: 12px;
        text-align: center;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.01);
    }
    
    /* Multi-step upload files card */
    .file-preview-card {
        background: rgba(255, 255, 255, 0.85);
        border: 1px dashed #8B5CF6;
        border-radius: 12px;
        padding: 16px 20px;
        margin: 15px 0;
        display: flex;
        align-items: center;
        gap: 15px;
        box-shadow: 0 8px 24px rgba(124, 58, 237, 0.03);
    }
    
    /* Feature Navigation Card Buttons */
    .feature-nav-card {
        background: rgba(255, 255, 255, 0.8);
        border: 1px solid rgba(255, 255, 255, 0.5);
        border-radius: 16px;
        padding: 20px;
        text-align: center;
        cursor: pointer;
        transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
        box-shadow: 0 8px 25px rgba(31, 38, 135, 0.02);
        display: flex;
        flex-direction: column;
        align-items: center;
        height: 100%;
        min-height: 130px;
        justify-content: center;
    }
    
    .feature-nav-card:hover {
        transform: translateY(-4px);
        background: #FFFFFF;
        box-shadow: 0 12px 30px rgba(124, 58, 237, 0.12);
        border-color: rgba(124, 58, 237, 0.35);
    }
    
    .feature-nav-card.active {
        background: linear-gradient(135deg, #FAF5FF 0%, #EEF2FF 100%);
        border: 2px solid #7C3AED !important;
        box-shadow: 0 12px 35px rgba(124, 58, 237, 0.15);
    }

    /* Custom clickable card container overlay */
    .clickable-card-container {
        position: relative;
        width: 100%;
        height: 100%;
    }
    .clickable-card-container div[data-testid="element-container"] {
        position: absolute !important;
        top: 0 !important;
        left: 0 !important;
        width: 100% !important;
        height: 100% !important;
        margin: 0 !important;
        padding: 0 !important;
        z-index: 10 !important;
    }
    .clickable-card-container button {
        position: absolute !important;
        top: 0 !important;
        left: 0 !important;
        width: 100% !important;
        height: 100% !important;
        opacity: 0 !important;
        cursor: pointer !important;
        margin: 0 !important;
        padding: 0 !important;
        border: none !important;
        background: transparent !important;
    }

    /* Custom metrics badges */
    .saas-badge {
        background-color: #FAF5FF;
        color: #7C3AED;
        padding: 6px 14px;
        margin: 4px;
        border-radius: 20px;
        font-size: 13px;
        font-weight: 600;
        display: inline-block;
        border: 1px solid rgba(124, 58, 237, 0.15);
        transition: all 0.2s ease;
    }
    
    .saas-badge:hover {
        background-color: #7C3AED;
        color: #FFFFFF;
        transform: scale(1.05);
    }
    
    /* Custom buttons styling override */
    .stButton>button {
        background: linear-gradient(135deg, #7C3AED 0%, #6366F1 100%) !important;
        color: white !important;
        border-radius: 10px !important;
        border: none !important;
        padding: 12px 30px !important;
        font-weight: 700 !important;
        font-family: 'Outfit', sans-serif !important;
        letter-spacing: 0.5px !important;
        box-shadow: 0 8px 20px rgba(124, 58, 237, 0.2) !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        width: 100%;
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 12px 25px rgba(124, 58, 237, 0.35) !important;
        background: linear-gradient(135deg, #8B5CF6 0%, #7C3AED 100%) !important;
    }
    
    .stButton>button:active {
        transform: translateY(1px);
    }

    /* Override secondary buttons to be purple-indigo gradient instead of black */
    button[data-testid="baseButton-secondary"] {
        background: linear-gradient(135deg, #7C3AED 0%, #6366F1 100%) !important;
        color: white !important;
        border-radius: 8px !important;
        border: none !important;
        padding: 8px 20px !important;
        font-weight: 600 !important;
        font-family: 'Outfit', sans-serif !important;
        box-shadow: 0 4px 12px rgba(124, 58, 237, 0.15) !important;
        transition: all 0.3s ease !important;
    }
    button[data-testid="baseButton-secondary"]:hover {
        background: linear-gradient(135deg, #8B5CF6 0%, #7C3AED 100%) !important;
        transform: translateY(-1px) !important;
        box-shadow: 0 6px 15px rgba(124, 58, 237, 0.25) !important;
        color: white !important;
    }

    /* Style the vertical block wrapper that has a file uploader widget inside it to look like the glass card */
    div[data-testid="stVerticalBlockBorderWrapper"]:has([data-testid="stFileUploader"]) {
        background: rgba(255, 255, 255, 0.75) !important;
        border: 1px solid rgba(255, 255, 255, 0.45) !important;
        border-radius: 16px !important;
        padding: 24px !important;
        box-shadow: 0 10px 30px rgba(31, 38, 135, 0.03) !important;
        backdrop-filter: blur(8px) !important;
        margin-bottom: 20px !important;
    }

    /* Customize the file uploader dropzone background inside the wrapper to be light/glossy instead of dark */
    div[data-testid="stVerticalBlockBorderWrapper"]:has([data-testid="stFileUploader"]) [data-testid="stFileUploadDropzone"] {
        background-color: rgba(245, 243, 255, 0.45) !important;
        border: 2.5px dashed #8B5CF6 !important;
        border-radius: 12px !important;
    }

    /* Style the Browse Files button inside the wrapper uploader to match the background gradient */
    div[data-testid="stVerticalBlockBorderWrapper"]:has([data-testid="stFileUploader"]) [data-testid="stFileUploadDropzone"] button {
        background: linear-gradient(135deg, #7C3AED 0%, #6366F1 100%) !important;
        color: white !important;
        border-radius: 8px !important;
        border: none !important;
        padding: 8px 18px !important;
        font-weight: 600 !important;
        font-family: 'Outfit', sans-serif !important;
        box-shadow: 0 4px 12px rgba(124, 58, 237, 0.15) !important;
        transition: all 0.3s ease !important;
    }
    div[data-testid="stVerticalBlockBorderWrapper"]:has([data-testid="stFileUploader"]) [data-testid="stFileUploadDropzone"] button:hover {
        background: linear-gradient(135deg, #8B5CF6 0%, #7C3AED 100%) !important;
        transform: translateY(-1px) !important;
        box-shadow: 0 6px 15px rgba(124, 58, 237, 0.25) !important;
        color: white !important;
    }

    /* Text elements inside dropzone */
    div[data-testid="stVerticalBlockBorderWrapper"]:has([data-testid="stFileUploader"]) [data-testid="stFileUploadDropzone"] div[data-testid="stMarkdownContainer"] p {
        color: #4B5563 !important;
    }
    div[data-testid="stVerticalBlockBorderWrapper"]:has([data-testid="stFileUploader"]) [data-testid="stFileUploadDropzone"] span {
        color: #6B7280 !important;
    }

    /* Custom File upload dropzone styles */
    section[data-testid="stFileUploadDropzone"] {
        border: 2px dashed #8B5CF6 !important;
        background-color: rgba(245, 243, 255, 0.6) !important;
        border-radius: 16px !important;
        padding: 30px 20px !important;
        transition: all 0.2s ease;
    }
    
    section[data-testid="stFileUploadDropzone"]:hover {
        border-color: #7C3AED !important;
        background-color: rgba(245, 243, 255, 0.9) !important;
    }

    /* Profile Card styling matching the wireframe */
    .profile-card {
        background: rgba(255, 255, 255, 0.75) !important;
        border: 1px solid rgba(255, 255, 255, 0.45) !important;
        border-radius: 16px !important;
        padding: 20px !important;
        box-shadow: 0 8px 32px rgba(31, 38, 135, 0.03) !important;
        backdrop-filter: blur(8px) !important;
        margin-bottom: 20px !important;
    }
    .profile-header {
        display: flex;
        align-items: center;
        gap: 12px;
        margin-bottom: 12px;
    }
    .profile-avatar {
        width: 44px;
        height: 44px;
        border-radius: 50%;
        background: #E0F2FE;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: 600;
        font-size: 15px;
        color: #0369A1;
        font-family: 'Outfit', sans-serif;
    }
    .profile-info {
        flex-grow: 1;
    }
    .profile-name {
        font-weight: 700;
        font-size: 16px;
        color: #111827;
        font-family: 'Outfit', sans-serif;
    }
    .profile-contact {
        font-size: 13px;
        color: #4B5563;
        margin-top: 2px;
    }
    .profile-skills-row {
        display: flex;
        gap: 8px;
        flex-wrap: wrap;
        margin-top: 8px;
    }
    .profile-skill-chip {
        background: #E0F2FE;
        color: #0369A1;
        font-size: 12px;
        padding: 3px 12px;
        border-radius: 99px;
        font-weight: 600;
        border: 1px solid rgba(3, 105, 161, 0.1);
    }

    /* ATS Scorecard Results Layout */
    .ats-results-grid {
        display: flex;
        gap: 12px;
        margin-bottom: 12px;
        width: 100%;
    }
    .ats-score-col-left {
        flex: 1;
        background: rgba(255, 255, 255, 0.8) !important;
        border: 1px solid rgba(255, 255, 255, 0.5) !important;
        border-radius: 12px !important;
        padding: 20px;
        text-align: center;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.01) !important;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        min-height: 120px;
    }
    .ats-score-col-right {
        flex: 2;
        background: rgba(255, 255, 255, 0.8) !important;
        border: 1px solid rgba(255, 255, 255, 0.5) !important;
        border-radius: 12px !important;
        padding: 20px;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.01) !important;
        display: flex;
        flex-direction: column;
        justify-content: center;
        min-height: 120px;
    }
    .ats-score-num {
        font-size: 32px;
        font-weight: 700;
        color: #185FA5;
        font-family: 'Outfit', sans-serif;
    }
    .ats-score-denom {
        font-size: 15px;
        color: #6B7280;
        font-weight: 500;
    }
    .ats-score-label {
        font-size: 12px;
        color: #6B7280;
        margin-top: 4px;
        font-weight: 600;
    }
    .ats-progress-label {
        font-size: 12px;
        color: #4B5563;
        font-weight: 600;
        margin-bottom: 5px;
    }
    .ats-progress-track {
        height: 8px;
        background: #E5E7EB;
        border-radius: 4px;
        overflow: hidden;
        margin-bottom: 12px;
    }
    .ats-progress-track:last-child {
        margin-bottom: 0;
    }
    .ats-progress-bar {
        height: 100%;
        border-radius: 4px;
    }
    .skill-match-bar {
        background: #185FA5;
    }
    .keyword-match-bar {
        background: #1D9E75;
    }

    /* Custom ChatGPT-style bubbles styling */
    .chat-bubble-user {
        background: linear-gradient(135deg, #7C3AED 0%, #6366F1 100%);
        color: white;
        padding: 14px 18px;
        border-radius: 18px 18px 0px 18px;
        margin-bottom: 12px;
        max-width: 80%;
        align-self: flex-end;
        box-shadow: 0 4px 15px rgba(124, 58, 237, 0.15);
        font-size: 14px;
        line-height: 1.5;
        margin-left: auto;
    }
    
    .chat-bubble-assistant {
        background: rgba(255, 255, 255, 0.85);
        border: 1px solid rgba(255, 255, 255, 0.6);
        color: #1F2937;
        padding: 14px 18px;
        border-radius: 18px 18px 18px 0px;
        margin-bottom: 12px;
        max-width: 80%;
        align-self: flex-start;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.02);
        font-size: 14px;
        line-height: 1.5;
        border-left: 4px solid #8B5CF6;
    }

    /* RAG Chat Input typing text and placeholder overrides (forcing visible white text on dark background) */
    div[data-testid="stChatInput"] textarea,
    div[data-testid="stChatInput"] textarea:focus,
    div[data-testid="stChatInput"] textarea:active,
    div[data-testid="stChatInputTextArea"],
    div[data-testid="stChatInputTextArea"]:focus,
    div[data-testid="stChatInputTextArea"]:active,
    .stChatInput textarea,
    .stChatInput textarea:focus,
    div[data-testid="stBottom"] textarea,
    div[data-testid="stBottom"] textarea:focus,
    div[data-baseweb="textarea"] textarea,
    div[data-baseweb="textarea"] textarea:focus {
        color: #FFFFFF !important;
        -webkit-text-fill-color: #FFFFFF !important;
        caret-color: #FFFFFF !important;
        font-weight: 500 !important;
    }

    div[data-testid="stChatInput"] textarea::placeholder,
    div[data-testid="stChatInputTextArea"]::placeholder,
    .stChatInput textarea::placeholder,
    div[data-testid="stBottom"] textarea::placeholder,
    div[data-baseweb="textarea"] textarea::placeholder {
        color: rgba(255, 255, 255, 0.65) !important;
        -webkit-text-fill-color: rgba(255, 255, 255, 0.65) !important;
    }

    /* Chat input submit button icon */
    button[data-testid="stChatInputSubmitButton"],
    button[data-testid="stChatInputSubmitButton"]:hover,
    button[data-testid="stChatInputSubmitButton"] svg,
    div[data-testid="stChatInput"] button svg {
        color: #FFFFFF !important;
        fill: #FFFFFF !important;
    }

    /* Accordions/Expanders overrides */
    .streamlit-expanderHeader {
        background-color: rgba(255, 255, 255, 0.6) !important;
        border-radius: 8px !important;
        border: 1px solid rgba(255, 255, 255, 0.4) !important;
        font-weight: 600 !important;
        font-size: 14px !important;
        color: #374151 !important;
    }

    /* Suppress vertical block wrapper empty box */
    div[data-testid="element-container"]:has(.hidden-trigger-marker) {
        display: none !important;
    }

    /* Micro-animations keyframes */
    @keyframes fadeIn {
        from {
            opacity: 0;
            transform: translateY(8px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
</style>
"""

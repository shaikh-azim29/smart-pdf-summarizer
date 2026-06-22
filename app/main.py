import os
import sys

# Robust path handling: Add the workspace root to Python path
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)

import streamlit as st
from app.summarizer import get_api_key, get_model_name

# Page Configuration
st.set_page_config(
    page_title="Multi-Format PDF Summarization Studio",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)


def inject_custom_css():
    st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&display=swap');

        html, body, [class*="css"], .stMarkdown {
            font-family: 'Outfit', 'Inter', sans-serif;
        }

        .header-container {
            background: linear-gradient(135deg, #1e3a8a 0%, #2563eb 50%, #3b82f6 100%);
            padding: 30px;
            border-radius: 16px;
            color: white;
            margin-bottom: 25px;
            box-shadow: 0 4px 20px rgba(37, 99, 235, 0.15);
            text-align: center;
        }
        .header-title {
            font-size: 2.5rem;
            font-weight: 800;
            margin: 0;
            letter-spacing: -0.5px;
        }
        .header-subtitle {
            font-size: 1.1rem;
            font-weight: 300;
            opacity: 0.9;
            margin-top: 10px;
        }

        .metric-card {
            background: rgba(255, 255, 255, 0.8);
            border: 1px solid rgba(229, 231, 235, 0.5);
            border-radius: 12px;
            padding: 15px;
            text-align: center;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.02);
        }
        .metric-val {
            font-size: 1.8rem;
            font-weight: 700;
            color: #1e3a8a;
        }
        .metric-label {
            font-size: 0.9rem;
            color: #4b5563;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }

        .glass-panel {
            background: #ffffff;
            border: 1px solid #e5e7eb;
            border-radius: 12px;
            padding: 20px;
            margin-bottom: 20px;
            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.02);
        }

        .sidebar-header {
            font-size: 1.25rem;
            font-weight: 700;
            color: #1e3a8a;
            margin-bottom: 15px;
        }
    </style>
    """, unsafe_allow_html=True)


inject_custom_css()

# --- SIDEBAR: Day 8 layout (uploader, format selector, sliders) ---
with st.sidebar:
    st.markdown('<p class="sidebar-header">🛠️ Studio Control Panel</p>', unsafe_allow_html=True)

    env_api_key = get_api_key()
    api_key_placeholder = "Enter API Key..."
    if env_api_key and env_api_key != "your_gemini_api_key_here":
        api_key_placeholder = "🔑 Key loaded from Environment"

    st.text_input(
        "Google Gemini API Key",
        type="password",
        placeholder=api_key_placeholder,
        help="Paste your Google AI Studio Gemini API Key. Overrides config/.env file."
    )

    st.markdown("---")

    # File Uploader (Day 8 deliverable)
    uploaded_file = st.file_uploader(
        "Upload PDF Document",
        type=["pdf"],
        help="Upload a multi-page PDF document to summarize."
    )

    st.markdown("---")

    # Format Selector (Day 8 deliverable)
    st.markdown('<p class="sidebar-header">⚙️ Summary Adjustments</p>', unsafe_allow_html=True)

    summary_format = st.selectbox(
        "Summary Format",
        options=["Executive Summary", "Action-Items Checklist", "Q&A Study Guide", "Core Timeline"],
        help="Choose the narrative style for the final output report."
    )

    chunk_size = st.slider(
        "Text Chunk Size (chars)",
        min_value=1500,
        max_value=5000,
        value=3000,
        step=500,
        help="Target size for mapping chunks."
    )

    chunk_overlap = st.slider(
        "Chunk Overlap (chars)",
        min_value=0,
        max_value=500,
        value=200,
        step=50,
        help="Overlap size to maintain context between contiguous chunks."
    )

    st.markdown("---")
    st.caption("Smart PDF Summarizer v0.8 (Day 8 build)")
    st.caption("Assigned Student: Shaikh Ajimuddin")

# --- MAIN LAYOUT (Day 8: static rendering only) ---
st.markdown("""
<div class="header-container">
    <h1 class="header-title">📄 Multi-Format PDF Summarization Studio</h1>
    <p class="header-subtitle">Analyze, parse, and condense documents of any size using manual Map-Reduce chunking & Gemini AI</p>
</div>
""", unsafe_allow_html=True)

if not uploaded_file:
    # Welcome banner shown when no file is uploaded yet
    st.markdown("""
    <div class="glass-panel" style="text-align: center; padding: 40px;">
        <h3 style="color:#1e3a8a; font-weight:700;">Welcome to the Summarization Studio!</h3>
        <p style="color:#4b5563; max-width: 600px; margin: 15px auto;">
            To get started, drag-and-drop a PDF file into the <b>Upload PDF Document</b> area
            on the left control panel, and select your target summary format.
        </p>
        <div style="display:flex; justify-content:center; gap: 20px; margin-top:20px; flex-wrap: wrap;">
            <div class="metric-card" style="width: 130px;">
                <div class="metric-val">⚡</div>
                <div class="metric-label" style="font-size:0.75rem;">Fast Parsing</div>
            </div>
            <div class="metric-card" style="width: 130px;">
                <div class="metric-val">🧩</div>
                <div class="metric-label" style="font-size:0.75rem;">Map-Reduce</div>
            </div>
            <div class="metric-card" style="width: 130px;">
                <div class="metric-val">📈</div>
                <div class="metric-label" style="font-size:0.75rem;">4 Formats</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
else:
    # Day 8 scope: show file stats only. Wiring this up to the real
    # Map-Reduce pipeline (parser -> chunker -> summarizer -> DB) is
    # Day 10: App Integration.
    file_bytes = uploaded_file.getvalue()
    file_size_kb = len(file_bytes) / 1024
    size_str = f"{file_size_kb:.1f} KB" if file_size_kb < 1024 else f"{file_size_kb/1024:.2f} MB"

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">📁 File Name</div>
            <div style="font-size: 1.15rem; font-weight: 700; color: #1e3a8a; margin-top:5px;">
                {uploaded_file.name}
            </div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">⚖️ File Size</div>
            <div class="metric-val">{size_str}</div>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">🧩 Selected Format</div>
            <div style="font-size: 1.1rem; font-weight: 700; color: #1e3a8a; margin-top:5px;">
                {summary_format}
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.button("🚀 Generate Summarization Report", use_container_width=False, type="primary")
    st.caption(
        f"Will segment text into blocks of ~{chunk_size} characters using "
        f"'{summary_format}' layout. (Pipeline wiring comes in Day 10: App Integration.)"
    )

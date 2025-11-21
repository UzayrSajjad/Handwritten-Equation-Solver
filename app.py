import streamlit as st
from streamlit_drawable_canvas import st_canvas
from PIL import Image
import numpy as np
import cv2
from utils.preprocess import predict
import base64
import os


# Initialize theme in session state
if 'dark_mode' not in st.session_state:
    st.session_state.dark_mode = True

st.set_page_config(
    page_title="Handy Math — AI Equation Solver", 
    layout="wide",
    initial_sidebar_state="collapsed"
)
# Initialize theme in session state
if 'dark_mode' not in st.session_state:
    st.session_state.dark_mode = True

st.set_page_config(
    page_title="Handy Math — AI Equation Solver", 
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Modern 2025 Color Palette
if st.session_state.dark_mode:
    BG_PRIMARY = "#0a0e1a"
    BG_SECONDARY = "#131829"
    BG_CARD = "#1a1f35"
    TEXT_PRIMARY = "#ffffff"
    TEXT_SECONDARY = "#94a3b8"
    ACCENT_1 = "#818cf8"  # Indigo
    ACCENT_2 = "#a78bfa"  # Purple
    ACCENT_3 = "#6366f1"  # Deep Indigo
    BORDER = "#2d3548"
    CANVAS_BG = "#ffffff"
else:
    BG_PRIMARY = "#ffffff"
    BG_SECONDARY = "#f8fafc"
    BG_CARD = "#ffffff"
    TEXT_PRIMARY = "#0f172a"
    TEXT_SECONDARY = "#64748b"
    ACCENT_1 = "#6366f1"
    ACCENT_2 = "#8b5cf6"
    ACCENT_3 = "#4f46e5"
    BORDER = "#e2e8f0"
    CANVAS_BG = "#ffffff"


_CSS = f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

* {{
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
}}

/* Hide Streamlit branding */
#MainMenu {{visibility: hidden;}}
footer {{visibility: hidden;}}
header {{visibility: hidden;}}

/* Root styles */
.stApp {{
    background: {BG_PRIMARY};
    background-image: 
        radial-gradient(at 0% 0%, {ACCENT_1}15 0px, transparent 50%),
        radial-gradient(at 100% 100%, {ACCENT_2}15 0px, transparent 50%);
}}

/* Custom scrollbar */
::-webkit-scrollbar {{
    width: 8px;
    height: 8px;
}}
::-webkit-scrollbar-track {{
    background: {BG_SECONDARY};
}}
::-webkit-scrollbar-thumb {{
    background: {ACCENT_1};
    border-radius: 4px;
}}
::-webkit-scrollbar-thumb:hover {{
    background: {ACCENT_3};
}}

/* Header */
.main-header {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 24px 0;
    margin-bottom: 32px;
}}

.logo-section {{
    display: flex;
    align-items: center;
    gap: 16px;
}}

.logo {{
    width: 64px;
    height: 64px;
    border-radius: 16px;
    background: linear-gradient(135deg, {ACCENT_1}, {ACCENT_2});
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: 800;
    font-size: 28px;
    color: white;
    box-shadow: 0 8px 32px {ACCENT_1}40;
    position: relative;
    overflow: hidden;
}}

.logo::before {{
    content: '';
    position: absolute;
    width: 100%;
    height: 100%;
    background: linear-gradient(135deg, transparent, rgba(255,255,255,0.2));
    transform: translateX(-100%);
    transition: transform 0.6s;
}}

.logo:hover::before {{
    transform: translateX(100%);
}}

.title-section {{
    display: flex;
    flex-direction: column;
    gap: 4px;
}}

.app-title {{
    font-size: 32px;
    font-weight: 800;
    margin: 0;
    background: linear-gradient(135deg, {ACCENT_1}, {ACCENT_2});
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}}

.app-subtitle {{
    color: {TEXT_SECONDARY};
    font-size: 14px;
    font-weight: 500;
    margin: 0;
}}

/* Theme Toggle */
.theme-toggle {{
    background: {BG_CARD};
    border: 2px solid {BORDER};
    border-radius: 12px;
    padding: 8px 16px;
    cursor: pointer;
    transition: all 0.3s ease;
    display: flex;
    align-items: center;
    gap: 8px;
    font-weight: 600;
    color: {TEXT_PRIMARY};
}}

.theme-toggle:hover {{
    border-color: {ACCENT_1};
    transform: translateY(-2px);
    box-shadow: 0 8px 16px {ACCENT_1}20;
}}

/* Glass Card */
.glass-card {{
    background: {BG_CARD};
    backdrop-filter: blur(20px);
    border: 1px solid {BORDER};
    border-radius: 20px;
    padding: 32px;
    box-shadow: 0 8px 32px rgba(0,0,0,0.1);
    transition: all 0.3s ease;
}}

.glass-card:hover {{
    border-color: {ACCENT_1}50;
    box-shadow: 0 12px 48px {ACCENT_1}15;
}}

.canvas-container {{
    background: transparent;
    padding: 0;
    border: none;
    box-shadow: none;
}}

/* Remove all black backgrounds and center canvas */
.stTabs [data-baseweb="tab-panel"] {{
    background: transparent !important;
}}

.stTabs [data-baseweb="tab-panel"] > div {{
    background: transparent !important;
}}

.stTabs [data-baseweb="tab-panel"] > div > div {{
    background: transparent !important;
}}

/* Target all parent containers of canvas */
.element-container {{
    background: transparent !important;
}}

.stBlock {{
    background: transparent !important;
}}

/* Ensure canvas iframe and its parents are transparent */
.element-container:has(iframe[title*="canvas"]) {{
    background: transparent !important;
    display: flex !important;
    justify-content: center !important;
}}

iframe[title*="canvas"] {{
    background: transparent !important;
}}

/* Make sure there's no dark background anywhere in tabs */
div[data-testid="stVerticalBlock"] {{
    background: transparent !important;
}}

div[data-testid="stHorizontalBlock"] {{
    background: transparent !important;
}}

/* Hide any overflow to prevent black areas */
.stTabs [data-baseweb="tab-panel"] {{
    overflow: hidden !important;
}}

/* Ensure column containers are transparent and centered */
.stColumn {{
    background: transparent !important;
}}

/* Center the canvas within its container */
.stColumn > div {{
    display: flex !important;
    justify-content: center !important;
    align-items: center !important;
}}

/* Section Headers */
.section-header {{
    font-size: 24px;
    font-weight: 700;
    color: {TEXT_PRIMARY};
    margin: 0 0 8px 0;
}}

.section-description {{
    color: {TEXT_SECONDARY};
    font-size: 14px;
    margin: 0 0 24px 0;
}}

/* Tabs */
.stTabs [data-baseweb="tab-list"] {{
    gap: 0px;
    background: {BG_SECONDARY};
    padding: 6px;
    border-radius: 12px;
    border-bottom: none;
    display: flex;
    width: 100%;
}}

.stTabs [data-baseweb="tab-list"] button {{
    border-bottom: none !important;
}}

.stTabs [data-baseweb="tab"] {{
    border-radius: 8px;
    color: {TEXT_SECONDARY};
    font-weight: 600;
    padding: 12px 24px;
    border: none !important;
    background: transparent;
    transition: all 0.3s ease;
    flex: 1;
    text-align: center;
    position: relative;
    overflow: hidden;
}}

.stTabs [data-baseweb="tab"]::after {{
    display: none;
}}

.stTabs [aria-selected="true"] {{
    background: linear-gradient(135deg, {ACCENT_1}, {ACCENT_2});
    color: white !important;
    box-shadow: 0 4px 12px {ACCENT_1}40;
    border: none !important;
    position: relative;
}}

.stTabs [aria-selected="true"]::before {{
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: linear-gradient(135deg, {ACCENT_1}, {ACCENT_2});
    border-radius: 8px;
    z-index: -1;
}}

.stTabs [data-baseweb="tab-highlight"] {{
    display: none !important;
}}

/* Buttons */
.stButton > button {{
    background: linear-gradient(135deg, {ACCENT_1}, {ACCENT_2});
    color: white;
    border: none;
    border-radius: 12px;
    padding: 14px 28px;
    font-weight: 600;
    font-size: 15px;
    transition: all 0.3s ease;
    box-shadow: 0 4px 16px {ACCENT_1}30;
    width: 100%;
}}

.stButton > button:hover {{
    transform: translateY(-2px);
    box-shadow: 0 8px 24px {ACCENT_1}50;
}}

.stButton > button:active {{
    transform: translateY(0);
}}

/* Secondary Button */
.secondary-btn {{
    background: {BG_SECONDARY} !important;
    color: {TEXT_PRIMARY} !important;
    border: 2px solid {BORDER} !important;
}}

.secondary-btn:hover {{
    border-color: {ACCENT_1} !important;
    background: {BG_CARD} !important;
}}

/* Result Card */
.result-card {{
    background: linear-gradient(135deg, {ACCENT_1}15, {ACCENT_2}15);
    border: 2px solid {ACCENT_1}30;
    border-radius: 16px;
    padding: 24px;
    margin-top: 24px;
    animation: slideUp 0.5s ease;
}}

@keyframes slideUp {{
    from {{
        opacity: 0;
        transform: translateY(20px);
    }}
    to {{
        opacity: 1;
        transform: translateY(0);
    }}
}}

.result-header {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 16px;
}}

.result-label {{
    color: {TEXT_SECONDARY};
    font-size: 14px;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 1px;
}}

.result-value {{
    background: linear-gradient(135deg, {ACCENT_1}, {ACCENT_2});
    color: white;
    padding: 12px 24px;
    border-radius: 12px;
    font-size: 28px;
    font-weight: 800;
    box-shadow: 0 4px 16px {ACCENT_1}40;
}}

.equation-display {{
    color: {TEXT_PRIMARY};
    font-size: 20px;
    font-weight: 600;
    margin-top: 12px;
}}

.equation-label {{
    color: {TEXT_SECONDARY};
    font-size: 14px;
    margin-bottom: 4px;
}}

/* Tips Card */
.tips-card {{
    background: {BG_CARD};
    border: 1px solid {BORDER};
    border-radius: 16px;
    padding: 28px;
    height: 320px;
    display: flex;
    flex-direction: column;
    transition: all 0.3s ease;
}}

.tips-card:hover {{
    border-color: {ACCENT_1}50;
    box-shadow: 0 8px 24px {ACCENT_1}15;
    transform: translateY(-4px);
}}

.tips-title {{
    font-size: 20px;
    font-weight: 700;
    color: {TEXT_PRIMARY};
    margin-bottom: 20px;
    display: flex;
    align-items: center;
    gap: 12px;
    padding-bottom: 16px;
    border-bottom: 2px solid {BORDER};
}}

.tips-icon {{
    font-size: 28px;
    display: flex;
    align-items: center;
    justify-content: center;
    width: 48px;
    height: 48px;
    background: linear-gradient(135deg, {ACCENT_1}20, {ACCENT_2}20);
    border-radius: 12px;
}}

.tips-list {{
    list-style: none;
    padding: 0;
    margin: 0;
    flex: 1;
}}

.tips-list li {{
    color: {TEXT_SECONDARY};
    font-size: 14px;
    line-height: 1.6;
    padding: 12px 0;
    padding-left: 32px;
    position: relative;
    border-bottom: 1px solid {BORDER}20;
}}

.tips-list li:last-child {{
    border-bottom: none;
}}

.tips-list li::before {{
    content: '✓';
    position: absolute;
    left: 0;
    color: {ACCENT_1};
    font-weight: 700;
    font-size: 18px;
    width: 24px;
    height: 24px;
    background: {ACCENT_1}15;
    border-radius: 6px;
    display: flex;
    align-items: center;
    justify-content: center;
}}

/* Expander */
.streamlit-expanderHeader {{
    background: {BG_SECONDARY};
    border-radius: 12px;
    color: {TEXT_PRIMARY};
    font-weight: 600;
    border: 1px solid {BORDER};
}}

/* Slider */
.stSlider {{
    padding: 8px 0;
}}

.stSlider > div > div > div {{
    background: {ACCENT_1};
}}

/* File Uploader */
.stFileUploader {{
    border: 2px dashed {BORDER};
    border-radius: 12px;
    padding: 24px;
    background: {BG_SECONDARY};
    transition: all 0.3s ease;
}}

.stFileUploader:hover {{
    border-color: {ACCENT_1};
    background: {BG_CARD};
}}

/* Canvas Container */
canvas {{
    border-radius: 12px;
    box-shadow: 0 4px 16px rgba(0,0,0,0.1);
}}

/* Info badges */
.badge {{
    display: inline-block;
    padding: 6px 12px;
    background: {ACCENT_1}20;
    color: {ACCENT_1};
    border-radius: 8px;
    font-size: 12px;
    font-weight: 600;
    margin-right: 8px;
}}

/* Footer */
.footer {{
    text-align: center;
    padding: 32px 0;
    color: {TEXT_SECONDARY};
    font-size: 14px;
    border-top: 1px solid {BORDER};
    margin-top: 48px;
}}

.footer-gradient {{
    background: linear-gradient(135deg, {ACCENT_1}, {ACCENT_2});
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    font-weight: 700;
}}

</style>
"""


st.markdown(_CSS, unsafe_allow_html=True)


def render_header():
    col1, col2 = st.columns([4, 1])
    with col1:
        st.markdown("""
            <div class='main-header'>
                <div class='logo-section'>
                    <div class='logo'>HM</div>
                    <div class='title-section'>
                        <h1 class='app-title'>Handy Math</h1>
                        <p class='app-subtitle'>AI-Powered Handwritten Equation Solver</p>
                    </div>
                </div>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        # Show "Light Mode" when in dark mode, "Dark Mode" when in light mode
        if st.session_state.dark_mode:
            theme_label = "☀️ Light Mode"
        else:
            theme_label = "🌙 Dark Mode"
        
        if st.button(theme_label, key="theme_toggle"):
            st.session_state.dark_mode = not st.session_state.dark_mode
            st.rerun()


def render_result_card(equation, result):
    st.markdown(f"""
        <div class='result-card'>
            <div class='result-header'>
                <div>
                    <div class='result-label'>Result</div>
                    <div class='equation-label'>Recognized Equation</div>
                </div>
                <div class='result-value'>{result}</div>
            </div>
            <div class='equation-display'>
                <span style='color: {TEXT_SECONDARY}'>Expression:</span> {equation}
            </div>
        </div>
    """, unsafe_allow_html=True)


def render_tips():
    st.markdown(f"""
        <div class='tips-card'>
            <div class='tips-title'>
                <div class='tips-icon'>💡</div>
                <div>Pro Tips</div>
            </div>
            <ul class='tips-list'>
                <li>Write large, well-spaced characters</li>
                <li>Use dark ink on light background</li>
                <li>Avoid overlapping symbols</li>
                <li>Keep numbers and operators clear</li>
            </ul>
        </div>
    """, unsafe_allow_html=True)


def render_about():
    st.markdown(f"""
        <div class='tips-card'>
            <div class='tips-title'>
                <div class='tips-icon'>ℹ️</div>
                <div>About</div>
            </div>
            <div style='flex: 1;'>
                <p style='color: {TEXT_SECONDARY}; font-size: 14px; line-height: 1.8; margin: 0 0 20px 0;'>
                    <strong style='color: {TEXT_PRIMARY}'>Handy Math</strong> uses deep learning 
                    to recognize handwritten digits and operators (+, -, ×, ÷) and instantly 
                    evaluates your mathematical expressions.
                </p>
                <div style='display: flex; gap: 8px; flex-wrap: wrap;'>
                    <span class='badge'>CNN Model</span>
                    <span class='badge'>Real-time</span>
                    <span class='badge'>AI-Powered</span>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)


render_header()

st.write("")

# Main layout: Left side (app interactivity) + Right side (tips and about vertically)
main_col1, main_col2 = st.columns([2, 1], gap="large")

with main_col1:
    # Centralized main canvas section
    st.markdown("<div class='glass-card canvas-container'>", unsafe_allow_html=True)
    st.markdown(f"<h3 class='section-header' style='text-align: center;'>Draw or Upload Your Equation</h3><p class='section-description' style='text-align: center;'>Create your equation by drawing on the canvas or uploading an image</p>", unsafe_allow_html=True)

    tab1, tab2 = st.tabs(["🖌️ Draw", "📷 Upload"])

    with tab1:
        st.markdown(f"<p style='color: {TEXT_SECONDARY}; font-size: 14px; margin-bottom: 16px; text-align: center;'>Use the interactive canvas below to write your equation</p>", unsafe_allow_html=True)
        
        # Centered expander
        col_left, col_center, col_right = st.columns([1, 2, 1])
        with col_center:
            with st.expander("⚙️ Drawing Settings", expanded=False):
                stroke_width = st.slider("Stroke Width", min_value=3, max_value=25, value=10)
                bg_color = st.color_picker("Canvas Background", value=CANVAS_BG)

        # Centered canvas with fixed width
        col_canvas_left, col_canvas_center, col_canvas_right = st.columns([0.05, 1, 0.05])
        with col_canvas_center:
            data = st_canvas(
                stroke_width=stroke_width,
                stroke_color="#1a1f35",
                background_color=bg_color,
                update_streamlit=True,
                height=400,
                width=1050,
                drawing_mode="freedraw",
                key=f"canvas_app_{st.session_state.get('canvas_key', 0)}",
            )

        # Centered buttons below canvas
        col_left, col_btn1, col_btn2, col_right = st.columns([1, 1, 1, 1])
        
        with col_btn1:
            predict_clicked = st.button('🚀 Predict Equation', key="predict_canvas", use_container_width=True)
        
        with col_btn2:
            if st.button('🗑️ Clear Canvas', key="clear_canvas", use_container_width=True):
                st.session_state.canvas_key = st.session_state.get('canvas_key', 0) + 1
                st.rerun()
        
        # Process prediction after buttons are rendered
        if predict_clicked:
            if data is None or data.image_data is None:
                st.warning("⚠️ Please draw an equation first!")
            else:
                with st.spinner("🔮 Analyzing your equation..."):
                    path = 'temp/temp.png'
                    os.makedirs(os.path.dirname(path), exist_ok=True)
                    try:
                        img = data.image_data
                        if img.dtype != np.uint8:
                            img = np.clip(img, 0, 255).astype(np.uint8)
                        if img.ndim == 3 and img.shape[2] == 4:
                            img = cv2.cvtColor(img, cv2.COLOR_RGBA2BGR)
                        cv2.imwrite(path, img)
                        eq, res = predict(path)
                        render_result_card(eq, res)
                    except Exception as e:
                        st.error(f"❌ Failed to process drawing: {e}")

    with tab2:
        st.markdown(f"<p style='color: {TEXT_SECONDARY}; font-size: 14px; margin-bottom: 16px; text-align: center;'>Upload a clear photo of your handwritten equation</p>", unsafe_allow_html=True)
        
        # Centered file uploader
        col_left, col_center, col_right = st.columns([1, 2, 1])
        with col_center:
            uploaded_file = st.file_uploader("📁 Choose an image file", type=['png', 'jpg', 'jpeg', 'bmp'], label_visibility="collapsed")
        
        if uploaded_file is not None:
            # Centered image preview
            col_left, col_center, col_right = st.columns([0.5, 2, 0.5])
            with col_center:
                image = Image.open(uploaded_file)
                st.image(image, caption="📸 Your Uploaded Image", use_column_width=True)
            
            image_array = np.array(image)
            if len(image_array.shape) == 3:
                image_cv = cv2.cvtColor(image_array, cv2.COLOR_RGB2BGR)
            else:
                image_cv = image_array
                
            upload_path = 'temp/uploaded_image.png'
            os.makedirs(os.path.dirname(upload_path), exist_ok=True)
            cv2.imwrite(upload_path, image_cv)
            
            # Centered button
            col_left, col_center, col_right = st.columns([1, 1, 1])
            with col_center:
                if st.button('🚀 Analyze Image', key="predict_upload"):
                    with st.spinner("🔮 Processing your equation..."):
                        eq, res = predict(upload_path)
                        render_result_card(eq, res)

    st.markdown("</div>", unsafe_allow_html=True)

with main_col2:
    # Tips and About stacked vertically on the right
    render_tips()
    st.write("")
    render_about()
    
st.markdown(f"""
    <div class='footer'>
        Made with <span class='footer-gradient'>❤️</span> using Deep Learning
        <br><small style='color: {TEXT_SECONDARY}'>Handy Math © 2025</small>
    </div>
""", unsafe_allow_html=True)

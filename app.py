import streamlit as st
import json
from streamlit_option_menu import option_menu
from streamlit_lottie import st_lottie
import requests

# Page configuration
st.set_page_config(
    page_title="Swayam Sites - AI Portfolio Builder",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for clean, professional UI
def load_css():
    st.markdown("""
    <style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Global Styles */
    .main {
        font-family: 'Inter', sans-serif;
    }
    
    /* Clean gradient background */
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        background-attachment: fixed;
    }
    
    /* Main container styling */
    .main-container {
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(10px);
        border-radius: 20px;
        padding: 2rem;
        margin: 1rem;
        box-shadow: 0 20px 40px rgba(0,0,0,0.1);
        border: 1px solid rgba(255,255,255,0.2);
    }
    
    /* Animated title */
    .animated-title {
        background: linear-gradient(45deg, #667eea, #764ba2, #f093fb, #f5576c);
        background-size: 400% 400%;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: gradient 3s ease infinite;
        font-size: 3rem;
        font-weight: 700;
        text-align: center;
        margin-bottom: 1rem;
    }
    
    @keyframes gradient {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    /* Card styling */
    .feature-card {
        background: rgba(255, 255, 255, 0.9);
        border-radius: 15px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        border: 1px solid rgba(255,255,255,0.3);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    
    .feature-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 20px 40px rgba(0,0,0,0.15);
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(45deg, #667eea, #764ba2);
        color: white !important;
        border: none;
        border-radius: 25px;
        padding: 0.75rem 2rem;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 5px 15px rgba(102, 126, 234, 0.3);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 25px rgba(102, 126, 234, 0.4);
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(10px);
    }
    
    /* Text input styling for better visibility */
    .stTextInput > div > div > input {
        background-color: white !important;
        color: #333 !important;
        border: 2px solid #e0e0e0 !important;
        border-radius: 10px !important;
        padding: 0.75rem !important;
        font-size: 1rem !important;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #667eea !important;
        box-shadow: 0 0 0 2px rgba(102, 126, 234, 0.2) !important;
    }
    
    /* Password input styling */
    .stTextInput > div > div > input[type="password"] {
        background-color: white !important;
        color: #333 !important;
        border: 2px solid #e0e0e0 !important;
        border-radius: 10px !important;
        padding: 0.75rem !important;
        font-size: 1rem !important;
    }
    
    /* Text area styling */
    .stTextArea > div > div > textarea {
        background-color: white !important;
        color: #333 !important;
        border: 2px solid #e0e0e0 !important;
        border-radius: 10px !important;
        padding: 0.75rem !important;
        font-size: 1rem !important;
    }
    
    /* Select box styling */
    .stSelectbox > div > div > select {
        background-color: white !important;
        color: #333 !important;
        border: 2px solid #e0e0e0 !important;
        border-radius: 10px !important;
    }
    
    /* Form labels */
    .stTextInput > label,
    .stTextArea > label,
    .stSelectbox > label {
        color: #333 !important;
        font-weight: 600 !important;
        font-size: 1rem !important;
        margin-bottom: 0.5rem !important;
    }
    
    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    
    .stTabs [data-baseweb="tab"] {
        background-color: rgba(255, 255, 255, 0.7);
        border-radius: 10px;
        color: #333;
        border: 1px solid #e0e0e0;
        padding: 0.5rem 1rem;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(45deg, #667eea, #764ba2);
        color: white !important;
        box-shadow: 0 5px 15px rgba(102, 126, 234, 0.3);
    }
    
    /* Success/Error message styling */
    .stSuccess {
        background-color: rgba(0, 255, 65, 0.1) !important;
        border: 1px solid rgba(0, 255, 65, 0.3) !important;
        border-radius: 10px !important;
        color: #00aa00 !important;
    }
    
    .stError {
        background-color: rgba(255, 0, 0, 0.1) !important;
        border: 1px solid rgba(255, 0, 0, 0.3) !important;
        border-radius: 10px !important;
        color: #cc0000 !important;
    }
    
    .stWarning {
        background-color: rgba(255, 165, 0, 0.1) !important;
        border: 1px solid rgba(255, 165, 0, 0.3) !important;
        border-radius: 10px !important;
        color: #ff8800 !important;
    }
    
    .stInfo {
        background-color: rgba(0, 123, 255, 0.1) !important;
        border: 1px solid rgba(0, 123, 255, 0.3) !important;
        border-radius: 10px !important;
        color: #007bff !important;
    }
    
    /* Checkbox styling */
    .stCheckbox > label {
        color: #333 !important;
        font-size: 1rem !important;
    }
    
    /* Radio button styling */
    .stRadio > label {
        color: #333 !important;
        font-size: 1rem !important;
        font-weight: 600 !important;
    }
    
    /* Multiselect styling */
    .stMultiSelect > label {
        color: #333 !important;
        font-size: 1rem !important;
        font-weight: 600 !important;
    }
    
    /* Number input styling */
    .stNumberInput > div > div > input {
        background-color: white !important;
        color: #333 !important;
        border: 2px solid #e0e0e0 !important;
        border-radius: 10px !important;
    }
    
    /* Date input styling */
    .stDateInput > div > div > input {
        background-color: white !important;
        color: #333 !important;
        border: 2px solid #e0e0e0 !important;
        border-radius: 10px !important;
    }
    
    /* Ensure all text is readable */
    .main .block-container {
        color: #333 !important;
    }
    
    /* Headers */
    h1, h2, h3, h4, h5, h6 {
        color: #333 !important;
    }
    
    /* Paragraphs */
    p {
        color: #555 !important;
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .stDeployButton {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# Load Lottie animation
def load_lottie_url(url: str):
    try:
        r = requests.get(url)
        if r.status_code != 200:
            return None
        return r.json()
    except:
        return None

def main():
    load_css()
    
    # Check if user is logged in
    if 'logged_in' not in st.session_state:
        st.session_state['logged_in'] = False
    
    # If not logged in, show login page
    if not st.session_state['logged_in']:
        from pages import login
        login.app()
        return
    
    # Header with animation for logged-in users
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown('<h1 class="animated-title">🚀 Swayam Sites</h1>', unsafe_allow_html=True)
        st.markdown('<p style="text-align: center; font-size: 1.2rem; color: #666; margin-bottom: 2rem;">AI-Powered Portfolio Builder</p>', unsafe_allow_html=True)
    
    # Load Lottie animation
    lottie_coding = load_lottie_url("https://assets5.lottiefiles.com/packages/lf20_fcfjwiyb.json")
    
    if lottie_coding:
        col1, col2, col3 = st.columns([1, 1, 1])
        with col2:
            st_lottie(lottie_coding, height=200, key="coding")
    
    # Navigation menu
    with st.sidebar:
        # User info
        if 'username' in st.session_state:
            st.markdown(f"### 👋 Welcome, {st.session_state['username']}!")
            
            # Save session button
            if st.button("💾 Save Session"):
                from pages.login import save_user_session_data
                session_data = {
                    'template_choice': st.session_state.get('template_choice'),
                    'user_data': st.session_state.get('user_data'),
                    'generated_content': st.session_state.get('generated_content'),
                    'translated_content': st.session_state.get('translated_content'),
                    'custom_content': st.session_state.get('custom_content')
                }
                save_user_session_data(st.session_state['username'], session_data)
                st.success("✅ Session saved!")
            
            # Logout button
            if st.button("🚪 Logout"):
                # Clear session state
                for key in list(st.session_state.keys()):
                    del st.session_state[key]
                st.rerun()
        
        st.markdown("---")
        st.markdown("### 🎯 Navigation")
        selected = option_menu(
            menu_title=None,
            options=["📊 Dashboard", "🎨 Template Selector", "📝 User Input", "🤖 AI Generation", "📄 Preview & PDF"],
            icons=["speedometer2", "palette", "person-fill", "robot", "file-earmark-pdf"],
            menu_icon="cast",
            default_index=0,
            styles={
                "container": {"padding": "0!important", "background-color": "transparent"},
                "icon": {"color": "#667eea", "font-size": "18px"},
                "nav-link": {
                    "font-size": "16px",
                    "text-align": "left",
                    "margin": "0px",
                    "padding": "10px",
                    "border-radius": "10px",
                    "color": "#333",
                    "background-color": "transparent"
                },
                "nav-link-selected": {
                    "background": "linear-gradient(45deg, #667eea, #764ba2)",
                    "color": "white"
                },
            }
        )
    
    # Main content area
    st.markdown('<div class="main-container">', unsafe_allow_html=True)
    
    # Route to different pages
    if selected == "📊 Dashboard":
        from pages import user_dashboard
        user_dashboard.app()
    elif selected == "🎨 Template Selector":
        from pages import template_selector
        template_selector.app()
    elif selected == "📝 User Input":
        from pages import user_input
        user_input.app()
    elif selected == "🤖 AI Generation":
        from pages import auto_generation
        auto_generation.app()
    elif selected == "📄 Preview & PDF":
        from pages import preview_pdf
        preview_pdf.app()
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Footer
    st.markdown("---")
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown('<p style="text-align: center; color: #666;">Made with ❤️ using Streamlit & AI</p>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()
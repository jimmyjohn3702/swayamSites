import streamlit as st
from streamlit_lottie import st_lottie
import requests

def load_lottie_url(url: str):
    try:
        r = requests.get(url)
        if r.status_code != 200:
            return None
        return r.json()
    except:
        return None

def app():
    st.markdown("## 🎨 Choose Your Template")
    st.markdown("Select the perfect template for your portfolio")
    
    # Template options with animations
    col1, col2, col3 = st.columns(3)
    
    templates = {
        "Resume": {
            "icon": "📄",
            "description": "Professional resume template with modern design",
            "color": "#667eea",
            "lottie": "https://assets2.lottiefiles.com/packages/lf20_w51pcehl.json"
        },
        "Portfolio": {
            "icon": "💼", 
            "description": "Creative portfolio showcase for your projects",
            "color": "#764ba2",
            "lottie": "https://assets4.lottiefiles.com/packages/lf20_qp1q7mct.json"
        },
        "Poetry": {
            "icon": "✍️",
            "description": "Elegant template for poets and writers",
            "color": "#f093fb",
            "lottie": "https://assets1.lottiefiles.com/packages/lf20_jcikwtux.json"
        }
    }
    
    selected_template = None
    
    for i, (template_name, template_info) in enumerate(templates.items()):
        col = [col1, col2, col3][i]
        
        with col:
            # Create card container
            st.markdown(f"""
            <div style="
                background: linear-gradient(135deg, {template_info['color']}22, {template_info['color']}11);
                border-radius: 15px;
                padding: 1.5rem;
                text-align: center;
                border: 2px solid transparent;
                transition: all 0.3s ease;
                cursor: pointer;
                margin-bottom: 1rem;
            ">
                <div style="font-size: 3rem; margin-bottom: 1rem;">{template_info['icon']}</div>
                <h3 style="color: {template_info['color']}; margin-bottom: 0.5rem;">{template_name}</h3>
                <p style="color: #666; font-size: 0.9rem;">{template_info['description']}</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Load and display Lottie animation
            lottie_anim = load_lottie_url(template_info['lottie'])
            if lottie_anim:
                st_lottie(lottie_anim, height=150, key=f"template_{template_name}")
            
            if st.button(f"Select {template_name}", key=f"btn_{template_name}", use_container_width=True):
                selected_template = template_name
                st.session_state['template_choice'] = template_name
                st.success(f"✅ {template_name} template selected!")
                st.balloons()
    
    # Display current selection
    if 'template_choice' in st.session_state:
        st.markdown("---")
        st.markdown(f"### 🎯 Current Selection: **{st.session_state['template_choice']}**")
        
        # Template preview
        template_choice = st.session_state['template_choice']
        if template_choice in templates:
            st.markdown(f"""
            <div style="
                background: linear-gradient(135deg, {templates[template_choice]['color']}22, {templates[template_choice]['color']}11);
                border-radius: 10px;
                padding: 1rem;
                border-left: 4px solid {templates[template_choice]['color']};
            ">
                <h4>{templates[template_choice]['icon']} {template_choice}</h4>
                <p>{templates[template_choice]['description']}</p>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("👉 **Next Step:** Go to 'User Input' to enter your details!")
    
    # Features showcase
    st.markdown("---")
    st.markdown("### ✨ What You'll Get")
    
    features_col1, features_col2 = st.columns(2)
    
    with features_col1:
        st.markdown("""
        - 🎨 **Modern Design** - Clean, professional layouts
        - 📱 **Responsive** - Looks great on all devices
        - 🌍 **Multi-language** - Support for Indian languages
        """)
    
    with features_col2:
        st.markdown("""
        - 🤖 **AI-Powered** - Auto-generated content
        - 📄 **PDF Export** - Download your portfolio
        - 🚀 **Fast & Easy** - Ready in minutes
        """)
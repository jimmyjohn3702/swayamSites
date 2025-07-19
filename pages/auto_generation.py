import streamlit as st
import requests
import json
from datetime import datetime
from utils.storage import save_generated_content
from utils.api_integration import get_ai_content, translate_content, test_api_connection
from streamlit_lottie import st_lottie

def load_lottie_url(url: str):
    try:
        r = requests.get(url)
        if r.status_code != 200:
            return None
        return r.json()
    except:
        return None



def app():
    st.markdown("## 🤖 AI Content Generation")
    st.markdown("Let AI create personalized content for your portfolio")
    
    # Check if user data exists
    if 'user_data' not in st.session_state:
        st.warning("⚠️ Please enter your details first!")
        st.markdown("👈 Go to 'User Input' to enter your information.")
        return
    
    user_data = st.session_state['user_data']
    template_choice = user_data.get('template_choice', 'Resume')
    
    # Display user info summary
    st.markdown(f"### 👤 Generating content for: **{user_data['personal_info']['name']}**")
    st.markdown(f"**Template:** {template_choice}")
    
    # AI Generation Section
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("#### 🎯 Content Generation Options")
        
        # Generation tabs
        gen_tab1, gen_tab2, gen_tab3 = st.tabs(["🚀 Auto Generate", "✏️ Custom Prompt", "🌍 Translation"])
        
        with gen_tab1:
            st.markdown("##### Automatic Content Generation")
            st.markdown("AI will create content based on your profile information")
            
            content_types = st.multiselect(
                "Select content to generate:",
                ["Professional Summary", "Skills Description", "Project Descriptions", "Career Objectives", "Personal Statement"],
                default=["Professional Summary", "Skills Description"]
            )
            
            if st.button("🚀 Generate Content", type="primary"):
                with st.spinner("🤖 AI is crafting your content..."):
                    generated_content = {}
                    
                    for content_type in content_types:
                        # Create prompt based on user data and content type
                        prompt = create_prompt(user_data, content_type, template_choice)
                        # Use task-specific AI generation
                        task_type = template_choice.lower()
                        content = get_ai_content(prompt, task_type, max_tokens=600)
                        generated_content[content_type] = content
                    
                    # Save generated content
                    st.session_state['generated_content'] = generated_content
                    save_generated_content({
                        "user_name": user_data['personal_info']['name'],
                        "template": template_choice,
                        "content": generated_content
                    })
                    
                    st.success("✅ Content generated successfully!")
                    st.balloons()
        
        with gen_tab2:
            st.markdown("##### Custom Content Generation")
            custom_prompt = st.text_area(
                "Enter your custom prompt:",
                placeholder="Write a professional bio for a software developer with 3 years of experience...",
                height=100
            )
            
            if st.button("Generate Custom Content") and custom_prompt:
                with st.spinner("🤖 Processing your request..."):
                    custom_content = get_ai_content(custom_prompt)
                    st.session_state['custom_content'] = custom_content
                    st.success("✅ Custom content generated!")
        
        with gen_tab3:
            st.markdown("##### Multi-language Support")
            
            if 'generated_content' in st.session_state:
                target_lang = st.selectbox(
                    "Translate to:",
                    ["Hindi", "Tamil", "Telugu", "Bengali", "Marathi", "Gujarati", "Kannada", "Malayalam", "Punjabi"]
                )
                
                if st.button("🌍 Translate Content"):
                    with st.spinner(f"Translating to {target_lang}..."):
                        translated_content = {}
                        for key, content in st.session_state['generated_content'].items():
                            translated_content[key] = translate_content(content, target_lang)
                        
                        st.session_state['translated_content'] = {
                            'language': target_lang,
                            'content': translated_content
                        }
                        st.success(f"✅ Content translated to {target_lang}!")
            else:
                st.info("Generate content first to enable translation")
    
    with col2:
        # Animation
        lottie_ai = load_lottie_url("https://assets4.lottiefiles.com/packages/lf20_M9p23l.json")
        if lottie_ai:
            st_lottie(lottie_ai, height=200, key="ai_generation")
        
        # API Status
        st.markdown("#### 🔑 API Status")
        
        if st.button("🧪 Test API Connection"):
            with st.spinner("Testing API connection..."):
                test_result = test_api_connection()
                
                if test_result["status"] == "success":
                    st.success("✅ API is working!")
                    st.info(f"Model: {test_result['model']}")
                    with st.expander("Test Response"):
                        st.write(test_result["message"])
                else:
                    st.error("❌ API connection failed")
                    st.error(test_result["message"])
        
        # API Info
        st.markdown("#### ℹ️ API Information")
        st.info("""
        **Integrated APIs:**
        • Google Gemini Flash (Fast & Efficient)
        • DeepSeek Chat (Technical Content)
        • Moonshot Kimi (Creative Writing)
        
        **Features:**
        • Automatic model selection
        • Load balancing across keys
        • Fallback to demo content
        """)
        
        # Usage Statistics
        if 'generated_content' in st.session_state and st.session_state['generated_content'] is not None:
            st.markdown("#### 📊 Generation Stats")
            total_sections = len(st.session_state['generated_content'])
            st.metric("Sections Generated", total_sections)
            
            total_words = sum(len(content.split()) for content in st.session_state['generated_content'].values())
            st.metric("Total Words", total_words)
    
    # Display Generated Content
    if 'generated_content' in st.session_state:
        st.markdown("---")
        st.markdown("### 📝 Generated Content")
        
        for content_type, content in st.session_state['generated_content'].items():
            with st.expander(f"📄 {content_type}", expanded=True):
                st.markdown(content)
                
                # Edit option
                edited_content = st.text_area(
                    f"Edit {content_type}:",
                    value=content,
                    height=150,
                    key=f"edit_{content_type}"
                )
                
                if edited_content != content:
                    if st.button(f"Save Changes to {content_type}", key=f"save_{content_type}"):
                        st.session_state['generated_content'][content_type] = edited_content
                        st.success(f"✅ {content_type} updated!")
    
    # Display Translated Content
    if 'translated_content' in st.session_state:
        st.markdown("---")
        st.markdown(f"### 🌍 Content in {st.session_state['translated_content']['language']}")
        
        for content_type, content in st.session_state['translated_content']['content'].items():
            with st.expander(f"📄 {content_type} ({st.session_state['translated_content']['language']})", expanded=False):
                st.markdown(content)
    
    # Custom Content Display
    if 'custom_content' in st.session_state:
        st.markdown("---")
        st.markdown("### ✏️ Custom Generated Content")
        st.markdown(st.session_state['custom_content'])
    
    # Progress and Next Steps
    if 'generated_content' in st.session_state:
        st.markdown("---")
        st.markdown("### 📊 Progress")
        progress_col1, progress_col2, progress_col3, progress_col4 = st.columns(4)
        
        with progress_col1:
            st.markdown("✅ **Template Selected**")
        with progress_col2:
            st.markdown("✅ **Details Entered**")
        with progress_col3:
            st.markdown("✅ **Content Generated**")
        with progress_col4:
            st.markdown("⏳ **Preview & Export**")
        
        st.markdown("👉 **Next Step:** Go to 'Preview & PDF' to see your final portfolio!")

def create_prompt(user_data, content_type, template_choice):
    """Create AI prompt based on user data and content type"""
    name = user_data['personal_info']['name']
    bio = user_data['personal_info']['bio']
    
    base_info = f"Name: {name}\nBio: {bio}\nTemplate: {template_choice}"
    
    prompts = {
        "Professional Summary": f"Write a professional summary for {name} based on this information: {base_info}. Make it engaging and highlight key strengths.",
        "Skills Description": f"Create a compelling skills description for {name} based on: {base_info}. Focus on technical and soft skills.",
        "Project Descriptions": f"Write engaging project descriptions for {name}'s portfolio based on: {base_info}. Make them sound impactful.",
        "Career Objectives": f"Create career objectives for {name} based on: {base_info}. Make them specific and ambitious.",
        "Personal Statement": f"Write a personal statement for {name} based on: {base_info}. Make it authentic and memorable."
    }
    
    return prompts.get(content_type, f"Create professional content for {name} based on: {base_info}")
import streamlit as st
import pandas as pd
from datetime import datetime
import json

def app():
    st.markdown("## 📝 Enter Your Details")
    st.markdown("Tell us about yourself to create your personalized portfolio")
    
    # Check if template is selected
    if 'template_choice' not in st.session_state:
        st.warning("⚠️ Please select a template first!")
        st.markdown("👈 Go to 'Template Selector' to choose your template.")
        return
    
    # Display selected template
    st.markdown(f"### 🎯 Creating: **{st.session_state['template_choice']}**")
    
    # Create tabs for different sections
    tab1, tab2, tab3, tab4 = st.tabs(["👤 Personal Info", "💼 Professional", "🎯 Skills & Projects", "🌍 Preferences"])
    
    with tab1:
        st.markdown("#### Personal Information")
        
        col1, col2 = st.columns(2)
        
        with col1:
            name = st.text_input("Full Name *", placeholder="Enter your full name")
            email = st.text_input("Email Address *", placeholder="your.email@example.com")
            phone = st.text_input("Phone Number", placeholder="+91 XXXXX XXXXX")
            
        with col2:
            location = st.text_input("Location", placeholder="City, State, Country")
            linkedin = st.text_input("LinkedIn Profile", placeholder="https://linkedin.com/in/yourprofile")
            github = st.text_input("GitHub Profile", placeholder="https://github.com/yourusername")
        
        bio = st.text_area("Professional Bio *", 
                          placeholder="Write a brief description about yourself, your goals, and what makes you unique...",
                          height=100)
    
    with tab2:
        st.markdown("#### Professional Experience")
        
        # Experience section
        st.markdown("##### Work Experience")
        num_experiences = st.number_input("Number of work experiences", min_value=0, max_value=10, value=1)
        
        experiences = []
        for i in range(int(num_experiences)):
            with st.expander(f"Experience #{i+1}"):
                exp_col1, exp_col2 = st.columns(2)
                with exp_col1:
                    job_title = st.text_input(f"Job Title", key=f"job_title_{i}")
                    company = st.text_input(f"Company", key=f"company_{i}")
                with exp_col2:
                    start_date = st.date_input(f"Start Date", key=f"start_date_{i}")
                    end_date = st.date_input(f"End Date", key=f"end_date_{i}")
                
                job_description = st.text_area(f"Job Description", key=f"job_desc_{i}", height=80)
                
                if job_title and company:
                    experiences.append({
                        "title": job_title,
                        "company": company,
                        "start_date": str(start_date),
                        "end_date": str(end_date),
                        "description": job_description
                    })
        
        # Education section
        st.markdown("##### Education")
        education_col1, education_col2 = st.columns(2)
        
        with education_col1:
            degree = st.text_input("Degree/Qualification")
            institution = st.text_input("Institution/University")
        
        with education_col2:
            graduation_year = st.number_input("Graduation Year", min_value=1990, max_value=2030, value=2023)
            grade = st.text_input("Grade/CGPA", placeholder="e.g., 8.5/10 or First Class")
    
    with tab3:
        st.markdown("#### Skills & Projects")
        
        # Skills section
        st.markdown("##### Technical Skills")
        skills_col1, skills_col2 = st.columns(2)
        
        with skills_col1:
            programming_languages = st.text_input("Programming Languages", 
                                                placeholder="Python, JavaScript, Java, etc.")
            frameworks = st.text_input("Frameworks & Libraries", 
                                     placeholder="React, Django, Flask, etc.")
        
        with skills_col2:
            tools = st.text_input("Tools & Technologies", 
                                placeholder="Git, Docker, AWS, etc.")
            databases = st.text_input("Databases", 
                                    placeholder="MySQL, MongoDB, PostgreSQL, etc.")
        
        # Projects section
        st.markdown("##### Projects")
        num_projects = st.number_input("Number of projects", min_value=0, max_value=10, value=2)
        
        projects = []
        for i in range(int(num_projects)):
            with st.expander(f"Project #{i+1}"):
                proj_col1, proj_col2 = st.columns(2)
                with proj_col1:
                    project_name = st.text_input(f"Project Name", key=f"proj_name_{i}")
                    project_url = st.text_input(f"Project URL/GitHub", key=f"proj_url_{i}")
                
                with proj_col2:
                    tech_stack = st.text_input(f"Technologies Used", key=f"tech_stack_{i}")
                
                project_description = st.text_area(f"Project Description", key=f"proj_desc_{i}", height=80)
                
                if project_name:
                    projects.append({
                        "name": project_name,
                        "url": project_url,
                        "technologies": tech_stack,
                        "description": project_description
                    })
    
    with tab4:
        st.markdown("#### Preferences & Settings")
        
        pref_col1, pref_col2 = st.columns(2)
        
        with pref_col1:
            st.markdown("##### Language Preferences")
            primary_language = st.selectbox("Primary Language", 
                                          ["English", "Hindi", "Tamil", "Telugu", "Bengali", "Marathi", "Gujarati", "Kannada", "Malayalam", "Punjabi"])
            
            include_translation = st.checkbox("Include content in regional language")
            
            if include_translation:
                secondary_language = st.selectbox("Secondary Language", 
                                                ["Hindi", "Tamil", "Telugu", "Bengali", "Marathi", "Gujarati", "Kannada", "Malayalam", "Punjabi", "English"])
        
        with pref_col2:
            st.markdown("##### Design Preferences")
            color_theme = st.selectbox("Color Theme", 
                                     ["Professional Blue", "Creative Purple", "Modern Green", "Elegant Black", "Warm Orange"])
            
            include_photo = st.checkbox("Include profile photo section")
            
            layout_style = st.radio("Layout Style", 
                                   ["Minimalist", "Detailed", "Creative"])
    
    # Save button
    st.markdown("---")
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        if st.button("💾 Save Details & Continue", use_container_width=True, type="primary"):
            # Validate required fields
            if not name or not email or not bio:
                st.error("❌ Please fill in all required fields (marked with *)")
                return
            
            # Compile all user data
            user_data = {
                "timestamp": datetime.now().isoformat(),
                "template_choice": st.session_state.get('template_choice'),
                "personal_info": {
                    "name": name,
                    "email": email,
                    "phone": phone,
                    "location": location,
                    "linkedin": linkedin,
                    "github": github,
                    "bio": bio
                },
                "professional": {
                    "experiences": experiences,
                    "education": {
                        "degree": degree,
                        "institution": institution,
                        "graduation_year": graduation_year,
                        "grade": grade
                    }
                },
                "skills_projects": {
                    "programming_languages": programming_languages,
                    "frameworks": frameworks,
                    "tools": tools,
                    "databases": databases,
                    "projects": projects
                },
                "preferences": {
                    "primary_language": primary_language,
                    "secondary_language": secondary_language if include_translation else None,
                    "include_translation": include_translation,
                    "color_theme": color_theme,
                    "include_photo": include_photo,
                    "layout_style": layout_style
                }
            }
            
            # Save to session state
            st.session_state['user_data'] = user_data
            
            # Save to CSV for persistence
            try:
                df = pd.DataFrame([user_data])
                df.to_csv("user_details.csv", index=False)
                st.success("✅ Details saved successfully!")
                st.balloons()
                st.markdown("👉 **Next Step:** Go to 'AI Generation' to create your content!")
                
            except Exception as e:
                st.error(f"❌ Error saving data: {str(e)}")
    
    # Progress indicator
    if 'user_data' in st.session_state:
        st.markdown("---")
        st.markdown("### 📊 Progress")
        progress_col1, progress_col2, progress_col3, progress_col4 = st.columns(4)
        
        with progress_col1:
            st.markdown("✅ **Template Selected**")
        with progress_col2:
            st.markdown("✅ **Details Entered**")
        with progress_col3:
            st.markdown("⏳ **AI Generation**")
        with progress_col4:
            st.markdown("⏳ **Preview & Export**")
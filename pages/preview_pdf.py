import streamlit as st
import json
from datetime import datetime
import base64

def app():
    st.markdown("## 📄 Preview & Export")
    st.markdown("Review your portfolio and export as PDF")
    
    # Check if all required data exists
    if 'user_data' not in st.session_state:
        st.warning("⚠️ Please enter your details first!")
        return
    
    if 'generated_content' not in st.session_state:
        st.warning("⚠️ Please generate content first!")
        return
    
    user_data = st.session_state['user_data']
    generated_content = st.session_state['generated_content']
    
    # Preview Options
    col1, col2 = st.columns([3, 1])
    
    with col2:
        st.markdown("#### 🎨 Preview Options")
        
        # Theme selection
        theme = st.selectbox(
            "Color Theme:",
            ["Professional Blue", "Creative Purple", "Modern Green", "Elegant Black", "Warm Orange"]
        )
        
        # Layout options
        layout = st.radio(
            "Layout Style:",
            ["Single Column", "Two Column", "Modern Grid"]
        )
        
        # Include options
        include_photo = st.checkbox("Include Photo Placeholder", value=True)
        include_contact = st.checkbox("Include Contact Info", value=True)
        include_translation = st.checkbox("Include Translated Content", 
                                        value='translated_content' in st.session_state)
    
    with col1:
        # Generate preview based on template and theme
        preview_html = generate_preview_html(user_data, generated_content, theme, layout, 
                                           include_photo, include_contact, include_translation)
        
        # Create a styled container for the preview
        with st.container():
            st.markdown(
                """
                <style>
                .preview-container {
                    border: 2px solid #ddd;
                    border-radius: 10px;
                    padding: 20px;
                    background: white;
                    box-shadow: 0 4px 6px rgba(0,0,0,0.1);
                    max-height: 600px;
                    overflow-y: auto;
                    margin: 10px 0;
                }
                </style>
                """,
                unsafe_allow_html=True
            )
            
            # Render the preview content properly
            st.markdown(f'<div class="preview-container">{preview_html}</div>', unsafe_allow_html=True)
    
    # Export Options
    st.markdown("---")
    st.markdown("### 📤 Export Options")
    
    export_col1, export_col2, export_col3 = st.columns(3)
    
    with export_col1:
        if st.button("📄 Download as PDF", type="primary", use_container_width=True):
            pdf_content = generate_pdf_content(user_data, generated_content, theme, layout)
            
            # For demo purposes, create a simple text file
            # In production, use libraries like pdfkit or weasyprint
            st.download_button(
                label="📥 Download Portfolio.pdf",
                data=pdf_content,
                file_name=f"{user_data['personal_info']['name']}_Portfolio.pdf",
                mime="application/pdf"
            )
            st.success("✅ PDF ready for download!")
    
    with export_col2:
        if st.button("📱 Download as HTML", use_container_width=True):
            html_content = generate_full_html(user_data, generated_content, theme, layout)
            
            st.download_button(
                label="📥 Download Portfolio.html",
                data=html_content,
                file_name=f"{user_data['personal_info']['name']}_Portfolio.html",
                mime="text/html"
            )
            st.success("✅ HTML ready for download!")
    
    with export_col3:
        if st.button("📊 Download Data (JSON)", use_container_width=True):
            portfolio_data = {
                "user_data": user_data,
                "generated_content": generated_content,
                "export_settings": {
                    "theme": theme,
                    "layout": layout,
                    "timestamp": datetime.now().isoformat()
                }
            }
            
            json_content = json.dumps(portfolio_data, indent=2, ensure_ascii=False)
            
            st.download_button(
                label="📥 Download Data.json",
                data=json_content,
                file_name=f"{user_data['personal_info']['name']}_Data.json",
                mime="application/json"
            )
            st.success("✅ Data ready for download!")
    
    # Portfolio Statistics
    st.markdown("---")
    st.markdown("### 📊 Portfolio Statistics")
    
    stats_col1, stats_col2, stats_col3, stats_col4 = st.columns(4)
    
    with stats_col1:
        st.metric("Sections", len(generated_content))
    
    with stats_col2:
        total_words = sum(len(content.split()) for content in generated_content.values())
        st.metric("Total Words", total_words)
    
    with stats_col3:
        projects_count = len(user_data.get('skills_projects', {}).get('projects', []))
        st.metric("Projects", projects_count)
    
    with stats_col4:
        experience_count = len(user_data.get('professional', {}).get('experiences', []))
        st.metric("Experiences", experience_count)
    
    # Completion Status
    st.markdown("---")
    st.markdown("### ✅ Completion Status")
    
    progress_col1, progress_col2, progress_col3, progress_col4 = st.columns(4)
    
    with progress_col1:
        st.markdown("✅ **Template Selected**")
    with progress_col2:
        st.markdown("✅ **Details Entered**")
    with progress_col3:
        st.markdown("✅ **Content Generated**")
    with progress_col4:
        st.markdown("✅ **Portfolio Complete**")
    
    # Success message
    st.success("🎉 Congratulations! Your portfolio is ready!")
    st.balloons()

def generate_preview_html(user_data, generated_content, theme, layout, include_photo, include_contact, include_translation):
    """Generate HTML preview of the portfolio"""
    
    # Theme colors
    theme_colors = {
        "Professional Blue": {"primary": "#2E86AB", "secondary": "#A23B72", "accent": "#F18F01"},
        "Creative Purple": {"primary": "#6A4C93", "secondary": "#C06C84", "accent": "#F8B500"},
        "Modern Green": {"primary": "#2D5016", "secondary": "#61A5C2", "accent": "#A9BCD0"},
        "Elegant Black": {"primary": "#2C3E50", "secondary": "#34495E", "accent": "#E74C3C"},
        "Warm Orange": {"primary": "#E67E22", "secondary": "#D35400", "accent": "#F39C12"}
    }
    
    colors = theme_colors.get(theme, theme_colors["Professional Blue"])
    
    personal_info = user_data['personal_info']
    
    html = f"""
    <div style="font-family: 'Inter', sans-serif; color: #333;">
        <!-- Header Section -->
        <div style="background: linear-gradient(135deg, {colors['primary']}, {colors['secondary']}); 
                    color: white; padding: 2rem; border-radius: 10px; margin-bottom: 2rem;">
            <div style="display: flex; align-items: center; gap: 2rem;">
                {f'<div style="width: 100px; height: 100px; background: rgba(255,255,255,0.2); border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 2rem;">📸</div>' if include_photo else ''}
                <div>
                    <h1 style="margin: 0; font-size: 2.5rem; font-weight: 700;">{personal_info['name']}</h1>
                    <p style="margin: 0.5rem 0; font-size: 1.2rem; opacity: 0.9;">{personal_info.get('bio', '')[:100]}...</p>
                    {f'<p style="margin: 0; opacity: 0.8;">📍 {personal_info.get("location", "")}</p>' if include_contact and personal_info.get('location') else ''}
                </div>
            </div>
        </div>
    """
    
    # Contact Information
    if include_contact:
        html += f"""
        <div style="background: #f8f9fa; padding: 1.5rem; border-radius: 10px; margin-bottom: 2rem;">
            <h3 style="color: {colors['primary']}; margin-bottom: 1rem;">📞 Contact Information</h3>
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 1rem;">
                {f'<p>📧 {personal_info.get("email", "")}</p>' if personal_info.get('email') else ''}
                {f'<p>📱 {personal_info.get("phone", "")}</p>' if personal_info.get('phone') else ''}
                {f'<p>💼 LinkedIn</p>' if personal_info.get('linkedin') else ''}
                {f'<p>🐙 GitHub</p>' if personal_info.get('github') else ''}
            </div>
        </div>
        """
    
    # Generated Content Sections
    for section_name, content in generated_content.items():
        html += f"""
        <div style="margin-bottom: 2rem;">
            <h3 style="color: {colors['primary']}; border-bottom: 2px solid {colors['accent']}; 
                       padding-bottom: 0.5rem; margin-bottom: 1rem;">
                {get_section_icon(section_name)} {section_name}
            </h3>
            <div style="background: white; padding: 1.5rem; border-radius: 10px; 
                       border-left: 4px solid {colors['primary']}; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
                {content.replace('\n', '<br>')}
            </div>
        </div>
        """
    
    # Projects Section
    projects = user_data.get('skills_projects', {}).get('projects', [])
    if projects:
        html += f"""
        <div style="margin-bottom: 2rem;">
            <h3 style="color: {colors['primary']}; border-bottom: 2px solid {colors['accent']}; 
                       padding-bottom: 0.5rem; margin-bottom: 1rem;">
                🚀 Projects
            </h3>
        """
        
        for project in projects:
            html += f"""
            <div style="background: white; padding: 1.5rem; border-radius: 10px; margin-bottom: 1rem;
                       border-left: 4px solid {colors['secondary']}; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
                <h4 style="color: {colors['primary']}; margin-bottom: 0.5rem;">{project.get('name', '')}</h4>
                <p style="color: #666; margin-bottom: 0.5rem;"><strong>Tech:</strong> {project.get('technologies', '')}</p>
                <p>{project.get('description', '')}</p>
            </div>
            """
        
        html += "</div>"
    
    html += "</div>"
    return html

def get_section_icon(section_name):
    """Get appropriate icon for section"""
    icons = {
        "Professional Summary": "👨‍💼",
        "Skills Description": "🛠️",
        "Project Descriptions": "🚀",
        "Career Objectives": "🎯",
        "Personal Statement": "💭"
    }
    return icons.get(section_name, "📄")

def generate_pdf_content(user_data, generated_content, theme, layout):
    """Generate PDF content as formatted text"""
    personal_info = user_data['personal_info']
    
    content = f"""
SWAYAM SITES - AI PORTFOLIO BUILDER
{'=' * 50}

PORTFOLIO FOR: {personal_info['name'].upper()}
Generated on: {datetime.now().strftime('%B %d, %Y at %I:%M %p')}

{'=' * 50}
PERSONAL INFORMATION
{'=' * 50}

Name: {personal_info['name']}
Email: {personal_info.get('email', 'Not provided')}
Phone: {personal_info.get('phone', 'Not provided')}
Location: {personal_info.get('location', 'Not provided')}
LinkedIn: {personal_info.get('linkedin', 'Not provided')}
GitHub: {personal_info.get('github', 'Not provided')}

Bio: {personal_info.get('bio', 'Not provided')}

{'=' * 50}
GENERATED CONTENT
{'=' * 50}
"""
    
    for section, text in generated_content.items():
        content += f"""
{section.upper()}
{'-' * len(section)}
{text}

"""
    
    # Add projects if available
    projects = user_data.get('skills_projects', {}).get('projects', [])
    if projects:
        content += f"""
{'=' * 50}
PROJECTS
{'=' * 50}
"""
        for i, project in enumerate(projects, 1):
            content += f"""
{i}. {project.get('name', 'Untitled Project')}
   Technologies: {project.get('technologies', 'Not specified')}
   Description: {project.get('description', 'No description provided')}
   URL: {project.get('url', 'Not provided')}

"""
    
    # Add professional experience if available
    experiences = user_data.get('professional', {}).get('experiences', [])
    if experiences:
        content += f"""
{'=' * 50}
PROFESSIONAL EXPERIENCE
{'=' * 50}
"""
        for i, exp in enumerate(experiences, 1):
            content += f"""
{i}. {exp.get('title', 'Position')} at {exp.get('company', 'Company')}
   Duration: {exp.get('start_date', 'Start')} to {exp.get('end_date', 'End')}
   Description: {exp.get('description', 'No description provided')}

"""
    
    content += f"""
{'=' * 50}
END OF PORTFOLIO
{'=' * 50}

Generated by Swayam Sites - AI Portfolio Builder
Visit us at: https://swayam-sites.streamlit.app
"""
    
    return content.encode('utf-8')

def generate_full_html(user_data, generated_content, theme, layout):
    """Generate complete HTML file"""
    preview_content = generate_preview_html(user_data, generated_content, theme, layout, True, True, False)
    
    html = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>{user_data['personal_info']['name']} - Portfolio</title>
        <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
        <style>
            body {{
                margin: 0;
                padding: 20px;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
            }}
            .container {{
                max-width: 1000px;
                margin: 0 auto;
                background: white;
                border-radius: 20px;
                padding: 2rem;
                box-shadow: 0 20px 40px rgba(0,0,0,0.1);
            }}
        </style>
    </head>
    <body>
        <div class="container">
            {preview_content}
        </div>
    </body>
    </html>
    """
    
    return html
import requests
import json
import random
import streamlit as st
from typing import Dict, List, Optional

class OpenRouterAPI:
    """OpenRouter API integration with multiple API keys and models"""
    
    def __init__(self):
        # Your provided API keys
        self.api_keys = [
            "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",  # Gemini Flash
            "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",  # DeepSeek
            "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",  # Claude
            "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",  # Venice
            "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"   # Sarvam
        ]
        
        self.base_url = "https://openrouter.ai/api/v1/chat/completions"
        
        # Model configurations
        self.models = {
            "gemini": {
                "name": "google/gemini-flash-1.5",
                "description": "Fast and efficient for general tasks",
                "max_tokens": 8192
            },
            "deepseek": {
                "name": "deepseek/deepseek-chat",
                "description": "Great for coding and technical content",
                "max_tokens": 4096
            },
            "claude": {
                "name": "anthropic/claude-3-haiku",
                "description": "Excellent for creative writing",
                "max_tokens": 4096
            },
            "venice": {
                "name": "openai/gpt-4o-mini",
                "description": "Versatile model for various tasks",
                "max_tokens": 4096
            },
            "sarvam": {
                "name": "meta-llama/llama-3.1-8b-instruct",
                "description": "Great for multilingual content",
                "max_tokens": 4096
            }
        }
    
    def get_random_api_key(self) -> str:
        """Get a random API key for load balancing"""
        return random.choice(self.api_keys)
    
    def get_model_for_task(self, task_type: str) -> str:
        """Select the best model based on task type"""
        task_model_mapping = {
            "resume": "gemini",
            "portfolio": "venice", 
            "poetry": "claude",
            "technical": "deepseek",
            "creative": "claude",
            "general": "sarvam",
            "multilingual": "sarvam"
        }
        
        model_key = task_model_mapping.get(task_type.lower(), "gemini")
        return self.models[model_key]["name"]
    
    def generate_content(self, prompt: str, task_type: str = "general", 
                        max_tokens: int = 500, temperature: float = 0.7) -> Dict:
        """Generate content using OpenRouter API"""
        
        model = self.get_model_for_task(task_type)
        api_key = self.get_random_api_key()
        
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://swayam-sites.streamlit.app",
            "X-Title": "Swayam Sites - AI Portfolio Builder"
        }
        
        payload = {
            "model": model,
            "messages": [
                {
                    "role": "system",
                    "content": "You are a professional content writer specializing in creating compelling portfolio content. Write in a professional, engaging tone that highlights achievements and skills effectively."
                },
                {
                    "role": "user", 
                    "content": prompt
                }
            ],
            "max_tokens": max_tokens,
            "temperature": temperature,
            "top_p": 0.9,
            "frequency_penalty": 0.1,
            "presence_penalty": 0.1
        }
        
        try:
            response = requests.post(
                self.base_url,
                headers=headers,
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                return {
                    "success": True,
                    "content": data["choices"][0]["message"]["content"].strip(),
                    "model_used": model,
                    "tokens_used": data.get("usage", {}).get("total_tokens", 0)
                }
            else:
                return {
                    "success": False,
                    "error": f"API Error {response.status_code}: {response.text}",
                    "model_used": model
                }
                
        except requests.exceptions.Timeout:
            return {
                "success": False,
                "error": "Request timed out. Please try again.",
                "model_used": model
            }
        except requests.exceptions.RequestException as e:
            return {
                "success": False,
                "error": f"Network error: {str(e)}",
                "model_used": model
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"Unexpected error: {str(e)}",
                "model_used": model
            }

# Global API instance
api_client = OpenRouterAPI()

def get_ai_content(prompt: str, task_type: str = "general", max_tokens: int = 500) -> str:
    """Simplified function to get AI content"""
    result = api_client.generate_content(prompt, task_type, max_tokens)
    
    if result["success"]:
        return result["content"]
    else:
        # Fallback to mock content if API fails
        st.warning(f"API Error: {result['error']}. Using demo content.")
        return generate_mock_content(prompt, task_type)

def generate_mock_content(prompt: str, task_type: str = "general") -> str:
    """Generate mock content as fallback"""
    
    mock_content = {
        "resume": {
            "Professional Summary": """
            **Dynamic Professional with Proven Excellence**
            
            Results-driven professional with extensive experience in delivering high-impact solutions and driving organizational success. Demonstrated expertise in project management, team leadership, and strategic planning. Known for innovative problem-solving abilities and commitment to continuous improvement.
            
            **Core Competencies:**
            • Strategic Planning & Execution
            • Team Leadership & Development  
            • Process Optimization & Innovation
            • Stakeholder Management
            • Data-Driven Decision Making
            """,
            
            "Skills Description": """
            **Technical Expertise & Professional Skills**
            
            **Technical Skills:**
            • Programming: Python, JavaScript, Java, C++
            • Web Technologies: React, Node.js, HTML5, CSS3
            • Databases: MySQL, MongoDB, PostgreSQL
            • Cloud Platforms: AWS, Azure, Google Cloud
            • Tools: Git, Docker, Jenkins, JIRA
            
            **Professional Skills:**
            • Project Management (Agile, Scrum)
            • Team Leadership & Mentoring
            • Client Relationship Management
            • Business Analysis & Strategy
            • Quality Assurance & Testing
            """,
            
            "Career Objectives": """
            **Professional Aspirations & Goals**
            
            Seeking to leverage my comprehensive skill set and proven track record in a challenging role that offers opportunities for professional growth and meaningful contribution to organizational success. 
            
            **Short-term Goals:**
            • Lead high-impact projects that drive business value
            • Expand expertise in emerging technologies
            • Mentor junior team members and contribute to knowledge sharing
            
            **Long-term Vision:**
            • Advance to senior leadership positions
            • Drive digital transformation initiatives
            • Build and scale innovative technology solutions
            """,
            
            "Project Descriptions": """
            **Professional Projects & Achievements**
            
            **🏢 Enterprise Solution Development**
            Led the development of a comprehensive business management system that streamlined operations for a 500+ employee organization. Implemented automated workflows, reporting systems, and integration with existing tools.
            *Impact: 40% reduction in processing time, 25% increase in productivity*
            
            **📈 Performance Analytics Platform**
            Designed and built a real-time analytics dashboard that provided actionable insights for business decision-making. Features included custom reporting, data visualization, and automated alerts.
            *Technologies: Python, React, PostgreSQL, AWS*
            
            **🔧 Process Automation Suite**
            Created automated solutions for repetitive business processes, reducing manual work and improving accuracy. Implemented workflow automation, document processing, and notification systems.
            *Result: 60% reduction in manual tasks, improved accuracy by 95%*
            """,
            
            "Personal Statement": """
            **Professional Philosophy & Vision**
            
            I believe in the power of technology to transform businesses and improve lives. My approach combines technical expertise with strategic thinking to deliver solutions that not only meet immediate needs but also position organizations for future growth.
            
            **What Drives Me:**
            • Solving complex problems with elegant solutions
            • Mentoring others and sharing knowledge
            • Staying current with emerging technologies
            • Building systems that make a lasting impact
            
            **My Commitment:**
            To deliver excellence in every project while maintaining the highest standards of professionalism and integrity.
            """
        },
        
        "portfolio": {
            "Professional Summary": """
            **Creative Innovator & Technology Enthusiast**
            
            Passionate creator at the intersection of technology and design, dedicated to building solutions that make a difference. With a strong foundation in both technical development and creative problem-solving, I bring ideas to life through code, design, and strategic thinking.
            
            **What Drives Me:**
            • Creating user-centric solutions that solve real problems
            • Exploring cutting-edge technologies and methodologies
            • Collaborating with diverse teams to achieve exceptional results
            • Continuous learning and adaptation in the ever-evolving tech landscape
            """,
            
            "Project Descriptions": """
            **Featured Projects & Achievements**
            
            **🚀 E-Commerce Platform Revolution**
            Architected and developed a comprehensive e-commerce solution serving 10,000+ active users. Implemented advanced features including real-time inventory management, personalized recommendations, and seamless payment integration.
            *Technologies: React, Node.js, MongoDB, AWS*
            
            **📊 Data Analytics Dashboard**
            Created an interactive business intelligence platform that transformed raw data into actionable insights. Enabled stakeholders to make data-driven decisions with real-time visualizations and automated reporting.
            *Technologies: Python, D3.js, PostgreSQL, Docker*
            
            **📱 Mobile Innovation Hub**
            Developed a cross-platform mobile application that achieved 4.8-star rating and 50,000+ downloads. Features include offline functionality, push notifications, and seamless cloud synchronization.
            *Technologies: React Native, Firebase, Redux*
            """,
            
            "Skills Description": """
            **Technical Arsenal & Creative Capabilities**
            
            **Development Expertise:**
            • Full-Stack Development (MERN, MEAN, Django)
            • Mobile App Development (React Native, Flutter)
            • Cloud Architecture & DevOps (AWS, Docker, Kubernetes)
            • Database Design & Optimization
            • API Development & Integration
            
            **Design & User Experience:**
            • UI/UX Design Principles
            • Responsive Web Design
            • User Research & Testing
            • Prototyping & Wireframing
            • Brand Identity & Visual Design
            """,
            
            "Career Objectives": """
            **Creative Vision & Professional Goals**
            
            To leverage my unique blend of technical expertise and creative vision in building innovative solutions that push the boundaries of what's possible. I aim to work with forward-thinking organizations that value creativity, innovation, and user-centered design.
            
            **Short-term Goals:**
            • Lead creative technology projects that make a meaningful impact
            • Expand expertise in emerging technologies like AI and AR/VR
            • Build a portfolio of award-winning digital experiences
            
            **Long-term Vision:**
            • Establish myself as a thought leader in creative technology
            • Launch innovative products that solve real-world problems
            • Mentor the next generation of creative technologists
            """,
            
            "Personal Statement": """
            **The Intersection of Art and Technology**
            
            I believe that the most powerful solutions emerge at the intersection of creativity and technology. My work is driven by a passion for creating experiences that not only function flawlessly but also inspire and delight users.
            
            **My Philosophy:**
            Every project is an opportunity to push boundaries, challenge conventions, and create something truly remarkable. I approach each challenge with curiosity, creativity, and a commitment to excellence.
            
            **What Sets Me Apart:**
            • Unique blend of technical skills and creative vision
            • User-centered approach to problem-solving
            • Passion for continuous learning and innovation
            • Ability to translate complex ideas into elegant solutions
            """
        },
        
        "poetry": {
            "Professional Summary": """
            **Poet & Literary Artist**
            
            Dedicated wordsmith with a passion for exploring the depths of human experience through verse. My work bridges the gap between traditional poetry and contemporary themes, creating pieces that resonate with modern audiences while honoring the timeless craft of poetry.
            
            **Literary Focus:**
            • Contemporary poetry with classical influences
            • Exploration of technology's impact on human connection
            • Cultural identity and heritage preservation
            • Environmental and social consciousness through verse
            • Collaborative projects with artists and musicians
            """,
            
            "Personal Statement": """
            **Words as Windows to the Soul**
            
            In the realm where language dances with emotion, I find my truest expression. Poetry, for me, is not merely an art form—it's a bridge between the tangible and the ethereal, a way to capture the fleeting moments that define our human experience.
            
            **My Poetic Journey:**
            Through verses that explore love, loss, hope, and transformation, I seek to create connections that transcend the boundaries of individual experience. Each poem is an invitation to pause, reflect, and discover the extraordinary within the ordinary.
            """,
            
            "Skills Description": """
            **Literary Craft & Creative Abilities**
            
            **Writing Expertise:**
            • Traditional and contemporary poetry forms
            • Spoken word and performance poetry
            • Creative writing and storytelling
            • Literary editing and manuscript review
            • Workshop facilitation and teaching
            
            **Creative Skills:**
            • Metaphor and imagery development
            • Rhythm and meter composition
            • Cross-cultural literary translation
            • Collaborative artistic projects
            • Digital poetry and multimedia integration
            """,
            
            "Creative Philosophy": """
            **The Art of Emotional Architecture**
            
            Poetry is the architecture of emotion, where each word is carefully placed like a stone in a cathedral of feeling. I believe in the power of language to heal, to inspire, and to illuminate the hidden corners of the human heart.
            
            **Themes I Explore:**
            • The beauty found in everyday moments
            • The complexity of human relationships
            • Nature as a mirror for inner landscapes
            • The journey of self-discovery and growth
            • Cultural heritage and contemporary identity
            """,
            
            "Project Descriptions": """
            **Literary Projects & Creative Works**
            
            **📚 "Voices of Tomorrow" Poetry Anthology**
            Curated and edited a collection featuring 50 emerging poets from diverse backgrounds. The anthology explores themes of hope, resilience, and cultural identity in the modern world.
            *Impact: 5,000+ copies sold, featured in 3 literary magazines*
            
            **🎭 "Digital Hearts" Multimedia Poetry Series**
            Created an innovative fusion of poetry, visual art, and technology. Each piece combines spoken word with digital imagery and interactive elements.
            *Platform: Online exhibition with 25,000+ views*
            
            **🌍 Community Poetry Workshops**
            Developed and facilitated creative writing workshops for underserved communities, focusing on self-expression and storytelling through poetry.
            *Reach: 200+ participants across 12 workshops*
            """,
            
            "Career Objectives": """
            **Literary Vision & Artistic Goals**
            
            To continue pushing the boundaries of contemporary poetry while honoring its rich traditions. I aim to create work that not only entertains but also challenges, inspires, and brings people together through the shared experience of language.
            
            **Short-term Goals:**
            • Publish a full-length poetry collection
            • Expand community outreach programs
            • Collaborate with musicians and visual artists
            
            **Long-term Vision:**
            • Establish a literary foundation for emerging poets
            • Create innovative digital poetry platforms
            • Mentor the next generation of literary artists
            """,
            
            "Featured Collections": """
            **Literary Journeys & Published Works**
            
            **"Whispers of Dawn" (2023)**
            A collection exploring themes of renewal and hope, where each poem captures the delicate transition from darkness to light. These verses celebrate the resilience of the human spirit and the promise that each new day brings.
            
            **"Urban Symphony" (2022)**
            An exploration of city life through poetic lens, finding rhythm and melody in the chaos of metropolitan existence. These poems reveal the hidden poetry in concrete jungles and the stories that echo through busy streets.
            
            **"Digital Dreams" (2024)**
            A contemporary collection examining our relationship with technology and virtual connections. These verses navigate the intersection of human emotion and digital existence, questioning what it means to be authentic in an increasingly connected world.
            """
        }
    }
    
    # Determine content type from prompt
    content_type = "Professional Summary"
    if "skills" in prompt.lower():
        content_type = "Skills Description"
    elif "project" in prompt.lower():
        content_type = "Project Descriptions"
    elif "objective" in prompt.lower() or "goal" in prompt.lower():
        content_type = "Career Objectives"
    elif "personal" in prompt.lower() or "statement" in prompt.lower():
        content_type = "Personal Statement"
    elif "creative" in prompt.lower() or "philosophy" in prompt.lower():
        content_type = "Creative Philosophy"
    elif "collection" in prompt.lower() or "work" in prompt.lower():
        content_type = "Featured Collections"
    elif "poem" in prompt.lower() or "poetry" in prompt.lower():
        content_type = "Personal Statement"
    
    template_content = mock_content.get(task_type, mock_content["resume"])
    
    # Handle case where content_type doesn't exist in template
    if content_type not in template_content:
        # Return the first available content type
        content_type = list(template_content.keys())[0]
    
    return template_content.get(content_type, "Content generation failed. Please try again.")

def translate_content(content: str, target_language: str) -> str:
    """Translate content using Google Translate"""
    try:
        from googletrans import Translator
        translator = Translator()
        
        # Language codes mapping
        lang_codes = {
            "Hindi": "hi",
            "Tamil": "ta", 
            "Telugu": "te",
            "Bengali": "bn",
            "Marathi": "mr",
            "Gujarati": "gu",
            "Kannada": "kn",
            "Malayalam": "ml",
            "Punjabi": "pa"
        }
        
        target_code = lang_codes.get(target_language, "hi")
        result = translator.translate(content, dest=target_code)
        return result.text
        
    except Exception as e:
        st.error(f"Translation error: {str(e)}")
        return f"[Translation to {target_language} failed: {content}]"

def test_api_connection() -> Dict:
    """Test API connection and return status"""
    test_prompt = "Write a brief professional greeting."
    result = api_client.generate_content(test_prompt, "general", 50)
    
    return {
        "status": "success" if result["success"] else "error",
        "message": result.get("content", result.get("error", "Unknown error")),
        "model": result.get("model_used", "unknown")
    }
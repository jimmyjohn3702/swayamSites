---
title: Swayam Sites - AI Portfolio Builder
emoji: 🚀
colorFrom: blue
colorTo: purple
sdk: streamlit
sdk_version: 1.28.0
app_file: app_hf.py
pinned: false
license: mit
---

# 🚀 Swayam Sites - AI Portfolio Builder

An AI-powered portfolio builder that creates stunning resumes, portfolios, and poetry collections with multi-language support.

## Features

- 🎨 **Multiple Templates**: Resume, Portfolio, Poetry
- 🤖 **AI Content Generation**: Auto-generated professional content
- 🌍 **Multi-language Support**: Indian regional languages
- 📍 **Location Analytics**: User location tracking
- 📄 **Export Options**: PDF, HTML, JSON downloads
- 🔐 **User Authentication**: Secure login system

## How to Use

1. **Register/Login**: Create an account or login
2. **Select Template**: Choose from Resume, Portfolio, or Poetry
3. **Enter Details**: Fill in your information
4. **AI Generation**: Let AI create professional content
5. **Preview & Export**: Download your portfolio

## Tech Stack

- **Frontend**: Streamlit with modern UI
- **AI**: Multiple API integrations (Gemini, DeepSeek, Claude)
- **Location**: IP-based geolocation with browser fallback
- **Storage**: CSV-based data persistence
- **Export**: PDF/HTML generation

## Note for Hugging Face Spaces

This app includes location detection features. In Hugging Face Spaces environment:
- IP-based location detection works normally
- Browser geolocation may have limitations
- Users can continue without precise location if needed

## Local Development

```bash
pip install -r requirements.txt
streamlit run app.py
```

## GitHub Repository

[https://github.com/jimmyjohn3702/swayamSites/](https://github.com/jimmyjohn3702/swayamSites/)
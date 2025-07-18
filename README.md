# 🚀 Swayam Sites - AI Portfolio Builder

A modern, multi-page Streamlit application that creates stunning portfolios using AI-powered content generation with support for Indian regional languages.

## ✨ Features

- **🎨 Multiple Templates**: Resume, Portfolio, and Poetry templates
- **🤖 AI-Powered Content**: Auto-generate professional content using OpenRouter API
- **🌍 Multi-language Support**: Support for Hindi, Tamil, Telugu, Bengali, and more
- **📱 Responsive Design**: Modern UI with animations and sleek design
- **📄 Export Options**: Download as PDF, HTML, or JSON
- **🔄 Real-time Preview**: See your portfolio as you build it
- **💾 Data Persistence**: Save and load your progress

## 🚀 Quick Start

### Option 1: Automated Setup
```bash
python setup.py
```

### Option 2: Manual Setup

1. **Install Dependencies**
```bash
pip install -r requirements.txt
```

2. **Run the Application**
```bash
streamlit run app.py
```

3. **Open in Browser**
The app will automatically open at `http://localhost:8501`

## 📁 Project Structure

```
swayam-sites/
├── app.py                 # Main Streamlit application
├── requirements.txt       # Python dependencies
├── setup.py              # Automated setup script
├── README.md             # This file
├── pages/                # Multi-page modules
│   ├── __init__.py
│   ├── template_selector.py    # Template selection page
│   ├── user_input.py          # User details input page
│   ├── auto_generation.py     # AI content generation page
│   └── preview_pdf.py         # Preview and export page
└── utils/                # Utility functions
    ├── __init__.py
    └── storage.py        # Data storage and geolocation utilities
```

## 🎯 How to Use

### Step 1: Select Template
- Choose from Resume, Portfolio, or Poetry templates
- Each template has unique styling and content structure

### Step 2: Enter Details
- Fill in personal information
- Add professional experience and education
- Include skills and projects
- Set language and design preferences

### Step 3: Generate Content
- Use AI to auto-generate professional content
- Customize with your own prompts
- Translate content to regional languages

### Step 4: Preview & Export
- Review your portfolio in real-time
- Choose from multiple themes and layouts
- Export as PDF, HTML, or JSON

## 🔧 Configuration

### API Setup (Optional)
For live AI content generation, add your OpenRouter API key:
1. Get an API key from [OpenRouter](https://openrouter.ai/)
2. Enter it in the AI Generation page
3. Without an API key, the app uses demo content

### Language Support
Supported languages:
- English (default)
- Hindi (हिंदी)
- Tamil (தமிழ்)
- Telugu (తెలుగు)
- Bengali (বাংলা)
- Marathi (मराठी)
- Gujarati (ગુજરાતી)
- Kannada (ಕನ್ನಡ)
- Malayalam (മലയാളം)
- Punjabi (ਪੰਜਾਬੀ)

## 🎨 Themes

Available color themes:
- **Professional Blue**: Corporate and trustworthy
- **Creative Purple**: Artistic and innovative
- **Modern Green**: Fresh and sustainable
- **Elegant Black**: Sophisticated and minimal
- **Warm Orange**: Energetic and friendly

## 📊 Features in Detail

### Template Selector
- Interactive template cards with animations
- Lottie animations for visual appeal
- Template preview and descriptions

### User Input
- Tabbed interface for organized data entry
- Form validation and error handling
- Progress tracking and data persistence

### AI Generation
- Multiple content types (summaries, skills, objectives)
- Custom prompt support
- Real-time translation capabilities
- Content editing and refinement

### Preview & Export
- Live preview with theme switching
- Multiple export formats
- Portfolio statistics and completion tracking
- Download buttons for all formats

## 🛠️ Technical Details

### Built With
- **Streamlit**: Web application framework
- **Pandas**: Data manipulation and storage
- **Geopy**: Geolocation services
- **Requests**: API communication
- **Plotly**: Interactive visualizations
- **Streamlit-Lottie**: Animations
- **Streamlit-Option-Menu**: Enhanced navigation

### Architecture
- Modular page-based structure
- Session state management for data persistence
- Utility modules for reusable functions
- CSS styling for modern UI/UX

## 🔒 Privacy & Security

- All data is processed locally
- No personal information is sent to external services (except for AI generation if API key is provided)
- CSV and JSON exports for data portability
- No user tracking or analytics

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📝 License

This project is open source and available under the MIT License.

## 🆘 Support

If you encounter any issues:
1. Check the console for error messages
2. Ensure all dependencies are installed
3. Verify Python version (3.7+ required)
4. Check internet connection for animations and translations

## 🎉 Acknowledgments

- Streamlit team for the amazing framework
- Lottie Files for beautiful animations
- OpenRouter for AI API services
- Google Translate for language support

---

**Made with ❤️ for the developer community**

*Create stunning portfolios in minutes, not hours!*
import streamlit as st
from pages.preview_pdf import app

# Set page config
st.set_page_config(
    page_title="Preview & PDF - Swayam Sites",
    page_icon="📄",
    layout="wide"
)

# Check if user is logged in
if 'logged_in' not in st.session_state or not st.session_state['logged_in']:
    st.warning("⚠️ Please login first!")
    st.markdown("[👈 Go to Login Page](./)")
    st.stop()

# Run the preview PDF app
app()
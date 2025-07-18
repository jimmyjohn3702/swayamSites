import streamlit as st
from pages.user_input import app

# Set page config
st.set_page_config(
    page_title="User Input - Swayam Sites",
    page_icon="📝",
    layout="wide"
)

# Check if user is logged in
if 'logged_in' not in st.session_state or not st.session_state['logged_in']:
    st.warning("⚠️ Please login first!")
    st.markdown("[👈 Go to Login Page](./)")
    st.stop()

# Run the user input app
app()
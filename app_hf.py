#!/usr/bin/env python3
"""
Hugging Face Spaces compatible version of Swayam Sites
"""

import streamlit as st
import sys
import os

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import the main app
from app import main

if __name__ == "__main__":
    main()
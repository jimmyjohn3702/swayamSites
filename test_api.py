#!/usr/bin/env python3
"""
Test script for OpenRouter API integration
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from utils.api_integration import test_api_connection, get_ai_content

def main():
    print("🧪 Testing Swayam Sites API Integration")
    print("=" * 50)
    
    # Test API connection
    print("1. Testing API Connection...")
    result = test_api_connection()
    
    if result["status"] == "success":
        print("✅ API Connection: SUCCESS")
        print(f"   Model Used: {result['model']}")
        print(f"   Response: {result['message'][:100]}...")
    else:
        print("❌ API Connection: FAILED")
        print(f"   Error: {result['message']}")
    
    print("\n" + "-" * 50)
    
    # Test content generation for different tasks
    test_cases = [
        ("resume", "Write a professional summary for a software developer with 3 years of experience."),
        ("portfolio", "Create an engaging project description for an e-commerce website."),
        ("poetry", "Write a short poem about technology and human connection.")
    ]
    
    for i, (task_type, prompt) in enumerate(test_cases, 2):
        print(f"{i}. Testing {task_type.title()} Content Generation...")
        
        try:
            content = get_ai_content(prompt, task_type, max_tokens=200)
            print(f"✅ {task_type.title()} Generation: SUCCESS")
            print(f"   Content Preview: {content[:150]}...")
        except Exception as e:
            print(f"❌ {task_type.title()} Generation: FAILED")
            print(f"   Error: {str(e)}")
        
        print()
    
    print("=" * 50)
    print("🎉 API Testing Complete!")

if __name__ == "__main__":
    main()
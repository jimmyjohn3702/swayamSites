#!/usr/bin/env python3
"""
Swayam Sites - AI Portfolio Builder Setup Script
"""

import subprocess
import sys
import os

def install_requirements():
    """Install required packages"""
    print("🚀 Installing required packages...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ All packages installed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error installing packages: {e}")
        return False

def create_directories():
    """Create necessary directories"""
    directories = ["data", "exports", "backups"]
    
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory)
            print(f"📁 Created directory: {directory}")

def run_app():
    """Run the Streamlit application"""
    print("🎉 Starting Swayam Sites...")
    try:
        subprocess.run([sys.executable, "-m", "streamlit", "run", "app.py"])
    except KeyboardInterrupt:
        print("\n👋 Thanks for using Swayam Sites!")
    except Exception as e:
        print(f"❌ Error running app: {e}")

def main():
    print("=" * 50)
    print("🚀 SWAYAM SITES - AI Portfolio Builder")
    print("=" * 50)
    
    # Check Python version
    if sys.version_info < (3, 7):
        print("❌ Python 3.7 or higher is required!")
        sys.exit(1)
    
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor} detected")
    
    # Install requirements
    if not install_requirements():
        print("❌ Setup failed. Please check the error messages above.")
        sys.exit(1)
    
    # Create directories
    create_directories()
    
    print("\n" + "=" * 50)
    print("✅ Setup completed successfully!")
    print("🎯 Ready to create amazing portfolios!")
    print("=" * 50)
    
    # Ask user if they want to run the app
    response = input("\n🚀 Would you like to start the application now? (y/n): ").lower().strip()
    
    if response in ['y', 'yes']:
        run_app()
    else:
        print("\n📝 To start the application later, run:")
        print("   streamlit run app.py")
        print("\n👋 Happy portfolio building!")

if __name__ == "__main__":
    main()
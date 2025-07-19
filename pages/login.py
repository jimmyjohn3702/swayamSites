import streamlit as st
import pandas as pd
import hashlib
import os
from datetime import datetime
import json
import requests
from utils.storage import get_user_location_from_ip, get_geolocation

def hash_password(password):
    """Hash password using SHA256"""
    return hashlib.sha256(password.encode()).hexdigest()

def save_user_to_db(username, email, password, location_data=None):
    """Save user to CSV database"""
    user_data = {
        'username': username,
        'email': email,
        'password_hash': hash_password(password),
        'created_at': datetime.now().isoformat(),
        'last_login': datetime.now().isoformat(),
        'latitude': location_data.get('latitude', '') if location_data else '',
        'longitude': location_data.get('longitude', '') if location_data else '',
        'city': location_data.get('city', '') if location_data else '',
        'country': location_data.get('country', '') if location_data else '',
        'ip_address': location_data.get('ip_address', '') if location_data else ''
    }
    
    # Create users database if it doesn't exist
    users_file = 'users_database.csv'
    
    if os.path.exists(users_file):
        df = pd.read_csv(users_file)
        # Check if user already exists
        if username in df['username'].values or email in df['email'].values:
            return False, "User already exists!"
        
        # Add new user
        new_df = pd.DataFrame([user_data])
        df = pd.concat([df, new_df], ignore_index=True)
    else:
        df = pd.DataFrame([user_data])
    
    df.to_csv(users_file, index=False)
    return True, "User registered successfully!"

def authenticate_user(username, password):
    """Authenticate user login"""
    users_file = 'users_database.csv'
    
    if not os.path.exists(users_file):
        return False, "No users registered yet!"
    
    df = pd.read_csv(users_file)
    user_row = df[df['username'] == username]
    
    if user_row.empty:
        return False, "Username not found!"
    
    stored_hash = user_row.iloc[0]['password_hash']
    if hash_password(password) == stored_hash:
        # Update last login
        df.loc[df['username'] == username, 'last_login'] = datetime.now().isoformat()
        df.to_csv(users_file, index=False)
        return True, "Login successful!"
    else:
        return False, "Invalid password!"

def save_user_session_data(username, session_data):
    """Save user's portfolio session data"""
    session_file = f'user_sessions/{username}_session.json'
    
    # Create directory if it doesn't exist
    os.makedirs('user_sessions', exist_ok=True)
    
    # Add timestamp to session data
    session_data['last_updated'] = datetime.now().isoformat()
    session_data['username'] = username
    
    with open(session_file, 'w', encoding='utf-8') as f:
        json.dump(session_data, f, indent=2, ensure_ascii=False)

def load_user_session_data(username):
    """Load user's portfolio session data"""
    session_file = f'user_sessions/{username}_session.json'
    
    if os.path.exists(session_file):
        with open(session_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    return None

def get_location_data():
    """Get user location data using multiple methods"""
    location_data = {}
    
    try:
        # Method 1: Get location from IP address (no API key required)
        ip_location = get_user_location_from_ip()
        if ip_location:
            location_data.update(ip_location)
            st.success(f"📍 Location detected: {ip_location.get('city', 'Unknown')}, {ip_location.get('country', 'Unknown')}")
        
        # Method 2: Browser geolocation (requires user permission)
        st.markdown("### 📍 Location Permission")
        st.info("We'd like to access your location to provide personalized services and analytics.")
        
        # JavaScript for browser geolocation
        location_js = """
        <script>
        function getLocation() {
            if (navigator.geolocation) {
                navigator.geolocation.getCurrentPosition(
                    function(position) {
                        const lat = position.coords.latitude;
                        const lon = position.coords.longitude;
                        const accuracy = position.coords.accuracy;
                        
                        // Store in session storage
                        sessionStorage.setItem('user_latitude', lat);
                        sessionStorage.setItem('user_longitude', lon);
                        sessionStorage.setItem('user_accuracy', accuracy);
                        
                        // Update the page
                        document.getElementById('location-status').innerHTML = 
                            '✅ Location captured: ' + lat.toFixed(6) + ', ' + lon.toFixed(6) + 
                            ' (Accuracy: ' + Math.round(accuracy) + 'm)';
                        document.getElementById('location-button').style.display = 'none';
                    },
                    function(error) {
                        let errorMsg = '';
                        switch(error.code) {
                            case error.PERMISSION_DENIED:
                                errorMsg = "❌ Location access denied by user.";
                                break;
                            case error.POSITION_UNAVAILABLE:
                                errorMsg = "❌ Location information is unavailable.";
                                break;
                            case error.TIMEOUT:
                                errorMsg = "❌ Location request timed out.";
                                break;
                            default:
                                errorMsg = "❌ An unknown error occurred.";
                                break;
                        }
                        document.getElementById('location-status').innerHTML = errorMsg;
                    },
                    {
                        enableHighAccuracy: true,
                        timeout: 10000,
                        maximumAge: 300000
                    }
                );
            } else {
                document.getElementById('location-status').innerHTML = 
                    "❌ Geolocation is not supported by this browser.";
            }
        }
        </script>
        
        <div id="location-status" style="margin: 10px 0; padding: 10px; background: #f0f2f6; border-radius: 5px;">
            📍 Click the button below to share your location
        </div>
        
        <button id="location-button" onclick="getLocation()" 
                style="background: linear-gradient(45deg, #667eea, #764ba2); 
                       color: white; border: none; padding: 10px 20px; 
                       border-radius: 25px; cursor: pointer; margin: 10px 0;">
            📍 Share My Location
        </button>
        """
        
        st.markdown(location_js, unsafe_allow_html=True)
        
        return location_data
        
    except Exception as e:
        st.warning(f"Could not get location data: {str(e)}")
        return location_data

def update_user_location(username, location_data):
    """Update user's location data in the database"""
    users_file = 'users_database.csv'
    
    if os.path.exists(users_file):
        df = pd.read_csv(users_file)
        
        # Update location data for the user
        mask = df['username'] == username
        if mask.any():
            for key, value in location_data.items():
                if key in df.columns:
                    df.loc[mask, key] = value
                else:
                    df[key] = ''
                    df.loc[mask, key] = value
            
            df.to_csv(users_file, index=False)
            return True
    return False

def app():
    st.markdown("## 🔐 Welcome to Swayam Sites")
    st.markdown("Please login or register to create your AI-powered portfolio")
    
    # Check if user just granted location permission (after page reload)
    st.markdown("""
    <script>
    // Check if location was granted and complete login
    if (sessionStorage.getItem('location_granted') === 'true') {
        // Get the stored location data
        const lat = sessionStorage.getItem('user_latitude');
        const lon = sessionStorage.getItem('user_longitude');
        const accuracy = sessionStorage.getItem('user_accuracy');
        
        if (lat && lon) {
            // Clear the session storage
            sessionStorage.removeItem('location_granted');
            sessionStorage.removeItem('user_latitude');
            sessionStorage.removeItem('user_longitude');
            sessionStorage.removeItem('user_accuracy');
            sessionStorage.removeItem('location_timestamp');
            
            // Set a flag to complete login
            sessionStorage.setItem('complete_login_with_location', 'true');
            sessionStorage.setItem('precise_lat', lat);
            sessionStorage.setItem('precise_lon', lon);
            sessionStorage.setItem('precise_accuracy', accuracy);
        }
    }
    </script>
    """, unsafe_allow_html=True)
    
    # Create tabs for login and register
    tab1, tab2 = st.tabs(["🔑 Login", "📝 Register"])
    
    with tab1:
        st.markdown("### 🔑 Login to Your Account")
        
        with st.form("login_form"):
            username = st.text_input("Username", placeholder="Enter your username")
            password = st.text_input("Password", type="password", placeholder="Enter your password")
            
            col1, col2 = st.columns([1, 2])
            with col1:
                login_button = st.form_submit_button("🚀 Login", use_container_width=True)
            
            if login_button:
                if username and password:
                    success, message = authenticate_user(username, password)
                    
                    if success:
                        st.success(message)
                        
                        # MANDATORY Location Permission Step
                        st.markdown("---")
                        st.markdown("### 📍 Location Permission Required")
                        st.warning("⚠️ **Location access is required to complete login.** Please grant location permission to continue.")
                        
                        # Get IP-based location (automatic)
                        with st.spinner("🌐 Getting your location..."):
                            location_data = get_user_location_from_ip()
                            
                        if location_data and location_data.get('city') != 'Unknown':
                            st.success(f"📍 Location detected: {location_data.get('city')}, {location_data.get('country')}")
                            
                            # Update user location in database
                            update_user_location(username, location_data)
                            
                            # Complete login automatically if IP location is successful
                            st.session_state['logged_in'] = True
                            st.session_state['username'] = username
                            
                            # Load user's previous session data if exists
                            session_data = load_user_session_data(username)
                            if session_data:
                                for key, value in session_data.items():
                                    if key not in ['last_updated', 'username']:
                                        st.session_state[key] = value
                                st.info("📂 Previous session restored!")
                            
                            st.success("🎉 Login completed successfully!")
                            st.balloons()
                            
                            # Auto-redirect
                            st.markdown("### ✅ Redirecting to Dashboard...")
                            st.markdown("""
                            <script>
                            setTimeout(function() {
                                window.location.reload();
                            }, 2000);
                            </script>
                            """, unsafe_allow_html=True)
                            
                        else:
                            # For Hugging Face Spaces - allow login without precise location
                            st.warning("📍 Could not detect location automatically.")
                            st.info("💡 **For Hugging Face Spaces**: Location detection may be limited. You can continue without precise location.")
                            
                            # Provide option to continue without location or try browser location
                            col1, col2 = st.columns(2)
                            
                            with col1:
                                if st.button("✅ Continue Without Location", type="primary", use_container_width=True):
                                    # Complete login without precise location
                                    st.session_state['logged_in'] = True
                                    st.session_state['username'] = username
                                    
                                    # Use default location data
                                    default_location = {
                                        "city": "Unknown",
                                        "country": "Unknown", 
                                        "latitude": 0,
                                        "longitude": 0,
                                        "ip_address": "Unknown"
                                    }
                                    update_user_location(username, default_location)
                                    
                                    # Load user's previous session data if exists
                                    session_data = load_user_session_data(username)
                                    if session_data:
                                        for key, value in session_data.items():
                                            if key not in ['last_updated', 'username']:
                                                st.session_state[key] = value
                                        st.info("📂 Previous session restored!")
                                    
                                    st.success("🎉 Login completed successfully!")
                                    st.balloons()
                                    
                                    # Auto-redirect
                                    st.markdown("### ✅ Redirecting to Dashboard...")
                                    st.markdown("""
                                    <script>
                                    setTimeout(function() {
                                        window.location.reload();
                                    }, 2000);
                                    </script>
                                    """, unsafe_allow_html=True)
                            
                            with col2:
                                if st.button("📍 Try Browser Location", use_container_width=True):
                                    st.info("🔄 Attempting browser location detection...")
                            
                            # Browser geolocation request with native popup (fallback)
                            st.markdown("""
                            <div style="background: linear-gradient(135deg, #667eea, #764ba2); padding: 20px; border-radius: 15px; margin: 20px 0;">
                                <h4 style="color: white; margin: 0 0 10px 0;">🔒 Complete Your Login</h4>
                                <p style="color: white; margin: 0 0 15px 0;">Click the button below to grant location permission. Your browser will show a popup asking for location access.</p>
                                <div id="location-status" style="background: rgba(255,255,255,0.2); padding: 10px; border-radius: 8px; margin: 10px 0; color: white;">
                                    📍 Ready to request location permission
                                </div>
                                <button id="location-button" onclick="requestLocationPermission()" 
                                        style="background: white; color: #667eea; border: none; padding: 15px 30px; 
                                               border-radius: 25px; cursor: pointer; font-weight: bold; font-size: 16px;
                                               box-shadow: 0 4px 15px rgba(0,0,0,0.2); transition: all 0.3s ease;">
                                    📍 Allow Location Access
                                </button>
                                <div style="margin-top: 15px; font-size: 14px; color: rgba(255,255,255,0.8);">
                                    ⚠️ Please click "Allow" when your browser asks for location permission
                                </div>
                            </div>
                            
                            <script>
                            let locationRequested = false;
                            
                            function requestLocationPermission() {
                                if (locationRequested) {
                                    return; // Prevent multiple requests
                                }
                                
                                locationRequested = true;
                                
                                // Check if geolocation is supported
                                if (!navigator.geolocation) {
                                    document.getElementById('location-status').innerHTML = 
                                        '❌ Geolocation is not supported by your browser.<br>Please use a modern browser like Chrome, Firefox, or Safari.';
                                    return;
                                }
                                
                                // Update UI to show we're requesting permission
                                document.getElementById('location-status').innerHTML = 
                                    '⏳ Requesting location permission...<br>📱 Please look for the browser popup and click "Allow"';
                                document.getElementById('location-button').disabled = true;
                                document.getElementById('location-button').innerHTML = '⏳ Waiting for permission...';
                                document.getElementById('location-button').style.opacity = '0.6';
                                
                                // Request geolocation with high accuracy
                                navigator.geolocation.getCurrentPosition(
                                    // Success callback
                                    function(position) {
                                        const lat = position.coords.latitude;
                                        const lon = position.coords.longitude;
                                        const accuracy = position.coords.accuracy;
                                        const timestamp = new Date().toLocaleString();
                                        
                                        // Store location data in sessionStorage
                                        sessionStorage.setItem('user_latitude', lat.toString());
                                        sessionStorage.setItem('user_longitude', lon.toString());
                                        sessionStorage.setItem('user_accuracy', accuracy.toString());
                                        sessionStorage.setItem('location_timestamp', timestamp);
                                        sessionStorage.setItem('location_granted', 'true');
                                        
                                        // Update UI with success message
                                        document.getElementById('location-status').innerHTML = 
                                            '✅ Location permission granted successfully!<br>' +
                                            '📍 Coordinates: ' + lat.toFixed(6) + ', ' + lon.toFixed(6) + '<br>' +
                                            '🎯 Accuracy: ±' + Math.round(accuracy) + ' meters<br>' +
                                            '⏰ Captured at: ' + timestamp + '<br>' +
                                            '🎉 Completing login process...';
                                        
                                        document.getElementById('location-button').style.display = 'none';
                                        
                                        // Show success animation
                                        document.getElementById('location-status').style.background = 'rgba(0,255,0,0.3)';
                                        document.getElementById('location-status').style.border = '2px solid rgba(0,255,0,0.5)';
                                        
                                        // Complete login after a short delay
                                        setTimeout(function() {
                                            // Trigger page reload to complete login
                                            window.location.reload();
                                        }, 3000);
                                    },
                                    
                                    // Error callback
                                    function(error) {
                                        locationRequested = false; // Allow retry
                                        
                                        let errorMsg = '';
                                        let errorColor = 'rgba(255,0,0,0.3)';
                                        
                                        switch(error.code) {
                                            case error.PERMISSION_DENIED:
                                                errorMsg = '❌ Location permission denied!<br>' +
                                                          '⚠️ You clicked "Block" or "Deny" in the browser popup.<br>' +
                                                          '🔧 To fix this:<br>' +
                                                          '1. Click the location icon in your browser address bar<br>' +
                                                          '2. Select "Allow" for location access<br>' +
                                                          '3. Refresh this page and try again';
                                                break;
                                            case error.POSITION_UNAVAILABLE:
                                                errorMsg = '❌ Location information is unavailable.<br>' +
                                                          '📡 Your device cannot determine your location.<br>' +
                                                          '🔧 Please check your device location settings.';
                                                break;
                                            case error.TIMEOUT:
                                                errorMsg = '⏰ Location request timed out.<br>' +
                                                          '🔧 Please try again or check your internet connection.';
                                                break;
                                            default:
                                                errorMsg = '❌ An unknown error occurred while getting your location.<br>' +
                                                          '🔧 Please try again or contact support.';
                                                break;
                                        }
                                        
                                        // Update UI with error message
                                        document.getElementById('location-status').innerHTML = errorMsg;
                                        document.getElementById('location-status').style.background = errorColor;
                                        document.getElementById('location-status').style.border = '2px solid rgba(255,0,0,0.5)';
                                        
                                        // Re-enable button for retry
                                        document.getElementById('location-button').disabled = false;
                                        document.getElementById('location-button').innerHTML = '🔄 Try Again';
                                        document.getElementById('location-button').style.opacity = '1';
                                    },
                                    
                                    // Options for high accuracy
                                    {
                                        enableHighAccuracy: true,    // Use GPS if available
                                        timeout: 30000,             // Wait up to 30 seconds
                                        maximumAge: 0               // Don't use cached location
                                    }
                                );
                            }
                            
                            // Auto-trigger location request when page loads (optional)
                            // Uncomment the line below if you want automatic popup
                            // setTimeout(requestLocationPermission, 1000);
                            </script>
                            """, unsafe_allow_html=True)
                            
                            # Handle the case where user returns after granting location
                            if st.button("🔄 Refresh After Location Grant", help="Click this if you granted location permission"):
                                st.rerun()
                    else:
                        st.error(message)
                else:
                    st.error("Please fill in all fields!")
    
    with tab2:
        st.markdown("### 📝 Create New Account")
        
        with st.form("register_form"):
            new_username = st.text_input("Choose Username", placeholder="Enter a unique username")
            new_email = st.text_input("Email Address", placeholder="your.email@example.com")
            new_password = st.text_input("Create Password", type="password", placeholder="Create a strong password")
            confirm_password = st.text_input("Confirm Password", type="password", placeholder="Confirm your password")
            
            # Terms and conditions
            agree_terms = st.checkbox("I agree to the Terms of Service and Privacy Policy")
            
            col1, col2 = st.columns([1, 2])
            with col1:
                register_button = st.form_submit_button("✨ Register", use_container_width=True)
            
            if register_button:
                if new_username and new_email and new_password and confirm_password:
                    if new_password != confirm_password:
                        st.error("Passwords don't match!")
                    elif len(new_password) < 6:
                        st.error("Password must be at least 6 characters long!")
                    elif not agree_terms:
                        st.error("Please agree to the Terms of Service!")
                    else:
                        # Get location data during registration
                        st.markdown("---")
                        st.markdown("### 📍 Location Services")
                        st.info("We'd like to capture your location for analytics and personalized services.")
                        
                        # Get IP-based location (automatic)
                        location_data = get_user_location_from_ip()
                        if location_data:
                            st.success(f"📍 Location detected: {location_data.get('city', 'Unknown')}, {location_data.get('country', 'Unknown')}")
                        
                        success, message = save_user_to_db(new_username, new_email, new_password, location_data)
                        
                        if success:
                            st.success(message)
                            st.info("🎉 Registration successful! Please login with your credentials.")
                            
                            # Show location capture option
                            if st.button("📍 Share Precise Location (Optional)", help="Click to share your precise location for better services"):
                                st.markdown("""
                                <script>
                                if (navigator.geolocation) {
                                    navigator.geolocation.getCurrentPosition(
                                        function(position) {
                                            alert('Location captured successfully! You can now login.');
                                        },
                                        function(error) {
                                            alert('Location access denied or unavailable. You can still use the app!');
                                        }
                                    );
                                }
                                </script>
                                """, unsafe_allow_html=True)
                            
                            st.balloons()
                        else:
                            st.error(message)
                else:
                    st.error("Please fill in all fields!")
    
    # Demo section
    st.markdown("---")
    st.markdown("### 🎯 What You'll Get")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        **🎨 Beautiful Templates**
        - Professional Resume
        - Creative Portfolio  
        - Poetry Collection
        """)
    
    with col2:
        st.markdown("""
        **🤖 AI-Powered Content**
        - Auto-generated text
        - Multi-language support
        - Smart recommendations
        """)
    
    with col3:
        st.markdown("""
        **📄 Export Options**
        - PDF Download
        - HTML Export
        - Data Backup
        """)
    
    # Footer
    st.markdown("---")
    st.markdown(
        """
        <div style="text-align: center; color: #666; font-size: 0.9rem;">
            🔒 Your data is secure and stored locally<br>
            Made with ❤️ using Streamlit & AI
        </div>
        """,
        unsafe_allow_html=True
    )
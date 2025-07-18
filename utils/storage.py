import pandas as pd
import json
import os
from datetime import datetime
from geopy.geocoders import Nominatim
import streamlit as st

def save_user_details(details: dict, filename="user_details.csv"):
    """Save user details to CSV file"""
    try:
        df = pd.DataFrame([details])
        if os.path.exists(filename):
            # Append to existing file
            existing_df = pd.read_csv(filename)
            df = pd.concat([existing_df, df], ignore_index=True)
        df.to_csv(filename, index=False)
        return True
    except Exception as e:
        st.error(f"Error saving user details: {str(e)}")
        return False

def load_user_details(filename="user_details.csv"):
    """Load user details from CSV file"""
    try:
        if os.path.exists(filename):
            df = pd.read_csv(filename)
            return df.to_dict('records')
        return []
    except Exception as e:
        st.error(f"Error loading user details: {str(e)}")
        return []

def get_geolocation(address="India"):
    """Get geolocation coordinates from address"""
    try:
        geolocator = Nominatim(user_agent="swayam_sites_app")
        location = geolocator.geocode(address)
        if location:
            return {
                "latitude": location.latitude,
                "longitude": location.longitude,
                "address": location.address
            }
        return {}
    except Exception as e:
        st.error(f"Error getting geolocation: {str(e)}")
        return {}

def save_generated_content(content: dict, filename="generated_content.json"):
    """Save AI generated content to JSON file"""
    try:
        content['timestamp'] = datetime.now().isoformat()
        
        # Load existing content if file exists
        existing_content = []
        if os.path.exists(filename):
            with open(filename, 'r', encoding='utf-8') as f:
                existing_content = json.load(f)
        
        # Add new content
        existing_content.append(content)
        
        # Save updated content
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(existing_content, f, indent=2, ensure_ascii=False)
        
        return True
    except Exception as e:
        st.error(f"Error saving generated content: {str(e)}")
        return False

def load_generated_content(filename="generated_content.json"):
    """Load AI generated content from JSON file"""
    try:
        if os.path.exists(filename):
            with open(filename, 'r', encoding='utf-8') as f:
                return json.load(f)
        return []
    except Exception as e:
        st.error(f"Error loading generated content: {str(e)}")
        return []

def create_backup(data: dict, backup_type="user_data"):
    """Create backup of important data"""
    try:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"backup_{backup_type}_{timestamp}.json"
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        return filename
    except Exception as e:
        st.error(f"Error creating backup: {str(e)}")
        return None

def get_user_location_from_ip():
    """Get user location from IP address with multiple fallback APIs"""
    
    # List of free IP geolocation APIs to try
    apis = [
        {
            "name": "ipapi.co",
            "url": "https://ipapi.co/json/",
            "parser": lambda data: {
                "city": data.get("city", "Unknown"),
                "region": data.get("region", "Unknown"),
                "country": data.get("country_name", "Unknown"),
                "latitude": data.get("latitude", 0),
                "longitude": data.get("longitude", 0),
                "ip_address": data.get("ip", "Unknown")
            }
        },
        {
            "name": "ip-api.com",
            "url": "http://ip-api.com/json/",
            "parser": lambda data: {
                "city": data.get("city", "Unknown"),
                "region": data.get("regionName", "Unknown"),
                "country": data.get("country", "Unknown"),
                "latitude": data.get("lat", 0),
                "longitude": data.get("lon", 0),
                "ip_address": data.get("query", "Unknown")
            }
        },
        {
            "name": "ipinfo.io",
            "url": "https://ipinfo.io/json",
            "parser": lambda data: {
                "city": data.get("city", "Unknown"),
                "region": data.get("region", "Unknown"),
                "country": data.get("country", "Unknown"),
                "latitude": float(data.get("loc", "0,0").split(",")[0]) if data.get("loc") else 0,
                "longitude": float(data.get("loc", "0,0").split(",")[1]) if data.get("loc") else 0,
                "ip_address": data.get("ip", "Unknown")
            }
        }
    ]
    
    for api in apis:
        try:
            print(f"Trying {api['name']}...")  # Debug log
            
            import requests
            response = requests.get(api["url"], timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                
                # Check if we got valid data
                if data and not data.get("error"):
                    location_data = api["parser"](data)
                    
                    # Validate that we got meaningful data
                    if (location_data.get("city") and location_data.get("city") != "Unknown" and
                        location_data.get("country") and location_data.get("country") != "Unknown"):
                        
                        print(f"✅ Successfully got location from {api['name']}")  # Debug log
                        return location_data
                    
        except requests.exceptions.Timeout:
            print(f"⏰ Timeout for {api['name']}")
            continue
        except requests.exceptions.RequestException as e:
            print(f"🌐 Network error for {api['name']}: {str(e)}")
            continue
        except Exception as e:
            print(f"❌ Error with {api['name']}: {str(e)}")
            continue
    
    # If all APIs fail, return a default location
    print("⚠️ All location APIs failed, using default location")
    return {
        "city": "Unknown",
        "region": "Unknown", 
        "country": "Unknown",
        "latitude": 0,
        "longitude": 0,
        "ip_address": "Unknown",
        "error": "Could not determine location"
    }
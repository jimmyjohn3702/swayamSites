import streamlit as st
import pandas as pd
import os
from datetime import datetime
import plotly.express as px
import plotly.graph_objects as go

def load_user_data(username):
    """Load user data from database"""
    users_file = 'users_database.csv'
    
    if os.path.exists(users_file):
        df = pd.read_csv(users_file)
        user_data = df[df['username'] == username]
        if not user_data.empty:
            return user_data.iloc[0].to_dict()
    return None

def get_all_users_location_data():
    """Get location data for all users for analytics"""
    users_file = 'users_database.csv'
    
    if os.path.exists(users_file):
        df = pd.read_csv(users_file)
        # Filter users with location data
        location_df = df[df['latitude'].notna() & df['longitude'].notna() & 
                        (df['latitude'] != '') & (df['longitude'] != '')]
        return location_df
    return pd.DataFrame()

def app():
    if 'username' not in st.session_state:
        st.error("Please login first!")
        return
    
    username = st.session_state['username']
    st.markdown(f"## 👋 Welcome back, {username}!")
    
    # Load user data
    user_data = load_user_data(username)
    
    if not user_data:
        st.error("Could not load user data!")
        return
    
    # Create tabs for different sections
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Dashboard", "📍 Location Info", "👥 User Analytics", "⚙️ Settings"])
    
    with tab1:
        st.markdown("### 📊 Your Dashboard")
        
        # User stats
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                label="📅 Member Since",
                value=datetime.fromisoformat(user_data['created_at']).strftime("%b %Y")
            )
        
        with col2:
            st.metric(
                label="🔐 Last Login",
                value=datetime.fromisoformat(user_data['last_login']).strftime("%b %d")
            )
        
        with col3:
            location_status = "✅ Available" if user_data.get('latitude') and user_data.get('longitude') else "❌ Not Set"
            st.metric(
                label="📍 Location",
                value=location_status
            )
        
        with col4:
            # Count user sessions
            session_file = f'user_sessions/{username}_session.json'
            session_status = "✅ Active" if os.path.exists(session_file) else "❌ None"
            st.metric(
                label="💾 Sessions",
                value=session_status
            )
        
        # Recent activity
        st.markdown("### 📈 Recent Activity")
        
        activity_data = {
            "Activity": ["Account Created", "Last Login", "Location Updated", "Session Saved"],
            "Date": [
                user_data['created_at'],
                user_data['last_login'],
                user_data.get('last_login', user_data['created_at']),
                user_data.get('last_login', user_data['created_at'])
            ],
            "Status": ["✅ Completed", "✅ Completed", "✅ Completed", "✅ Completed"]
        }
        
        activity_df = pd.DataFrame(activity_data)
        st.dataframe(activity_df, use_container_width=True)
    
    with tab2:
        st.markdown("### 📍 Your Location Information")
        
        if user_data.get('latitude') and user_data.get('longitude'):
            # Display location details
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("#### 🌍 Location Details")
                st.info(f"**City:** {user_data.get('city', 'Unknown')}")
                st.info(f"**Country:** {user_data.get('country', 'Unknown')}")
                st.info(f"**Coordinates:** {user_data.get('latitude', 'N/A')}, {user_data.get('longitude', 'N/A')}")
                st.info(f"**IP Address:** {user_data.get('ip_address', 'N/A')}")
            
            with col2:
                st.markdown("#### 🗺️ Your Location on Map")
                
                # Create map
                try:
                    lat = float(user_data['latitude'])
                    lon = float(user_data['longitude'])
                    
                    # Create a map using plotly
                    fig = go.Figure(go.Scattermapbox(
                        lat=[lat],
                        lon=[lon],
                        mode='markers',
                        marker=dict(size=15, color='red'),
                        text=[f"{username}'s Location"],
                        hovertemplate="<b>%{text}</b><br>Lat: %{lat}<br>Lon: %{lon}<extra></extra>"
                    ))
                    
                    fig.update_layout(
                        mapbox=dict(
                            style="open-street-map",
                            center=dict(lat=lat, lon=lon),
                            zoom=10
                        ),
                        height=400,
                        margin=dict(l=0, r=0, t=0, b=0)
                    )
                    
                    st.plotly_chart(fig, use_container_width=True)
                    
                except (ValueError, TypeError):
                    st.error("Invalid location coordinates")
            
            # Location update option
            st.markdown("---")
            st.markdown("#### 🔄 Update Location")
            
            if st.button("📍 Update My Location", help="Click to update your current location"):
                st.markdown("""
                <script>
                if (navigator.geolocation) {
                    navigator.geolocation.getCurrentPosition(
                        function(position) {
                            alert('New location captured: ' + position.coords.latitude + ', ' + position.coords.longitude + '\\nPlease refresh the page to see updates.');
                        },
                        function(error) {
                            alert('Location access denied or unavailable');
                        }
                    );
                }
                </script>
                """, unsafe_allow_html=True)
        
        else:
            st.warning("📍 Location data not available")
            st.markdown("#### Enable Location Services")
            st.info("To enable location services, please click the button below to share your location.")
            
            if st.button("📍 Share My Location", help="Click to share your location"):
                st.markdown("""
                <script>
                if (navigator.geolocation) {
                    navigator.geolocation.getCurrentPosition(
                        function(position) {
                            alert('Location captured: ' + position.coords.latitude + ', ' + position.coords.longitude + '\\nPlease refresh the page to see your location.');
                        },
                        function(error) {
                            alert('Location access denied or unavailable');
                        }
                    );
                }
                </script>
                """, unsafe_allow_html=True)
    
    with tab3:
        st.markdown("### 👥 User Analytics")
        
        # Load all users location data
        all_users_df = get_all_users_location_data()
        
        if not all_users_df.empty:
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("#### 🌍 Users by Country")
                country_counts = all_users_df['country'].value_counts()
                
                if not country_counts.empty:
                    fig_pie = px.pie(
                        values=country_counts.values,
                        names=country_counts.index,
                        title="User Distribution by Country"
                    )
                    st.plotly_chart(fig_pie, use_container_width=True)
            
            with col2:
                st.markdown("#### 🏙️ Users by City")
                city_counts = all_users_df['city'].value_counts().head(10)
                
                if not city_counts.empty:
                    fig_bar = px.bar(
                        x=city_counts.values,
                        y=city_counts.index,
                        orientation='h',
                        title="Top 10 Cities"
                    )
                    fig_bar.update_layout(yaxis={'categoryorder':'total ascending'})
                    st.plotly_chart(fig_bar, use_container_width=True)
            
            # World map of all users
            st.markdown("#### 🗺️ Global User Map")
            
            try:
                # Convert coordinates to float
                all_users_df['lat_float'] = pd.to_numeric(all_users_df['latitude'], errors='coerce')
                all_users_df['lon_float'] = pd.to_numeric(all_users_df['longitude'], errors='coerce')
                
                # Remove invalid coordinates
                valid_coords = all_users_df.dropna(subset=['lat_float', 'lon_float'])
                
                if not valid_coords.empty:
                    fig_map = go.Figure(go.Scattermapbox(
                        lat=valid_coords['lat_float'],
                        lon=valid_coords['lon_float'],
                        mode='markers',
                        marker=dict(size=10, color='blue', opacity=0.7),
                        text=valid_coords['username'],
                        hovertemplate="<b>%{text}</b><br>%{customdata}<extra></extra>",
                        customdata=valid_coords['city'] + ', ' + valid_coords['country']
                    ))
                    
                    fig_map.update_layout(
                        mapbox=dict(
                            style="open-street-map",
                            center=dict(lat=valid_coords['lat_float'].mean(), 
                                      lon=valid_coords['lon_float'].mean()),
                            zoom=2
                        ),
                        height=500,
                        margin=dict(l=0, r=0, t=0, b=0)
                    )
                    
                    st.plotly_chart(fig_map, use_container_width=True)
                
            except Exception as e:
                st.error(f"Could not create map: {str(e)}")
            
            # Statistics
            st.markdown("#### 📊 Location Statistics")
            
            stats_col1, stats_col2, stats_col3 = st.columns(3)
            
            with stats_col1:
                st.metric("Total Users with Location", len(all_users_df))
            
            with stats_col2:
                st.metric("Countries Represented", all_users_df['country'].nunique())
            
            with stats_col3:
                st.metric("Cities Represented", all_users_df['city'].nunique())
        
        else:
            st.info("No location data available for analytics yet.")
    
    with tab4:
        st.markdown("### ⚙️ Account Settings")
        
        # Account information
        st.markdown("#### 👤 Account Information")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.text_input("Username", value=user_data['username'], disabled=True)
            st.text_input("Email", value=user_data['email'], disabled=True)
        
        with col2:
            st.text_input("Member Since", value=datetime.fromisoformat(user_data['created_at']).strftime("%B %d, %Y"), disabled=True)
            st.text_input("Last Login", value=datetime.fromisoformat(user_data['last_login']).strftime("%B %d, %Y at %I:%M %p"), disabled=True)
        
        # Privacy settings
        st.markdown("---")
        st.markdown("#### 🔒 Privacy Settings")
        
        location_sharing = st.checkbox("Share location data for analytics", value=True, help="Allow your location data to be used for user analytics")
        
        if st.button("💾 Save Privacy Settings"):
            st.success("Privacy settings saved!")
        
        # Data export
        st.markdown("---")
        st.markdown("#### 📤 Data Export")
        
        if st.button("📥 Download My Data"):
            # Create user data export
            export_data = {
                "user_info": user_data,
                "export_date": datetime.now().isoformat(),
                "data_type": "user_account_data"
            }
            
            import json
            json_data = json.dumps(export_data, indent=2, default=str)
            
            st.download_button(
                label="📥 Download JSON",
                data=json_data,
                file_name=f"{username}_data_export.json",
                mime="application/json"
            )
            
            st.success("✅ Data export ready for download!")
        
        # Account deletion
        st.markdown("---")
        st.markdown("#### ⚠️ Danger Zone")
        
        with st.expander("🗑️ Delete Account", expanded=False):
            st.warning("This action cannot be undone. All your data will be permanently deleted.")
            
            confirm_delete = st.text_input("Type 'DELETE' to confirm account deletion")
            
            if confirm_delete == "DELETE":
                if st.button("🗑️ Permanently Delete Account", type="primary"):
                    st.error("Account deletion feature is not implemented yet for safety reasons.")
            else:
                st.button("🗑️ Permanently Delete Account", disabled=True)
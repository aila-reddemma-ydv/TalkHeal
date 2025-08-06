"""
TalkHeal Profile Management Module

This module handles user profile functionality including:
- Profile creation and editing
- Profile picture upload and management
- User preferences (name, font size)
- Profile display in sidebar

Author: TalkHeal Team
Version: 1.0
"""

import streamlit as st
import base64
from datetime import datetime
from io import BytesIO
from PIL import Image


def initialize_profile_state():
    """Initialize profile data in session state if not exists"""
    if "user_profile" not in st.session_state:
        st.session_state.user_profile = {
            "name": "",
            "profile_picture": None,
            "join_date": datetime.now().strftime("%B %Y"),
            "font_size": "Medium"
        }


def get_greeting():
    """Get appropriate greeting based on current time"""
    current_hour = datetime.now().hour
    if current_hour < 12:
        return "Good morning"
    elif current_hour < 17:
        return "Good afternoon"
    else:
        return "Good evening"


def get_user_initials(name):
    """Generate user initials from name"""
    if name:
        return ''.join([word[0].upper() for word in name.split()[:2]])
    return "TH"


def create_default_avatar(initials, size=80):
    """Create a default avatar with user initials"""
    return st.markdown(f"""
    <div style="
        width: {size}px; 
        height: {size}px; 
        border-radius: 50%; 
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        display: flex; 
        align-items: center; 
        justify-content: center; 
        color: white; 
        font-weight: bold; 
        font-size: {size//4}px;
        margin-bottom: 10px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    ">
        {initials}
    </div>
    """, unsafe_allow_html=True)


def handle_profile_picture_upload(uploaded_file):
    """Handle profile picture upload and processing"""
    if uploaded_file is not None:
        try:
            # Process and resize image to medium size
            image = Image.open(uploaded_file)
            # Resize to medium size (200x200) while maintaining aspect ratio
            image.thumbnail((200, 200), Image.Resampling.LANCZOS)
            
            # Convert to base64 for storage
            buffered = BytesIO()
            image.save(buffered, format="PNG")
            img_str = base64.b64encode(buffered.getvalue()).decode()
            
            # Save to session state
            st.session_state.user_profile["profile_picture"] = f"data:image/png;base64,{img_str}"
            
            st.success("✅ Profile picture uploaded successfully!")
            return True
            
        except Exception as e:
            st.error("❌ Error uploading image. Please try a different file.")
            return False
    
    return False


def render_profile_header():
    """Render the profile header with picture and greeting"""
    profile_data = st.session_state.user_profile
    greeting = get_greeting()
    
    # Profile header section
    st.markdown("### 👤 Profile")
    
    # Profile picture and greeting
    col1, col2 = st.columns([1, 2])
    
    with col1:
        if profile_data["profile_picture"]:
            # Display uploaded profile picture with circular shape and medium size
            st.markdown(f"""
            <div style="
                width: 80px; 
                height: 80px; 
                border-radius: 50%; 
                overflow: hidden;
                background: #f0f0f0;
                display: flex;
                align-items: center;
                justify-content: center;
                margin-bottom: 10px;
                box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            ">
                <img src="{profile_data['profile_picture']}" 
                     style="width: 100%; height: 100%; object-fit: cover;" 
                     alt="Profile Picture"/>
            </div>
            """, unsafe_allow_html=True)
        else:
            # Default avatar with initials
            initials = get_user_initials(profile_data["name"])
            create_default_avatar(initials, 80)
    
    with col2:
        if profile_data["name"]:
            display_name = profile_data["name"].split()[0]
            st.markdown(f"**{greeting}, {display_name}!** 👋")
        else:
            st.markdown(f"**Welcome to TalkHeal!** 🌟")
        st.caption(f"Member since {profile_data['join_date']}")


def render_profile_settings():
    """Render the profile settings form"""
    profile_data = st.session_state.user_profile
    
    # Add CSS to fix the text input color issue
    st.markdown("""
    <style>
    /* Fix text input color to ensure it's visible */
    .stTextInput > div > div > input {
        color: #262730 !important;
        background-color: #ffffff !important;
    }
    
    /* For dark theme compatibility */
    [data-theme="dark"] .stTextInput > div > div > input {
        color: #fafafa !important;
        background-color: #262730 !important;
    }
    
    /* Ensure placeholder text is visible */
    .stTextInput > div > div > input::placeholder {
        color: #9ca3af !important;
        opacity: 0.7;
    }
    </style>
    """, unsafe_allow_html=True)
    
    with st.expander("⚙️ Profile Settings"):
        
        # Name input
        st.markdown("**Your Name**")
        new_name = st.text_input(
            "Enter your name",
            value=profile_data["name"],
            key="profile_name_input",
            placeholder="Enter your name",
            help="Enter your preferred name for personalized interactions"
        )
        
        # Profile picture upload
        st.markdown("**Profile Picture**")
        uploaded_file = st.file_uploader(
            "Upload a profile picture (Optional)",
            type=['png', 'jpg', 'jpeg'],
            key="profile_pic_upload",
            help="Drag and drop or click to upload. Supported formats: PNG, JPG, JPEG"
        )
        
        # Handle file upload
        handle_profile_picture_upload(uploaded_file)
        
        # Font size preference
        st.markdown("**Font Size**")
        font_size = st.selectbox(
            "Choose your preferred text size",
            ["Small", "Medium", "Large"],
            index=["Small", "Medium", "Large"].index(profile_data["font_size"]),
            key="font_size_selector",
            help="This will change the font size throughout the entire application"
        )
        
        # Action buttons row
        col_save, col_reset = st.columns(2)
        
        with col_save:
            # Save profile button
            if st.button("💾 Save Profile", key="save_profile", use_container_width=True, type="primary"):
                # Update profile data
                profile_data["name"] = new_name.strip()
                profile_data["font_size"] = font_size
                
                # Save to session state
                st.session_state.user_profile = profile_data
                
                # Apply font size globally (you can implement this in your main app)
                st.session_state.global_font_size = font_size
                
                # Success message
                st.success("🎉 Profile saved successfully!")
                st.balloons()
                
                # Rerun to update the display
                st.rerun()
        
        with col_reset:
            # Reset profile button
            if st.button("🔄 Reset All", key="reset_profile", use_container_width=True, type="secondary"):
                # Show confirmation dialog
                st.session_state.show_reset_confirmation = True
                st.rerun()
        
        # Reset confirmation dialog
        if st.session_state.get("show_reset_confirmation", False):
            st.warning("⚠️ Are you sure you want to reset all profile settings?")
            col_confirm, col_cancel = st.columns(2)
            
            with col_confirm:
                if st.button("✅ Yes, Reset", key="confirm_reset", use_container_width=True, type="primary"):
                    # Reset to default values
                    st.session_state.user_profile = {
                        "name": "",
                        "profile_picture": None,
                        "join_date": datetime.now().strftime("%B %Y"),
                        "font_size": "Medium"
                    }
                    # Reset global font size
                    st.session_state.global_font_size = "Medium"
                    st.session_state.show_reset_confirmation = False
                    st.success("🔄 Profile reset successfully!")
                    st.rerun()
            
            with col_cancel:
                if st.button("❌ Cancel", key="cancel_reset", use_container_width=True):
                    st.session_state.show_reset_confirmation = False
                    st.rerun()


def render_profile_stats():
    """Render simplified profile statistics"""
    profile_data = st.session_state.user_profile
    
    if profile_data["name"]:
        with st.expander("📊 Your TalkHeal Journey"):
            col1, col2 = st.columns(2)
            
            with col1:
                st.metric("Conversations", "0", help="Total chat sessions")
            
            with col2:
                st.metric("Days Active", "1", help="Days you've used TalkHeal")


def render_profile_section():
    """
    Main function to render the complete profile section
    This is the function that should be imported and called in sidebar
    """
    # Initialize profile state
    initialize_profile_state()
    
    # Render profile components
    render_profile_header()
    render_profile_settings()
    render_profile_stats()
    
    # Add separator
    st.markdown("---")


# Optional: Helper functions for other parts of the app
def get_user_name():
    """Get the current user's name"""
    if "user_profile" in st.session_state:
        return st.session_state.user_profile.get("name", "")
    return ""


def get_user_font_size():
    """Get the current user's preferred font size"""
    if "global_font_size" in st.session_state:
        return st.session_state.global_font_size
    elif "user_profile" in st.session_state:
        return st.session_state.user_profile.get("font_size", "Medium")
    return "Medium"


def apply_global_font_size():
    """
    Apply the user's font size preference globally across the application.
    Call this function in your main app to apply font size changes.
    """
    font_size = get_user_font_size()
    
    # Font size mappings
    font_sizes = {
        "Small": "14px",
        "Medium": "16px", 
        "Large": "18px"
    }
    
    selected_size = font_sizes.get(font_size, "16px")
    
    # Apply CSS to change font size globally
    st.markdown(f"""
    <style>
    .stApp {{
        font-size: {selected_size};
    }}
    .stMarkdown, .stText, p, div, span {{
        font-size: {selected_size} !important;
    }}
    .stSelectbox label, .stTextInput label, .stTextArea label {{
        font-size: {selected_size} !important;
    }}
    .stButton button {{
        font-size: {selected_size} !important;
    }}
    .stRadio label, .stCheckbox label {{
        font-size: {selected_size} !important;
    }}
    </style>
    """, unsafe_allow_html=True)


def get_user_profile_picture():
    """Get the current user's profile picture"""
    if "user_profile" in st.session_state:
        return st.session_state.user_profile.get("profile_picture", None)
    return None
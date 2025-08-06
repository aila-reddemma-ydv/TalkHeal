# --- 0. IMPORTS ---
import uuid  # standard library import
import streamlit as st
from auth.auth_utils import init_db
from components.login_page import show_login_page
 emoji-mood-selector
# --- 1. PAGE CONFIG FIRST ---
from core.config import PAGE_CONFIG
st.set_page_config(**PAGE_CONFIG) 
st.set_page_config(page_title="TalkHeal", page_icon="💬", layout="wide")

# --- DB Initialization ---
if "db_initialized" not in st.session_state:
    init_db()
    st.session_state["db_initialized"] = True

# --- Auth State Initialization ---
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "show_signup" not in st.session_state:
    st.session_state.show_signup = False

# --- LOGIN PAGE ---
if not st.session_state.authenticated:
    show_login_page()
    st.stop()

# --- TOP RIGHT BUTTONS: THEME TOGGLE & LOGOUT ---
if st.session_state.get("authenticated", False):
    col_spacer, col_theme, col_logout = st.columns([5, 0.5, 0.7])
    with col_spacer:
        pass  # empty spacer to push buttons right
    with col_theme:
        is_dark = st.session_state.get('dark_mode', False)
        if st.button("🌙" if is_dark else "☀️", key="top_theme_toggle", help="Toggle Light/Dark Mode", use_container_width=True):
            st.session_state.dark_mode = not is_dark
            st.session_state.theme_changed = True
            st.rerun()
    with col_logout:
        if st.button("Logout", key="logout_btn", use_container_width=True):
            for key in ["authenticated", "user_email", "user_name", "show_signup"]:
                if key in st.session_state:
                    del st.session_state[key]
            st.rerun()

# --- MAIN UI (only after login) ---
header_col1, header_col2, header_col3 = st.columns([6, 1, 1])
with header_col1:
    st.title(f"Welcome to TalkHeal, {st.session_state.user_name}! 💬")
    st.markdown("Navigate to other pages from the sidebar.")

import google.generativeai as genai
from core.utils import save_conversations, load_conversations
from core.config import configure_gemini, PAGE_CONFIG
from core.utils import get_current_time, create_new_conversation
from css.styles import apply_custom_css

from core.config import configure_gemini, get_tone_prompt, get_selected_mood
from core.utils import save_conversations, load_conversations, get_current_time, create_new_conversation

from components.header import render_header
from components.sidebar import render_sidebar
from components.chat_interface import render_chat_interface, handle_chat_input
from components.mood_dashboard import render_mood_dashboard
from components.focus_session import render_focus_session

# --- 1. PAGE CONFIG & CSS ---
apply_custom_css()
from components.emergency_page import render_emergency_page
from components.profile import apply_global_font_size

# --- 2. SESSION STATE INITIALIZATION ---
default_values = {
    "conversations": [],
    "active_conversation": -1,
    "send_chat_message": False,
    "pre_filled_chat_input": "",
    "selected_mood_context": "",
    "current_mood_val": "",
    "chat_history": [],
    "show_emergency_page": False,
    "show_focus_session": False,
    "show_mood_dashboard": False,
    "sidebar_state": "expanded",
    "mental_disorders": [
        "Anxiety", "Depression", "Bipolar Disorder", "PTSD",
        "OCD", "ADHD", "Eating Disorders", "Schizophrenia"
    ]
}

for key, value in default_values.items():
    if key not in st.session_state:
        st.session_state[key] = value

        "Depression & Mood Disorders", "Anxiety & Panic Disorders", "Bipolar Disorder",
        "PTSD & Trauma", "OCD & Related Disorders", "Eating Disorders",
        "Substance Use Disorders", "ADHD & Neurodevelopmental", "Personality Disorders",
        "Sleep Disorders"
    ],
    "selected_tone": "Compassionate Listener",
    "selected_mood": "🙂"
}

for key, value in default_values.items():
    if key not in st.session_state:
        st.session_state[key] = value

# --- 2. SET PAGE CONFIG ---
apply_global_font_size()

# --- 3. APPLY STYLES & CONFIGURATIONS ---
apply_custom_css()
model = configure_gemini()

# --- 4. TONE SELECTION DROPDOWN IN SIDEBAR ---
TONE_OPTIONS = {
    "Compassionate Listener": "You are a compassionate listener — soft, empathetic, patient — like a therapist who listens without judgment.",
    "Motivating Coach": "You are a motivating coach — energetic, encouraging, and action-focused — helping the user push through rough days.",
    "Wise Friend": "You are a wise friend — thoughtful, poetic, and reflective — giving soulful responses and timeless advice.",
    "Neutral Therapist": "You are a neutral therapist — balanced, logical, and non-intrusive — asking guiding questions using CBT techniques.",
    "Mindfulness Guide": "You are a mindfulness guide — calm, slow, and grounding — focused on breathing, presence, and awareness."
}

}

for key, val in default_values.items():
    if key not in st.session_state:
        st.session_state[key] = val

# --- 3. GEMINI MODEL SETUP ---
model = configure_gemini()

# --- 4. SIDEBAR ---
render_sidebar()

# --- 5. MAIN LOGIC CONTAINER ---
main_area = st.container()

# --- 6. Load or Start Conversation ---
if not st.session_state.conversations:
    saved = load_conversations()
    if saved:
        st.session_state.conversations = saved
        if st.session_state.active_conversation == -1:
            st.session_state.active_conversation = 0
    else:
        create_new_conversation()
        st.session_state.active_conversation = 0
    st.rerun()

# --- 7. ROUTING ---
with main_area:
    if st.session_state.get("show_emergency_page"):
        render_emergency_page()
    elif st.session_state.get("show_focus_session"):
        render_focus_session()
    elif st.session_state.get("show_mood_dashboard"):
        render_mood_dashboard()
    else:
        render_header()
        st.markdown(f"""
        <div style="text-align: center; margin: 20px 0;">
            <h3>🗣️ Current Chatbot Tone: <strong>{st.session_state['selected_tone']}</strong></h3>
            <h4>🧠 Mood Selected: <strong>{get_selected_mood()}</strong></h4>
        </div>
        """, unsafe_allow_html=True)

        render_chat_interface()
        handle_chat_input(model=model, system_prompt=get_tone_prompt())

# --- 8. AUTO SCROLL SCRIPT ---
st.markdown("""
<script>
    function scrollToBottom() {
        var chatContainer = document.querySelector('.chat-container');
        if (chatContainer) {
            chatContainer.scrollTop = chatContainer.scrollHeight;
        }
    }
    setTimeout(scrollToBottom, 100);
</script>
""", unsafe_allow_html=True)


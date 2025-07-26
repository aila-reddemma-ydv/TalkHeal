# --- 0. IMPORTS ---
import streamlit as st
import google.generativeai as genai

# --- 1. FIRST COMMAND: PAGE CONFIG ---
from core.config import PAGE_CONFIG
st.set_page_config(**PAGE_CONFIG)

# --- 2. CONTINUED IMPORTS ---
from core.utils import save_conversations, load_conversations, get_current_time, create_new_conversation
from core.config import configure_gemini, get_tone_prompt, get_selected_mood
from css.styles import apply_custom_css
from components.header import render_header
from components.sidebar import render_sidebar
from components.chat_interface import render_chat_interface, handle_chat_input
from components.emergency_page import render_emergency_page

# --- 3. SESSION STATE INITIALIZATION ---
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "conversations" not in st.session_state:
    st.session_state.conversations = load_conversations()
if "active_conversation" not in st.session_state:
    st.session_state.active_conversation = -1
if "show_emergency_page" not in st.session_state:
    st.session_state.show_emergency_page = False
if "sidebar_state" not in st.session_state:
    st.session_state.sidebar_state = "expanded"
if "mental_disorders" not in st.session_state:
    st.session_state.mental_disorders = [
        "Depression & Mood Disorders", "Anxiety & Panic Disorders", "Bipolar Disorder",
        "PTSD & Trauma", "OCD & Related Disorders", "Eating Disorders",
        "Substance Use Disorders", "ADHD & Neurodevelopmental", "Personality Disorders",
        "Sleep Disorders"
    ]
if "selected_tone" not in st.session_state:
    st.session_state.selected_tone = "Compassionate Listener"
if "selected_mood" not in st.session_state:
    st.session_state.selected_mood = "🙂"  # Default emoji mood

# --- 4. STYLES & GEMINI SETUP ---
apply_custom_css()
model = configure_gemini()

# --- 5. SIDEBAR ---
render_sidebar()

# --- 6. MAIN PAGE ROUTING LOGIC ---
main_area = st.container()

# Load conversations or start a new one
if not st.session_state.conversations:
    saved_convos = load_conversations()
    if saved_convos:
        st.session_state.conversations = saved_convos
        if st.session_state.active_conversation == -1:
            st.session_state.active_conversation = 0
    else:
        create_new_conversation()
        st.session_state.active_conversation = 0
    st.rerun()

# --- 7. MAIN VIEW DISPLAY ---
if st.session_state.get("show_emergency_page"):
    with main_area:
        render_emergency_page()
else:
    with main_area:
        render_header()
        st.subheader(f"🗣️ Current Chatbot Tone: **{st.session_state['selected_tone']}**")
        st.markdown(f"**🧠 Mood Selected:** {get_selected_mood()}")
        render_chat_interface()
        handle_chat_input(model, system_prompt=get_tone_prompt())

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

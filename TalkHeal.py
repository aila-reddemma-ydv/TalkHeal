# --- 0. IMPORTS ---
import uuid  # standard library import
import streamlit as st

# --- 1. PAGE CONFIG FIRST ---
from core.config import PAGE_CONFIG
st.set_page_config(**PAGE_CONFIG) 
from css.styles import apply_custom_css

from core.config import configure_gemini, get_tone_prompt, get_selected_mood
from core.utils import save_conversations, load_conversations, get_current_time, create_new_conversation

from components.header import render_header
from components.sidebar import render_sidebar
from components.chat_interface import render_chat_interface, handle_chat_input
from components.emergency_page import render_emergency_page

# --- 1. PAGE CONFIG & CSS ---
apply_custom_css()

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
    "sidebar_state": "expanded",
    "mental_disorders": [
        "Depression & Mood Disorders", "Anxiety & Panic Disorders", "Bipolar Disorder",
        "PTSD & Trauma", "OCD & Related Disorders", "Eating Disorders",
        "Substance Use Disorders", "ADHD & Neurodevelopmental", "Personality Disorders",
        "Sleep Disorders"
    ],
    "selected_tone": "Compassionate Listener",
    "selected_mood": "🙂"
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
    else:
        render_header()
        st.subheader(f"🗣️ Current Chatbot Tone: **{st.session_state['selected_tone']}**")
        st.markdown(f"**🧠 Mood Selected:** {get_selected_mood()}")
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

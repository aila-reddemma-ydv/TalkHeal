import streamlit as st
import google.generativeai as genai
from pathlib import Path

# ---------- Logo and Page Config ----------
logo_path = str(Path(__file__).resolve().parent.parent / "TalkHealLogo.png")

PAGE_CONFIG = {
    "page_title": "TalkHeal - Mental Health Support",
    "page_icon": logo_path,
    "layout": "wide",
    "initial_sidebar_state": "expanded",
    "menu_items": None
}

# ⚠️ DO NOT CALL st.set_page_config HERE — it's already set in talkheal.py

# ---------- Tone Options ----------
TONE_OPTIONS = {
    "Compassionate Listener": "You are a compassionate listener — soft, empathetic, patient — like a therapist who listens without judgment.",
    "Motivating Coach": "You are a motivating coach — energetic, encouraging, and action-focused — helping the user push through rough days.",
    "Wise Friend": "You are a wise friend — thoughtful, poetic, and reflective — giving soulful responses and timeless advice.",
    "Neutral Therapist": "You are a neutral therapist — balanced, logical, and non-intrusive — asking guiding questions using CBT techniques.",
    "Mindfulness Guide": "You are a mindfulness guide — calm, slow, and grounding — focused on breathing, presence, and awareness."
}

# ---------- Emoji-Based Mood Options ----------
MOOD_OPTIONS = {
    "😊": "Happy",
    "😢": "Sad",
    "😡": "Angry",
    "😰": "Anxious",
    "😌": "Relaxed",
    "😔": "Lonely"
}

# ---------- Gemini API Configuration ----------
def configure_gemini():
    try:
        api_key = st.secrets["GEMINI_API_KEY"]
        if not api_key or api_key == "YOUR_API_KEY_HERE":
            raise ValueError("API key is missing or not set properly.")
        genai.configure(api_key=api_key)
        return genai.GenerativeModel('gemini-2.0-flash')
    except KeyError:
        st.error("❌ Gemini API key not found. Please set it in `.streamlit/secrets.toml` as GEMINI_API_KEY.")
    except Exception as e:
        st.error(f"❌ Failed to configure Gemini API: {e}")
    return None

# ---------- Get Tone Prompt ----------
def get_tone_prompt():
    tone = st.session_state.get("selected_tone", "Compassionate Listener")
    return TONE_OPTIONS.get(tone, TONE_OPTIONS["Compassionate Listener"])

# ---------- Get Mood Label ----------
def get_selected_mood():
    emoji = st.session_state.get("selected_mood", "😊")
    return MOOD_OPTIONS.get(emoji, "Happy")  # default fallback
# ---------- Conversation State Utility ----------
def create_new_conversation():
    from datetime import datetime

    new_convo = {
        "title": "New Chat",
        "messages": [],
        "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    if "conversations" not in st.session_state:
        st.session_state.conversations = []

    st.session_state.conversations.insert(0, new_convo)
    st.session_state.active_conversation = 0


import streamlit as st
import google.generativeai as genai
from pathlib import Path
import requests

# ---------- Logo and Page Config ----------
logo_path = str(Path(__file__).resolve().parent.parent / "TalkHealLogo.png")

PAGE_CONFIG = {
    "page_title": "TalkHeal - Mental Health Support",
    "page_icon": logo_path,
    "layout": "wide",
    "initial_sidebar_state": "expanded",
    "menu_items": None
}

emoji-mood-selector
# ⚠️ DO NOT CALL st.set_page_config HERE — it's already set in talkheal.py
#st.set_page_config(**PAGE_CONFIG)

# ---------- Custom Dropdown Style ----------
st.markdown("""
    <style>
        div[data-baseweb="select"] {
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15);
            border-radius: 8px;
        }
    </style>
""", unsafe_allow_html=True)


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
# ---------- Get Mood Label (for emoji picker) ----------
def get_selected_mood():
    emoji = st.session_state.get("selected_mood", "😊")
    return MOOD_OPTIONS.get(emoji, "Happy")  # default fallback

# ---------- Get Mood Prompt (for emoji-based OR radio mood selector) ----------
def get_mood_context():
    mood = st.session_state.get("current_mood_val") or get_selected_mood()
    return f"The user is currently feeling '{mood}'. Please respond empathetically and supportively based on their emotional state."

# ---------- Generate AI Response ----------
def generate_response(user_input, model):
    system_prompt = get_tone_system_prompt()
    try:
        response = model.generate_content([
            {"role": "system", "parts": [system_prompt]},
            {"role": "user", "parts": [user_input]}
        ])
        return response.text
    except ValueError as e:
        st.error("❌ Invalid input or model configuration issue. Please check your input.")
        return None
    except google.generativeai.types.BlockedPromptException as e:
        st.error("❌ Content policy violation. Please rephrase your message.")
        return None
    except google.generativeai.types.GenerationException as e:
        st.error("❌ Failed to generate response. Please try again.")
        return None
    except requests.RequestException as e:
        st.error("❌ Network connection issue. Please check your internet connection.")
        return None
    except Exception as e:
        st.error(f"❌ Unexpected error occurred: {e}")
        return None

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
# ---------- Required Constants for Imports ----------
MODEL = "models/gemini-1.5-flash"  # or use gemini-2.0 if preferred
SYSTEM_PROMPT = """
You are TalkHeal, a compassionate and supportive AI assistant focused on mental well-being.
Always reply empathetically, provide helpful suggestions, and foster a safe space for open communication.
"""


from datetime import datetime, timedelta, timezone
import streamlit as st
import re
import json
import os
import requests

def get_current_time():
    """Returns the user's local time formatted as HH:MM AM/PM."""
    tz_offset = st.context.timezone_offset

    if tz_offset is None:
        # Default to UTC if timezone is not available (e.g., on Streamlit Cloud)
        now = datetime.now()
    else:
        now_utc = datetime.now(timezone.utc)
        now = now_utc + timedelta(minutes=-tz_offset)

    return now.strftime("%I:%M %p").lstrip("0")

def create_new_conversation(initial_message=None):
    """
    Creates a new conversation in the session state.
    Optionally adds an initial message to the conversation.
    Returns the index of the newly created conversation.
    """
    new_convo = {
        "id": len(st.session_state.conversations),
        "title": initial_message[:30] + "..." if initial_message and len(initial_message) > 30 else "New Conversation",
        "date": datetime.now().strftime("%B %d, %Y"),
        "messages": []
    }

    if initial_message:
        new_convo["messages"].append({
            "sender": "user",
            "message": initial_message,
            "time": get_current_time()
        })

    st.session_state.conversations.insert(0, new_convo)
    st.session_state.active_conversation = 0
    return 0

def clean_ai_response(response_text):
    if not response_text:
        return response_text
    response_text = re.sub(r'<[^>]+>', '', response_text)
    response_text = re.sub(r'\s+', ' ', response_text).strip()
    response_text = response_text.replace('&nbsp;', ' ')
    response_text = response_text.replace('&lt;', '<')
    response_text = response_text.replace('&gt;', '>')
    response_text = response_text.replace('&amp;', '&')
    return response_text

def get_ai_response(user_message, model):
    if model is None:
        return "I'm sorry, I can't connect right now. Please check the API configuration."

    mental_health_prompt = f"""
    You are a compassionate mental health support chatbot named TalkHeal. Your role is to:
    1. Provide empathetic, supportive responses
    2. Encourage professional help when needed
    3. Never diagnose or provide medical advice
    4. Be warm, understanding, and non-judgmental
    5. Ask follow-up questions to better understand the user's situation
    6. Provide coping strategies and resources when appropriate
    7. Not assume that the user is always in overwhelming states. Sometimes he/she might also be in joyful or curious moods and ask questions not related to mental health

    IMPORTANT: Respond with PLAIN TEXT ONLY. Do not include any HTML tags, markdown formatting, or special characters. Just provide a natural, conversational response.

    User message: {user_message}

    Respond in a caring, supportive manner (keep response under 150 words):
    """
    
    try:
        response = model.generate_content(mental_health_prompt)
        cleaned_response = clean_ai_response(response.text)
        return cleaned_response
    except Exception as e:
        return "I'm here to listen and support you. Sometimes I have trouble connecting, but I want you to know that your feelings are valid and you're not alone. Would you like to share more about what you're experiencing?"

# Implementing IP Based Isolation
def cached_user_ip():
    # Check if IP is already cached in session state
    if hasattr(st.session_state, 'cached_ip') and hasattr(st.session_state, 'ip_cache_time'):
        # Check if cache is still valid (cache for 1 hour)
        cache_age = datetime.now() - st.session_state.ip_cache_time
        if cache_age < timedelta(hours=1):
            return st.session_state.cached_ip
    
    # Cache is missing or expired, fetch new IP
    try:
        response = requests.get("https://api.ipify.org", timeout=5)
        ip = response.text.strip()
        # Cache the IP and timestamp
        st.session_state.cached_ip = ip
        st.session_state.ip_cache_time = datetime.now()
        
        return ip
    except (requests.RequestException, requests.Timeout, Exception):
        # Fallback: use session ID or generate a unique identifier
        fallback_id = f"session_{hash(str(st.session_state)) % 100000}"
        
        # Cache the fallback ID so we use the same one consistently
        if not hasattr(st.session_state, 'cached_ip'):
            st.session_state.cached_ip = fallback_id
            st.session_state.ip_cache_time = datetime.now()
        
        return st.session_state.cached_ip

def get_user_ip():
    try:
        return requests.get("https://api.ipify.org").text
    except:
        return "unknown_ip"

def get_memory_file():
    ip = cached_user_ip()
    os.makedirs("data", exist_ok=True)
    return f"data/conversations_{ip}.json"

def save_conversations(conversations):
    memory_file = get_memory_file()
    with open(memory_file, 'w', encoding="utf-8") as f:
        json.dump(conversations, f, indent=4)

def load_conversations():
    memory_file = get_memory_file()
    if not os.path.exists(memory_file):
        return []
    with open(memory_file, 'r', encoding="utf-8") as f:
        return json.load(f)

# Mood Tip Generator
def get_mood_tip(mood):
    """
    Returns a tip or message based on the selected mood.
    """
    tips = {
        "Very Low": "It's okay to feel low sometimes. Consider talking to a friend or therapist.",
        "Low": "Take a short walk, breathe deeply, and treat yourself with kindness.",
        "Okay": "You're doing okay. Reflect on something you're grateful for today.",
        "Good": "That's great! Maybe help someone else feel good too.",
        "Great": "Awesome! Keep that positive energy going and spread it around."
    }
    return tips.get(mood, "Remember to take care of yourself.")
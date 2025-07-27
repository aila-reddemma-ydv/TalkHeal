import requests
import os
import streamlit as st

def get_ai_response(prompt, model="gemini-1.5-flash"):
    api_key = st.secrets.get("GEMINI_API_KEY", os.getenv("GEMINI_API_KEY"))
    if not api_key:
        raise ValueError("Gemini API key not found in secrets or environment variables.")

    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"
    headers = {
        "Content-Type": "application/json",
        "X-goog-api-key": api_key
    }
    data = {
        "contents": [
            {
                "parts": [{"text": prompt}]
            }
        ]
    }

    response = requests.post(url, headers=headers, json=data)

    # ✅ ADD THIS BLOCK HERE (before you parse JSON)
    if response.status_code != 200:
        st.error(f"Gemini API Error {response.status_code}: {response.text}")
        return "⚠️ Gemini API failed to respond. Please try again."

    try:
        return response.json()["candidates"][0]["content"]["parts"][0]["text"]
    except Exception as e:
        return f"⚠️ Failed to parse Gemini response: {e}"

import streamlit as st
import streamlit as st
import streamlit.components.v1 as components
from datetime import datetime
from core.utils import get_current_time, get_ai_response, save_conversations

# --- Inject JS to get user's local time zone ---
def set_user_time_in_session():
    if "user_time_offset" not in st.session_state:
        components.html("""
            <script>
            const offset = new Date().getTimezoneOffset(); 
            const time = new Date().toLocaleString();      
            const data = {offset: offset, time: time};
            window.parent.postMessage({type: 'USER_TIME', data: data}, '*');
            </script>
        """, height=0)

        st.markdown("""
        <script>
        window.addEventListener("message", (event) => {
            if (event.data.type === "USER_TIME") {
                const payload = JSON.stringify(event.data.data);
                fetch("/", {
                    method: "POST",
                    headers: {"Content-Type": "application/json"},
                    body: payload
                }).then(() => location.reload());
            }
        });
        </script>
        """, unsafe_allow_html=True)

set_user_time_in_session()

# --- Render chat messages ---
def render_chat_interface():
    st.markdown("### 🗨️ TalkHeal Conversation")

    active_index = st.session_state.get("active_conversation", -1)
    if active_index == -1 or active_index >= len(st.session_state.conversations):
        st.info("Start a conversation to see messages here.")
        return

    conversation = st.session_state.conversations[active_index]

    if not conversation["messages"]:
        st.markdown(f"""
        <div class="welcome-message">
            <strong>Hello! I'm TalkHeal, your mental health companion 🤗</strong><br>
            How are you feeling today? You can write below or start a new topic.
            <div class="message-time">{get_current_time()}</div>
        </div>
        """, unsafe_allow_html=True)

    for msg in conversation["messages"]:
        sender = msg["sender"]
        message = msg["message"]
        time = msg["time"]

        if sender == "user":
            with st.chat_message("user", avatar="🧍‍♀️"):
                st.markdown(f"**You:** {message}\n\n<sub>{time}</sub>", unsafe_allow_html=True)
        else:
            with st.chat_message("assistant", avatar="💬"):
                st.markdown(f"{message}\n\n<sub>{time}</sub>", unsafe_allow_html=True)

def handle_chat_input(model, system_prompt):
    pre_filled = st.session_state.get("pre_filled_chat_input", "")
    st.session_state.pre_filled_chat_input = ""

    form_key = f"chat_form_{st.session_state.get('active_conversation', 0)}"

    with st.form(key=form_key, clear_on_submit=True):
        col1, col2 = st.columns([5, 1])
        with col1:
            user_input = st.text_input(
                "Share your thoughts...",
                key="message_input",
                label_visibility="collapsed",
                placeholder="Type your message here...",
                value=pre_filled
            )
        with col2:
            send_pressed = st.form_submit_button("Send", use_container_width=True)

    auto_send = st.session_state.get("send_chat_message", False)

    if (send_pressed or auto_send) and user_input.strip():
        if auto_send:
            st.session_state.send_chat_message = False

        if st.session_state.active_conversation >= 0:
            current_time = get_current_time()
            active_convo = st.session_state.conversations[st.session_state.active_conversation]

            # Save user message
            active_convo["messages"].append({
                "sender": "user",
                "message": user_input.strip(),
                "time": current_time
            })

            if len(active_convo["messages"]) == 1:
                title = user_input[:30] + "..." if len(user_input) > 30 else user_input
                active_convo["title"] = title

            save_conversations(st.session_state.conversations)

            def format_memory(convo_history, max_turns=10):
                context = ""
                for msg in convo_history[-max_turns*2:]:
                    sender = "User" if msg["sender"] == "user" else "Bot"
                    context += f"{sender}: {msg['message']}\n"
                return context

            try:
                with st.spinner("TalkHeal is thinking..."):
                    memory = format_memory(active_convo["messages"])
                    mood = st.session_state.get("selected_mood_context") or st.session_state.get("current_mood_val", "okay")

                    prompt = (
                        f"{system_prompt}\n\n"
                        f"User is feeling {mood}. Respond empathetically.\n\n"
                        f"{memory}\nUser: {user_input.strip()}\nBot:"
                    )

                    ai_response = get_ai_response(prompt, "gemini-1.5-flash")

                    active_convo["messages"].append({
                        "sender": "bot",
                        "message": ai_response,
                        "time": get_current_time()
                    })

            except ValueError as e:
                st.error("I'm having trouble understanding your message. Could you please rephrase it?")
                active_convo["messages"].append({
                    "sender": "bot",
                    "message": "I'm having trouble understanding your message. Could you please rephrase it?",
                    "time": get_current_time()
                })
            except requests.RequestException as e:
                st.error("Network connection issue. Please check your internet connection.")
                active_convo["messages"].append({
                    "sender": "bot",
                    "message": "I'm having trouble connecting to my services. Please check your internet connection and try again.",
                    "time": get_current_time()
                })
            except Exception as e:
                st.error(f"An unexpected error occurred. Please try again.")
                active_convo["messages"].append({
                    "sender": "bot",
                    "message": "I'm having trouble responding right now. Please try again in a moment.",
                    "time": get_current_time()
                })

            save_conversations(st.session_state.conversations)
            st.rerun()

__all__ = ["render_chat_interface", "handle_chat_input"]

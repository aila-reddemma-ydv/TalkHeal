import streamlit as st
import webbrowser
from datetime import datetime
from core.utils import create_new_conversation, get_current_time
from core.theme import get_current_theme, toggle_theme, set_palette, PALETTES
#from core.resource import GLOBAL_RESOURCES, mental_health_resources_full


# --- Structured Emergency Resources ---
GLOBAL_RESOURCES = [
    {"name": "Befrienders Worldwide", "desc": "Emotional support to prevent suicide worldwide.",
        "url": "https://www.befrienders.org/"},
    {"name": "International Association for Suicide Prevention (IASP)", "desc": "Find a crisis center anywhere in the world.",
     "url": "https://www.iasp.info/resources/Crisis_Centres/"},
    {"name": "Crisis Text Line", "desc": "Text-based support available in the US, UK, Canada, and Ireland.",
     "url": "https://www.crisistextline.org/"},
    {"name": "The Trevor Project", "desc": "Crisis intervention and suicide prevention for LGBTQ young people.",
     "url": "https://www.thetrevorproject.org/"},
    {"name": "Child Helpline International", "desc": "A global network of child helplines for young people in need of help.",
     "url": "https://www.childhelplineinternational.org/"}
]

mental_health_resources_full = {
    "Depression & Mood Disorders": {
        "description": "Information on understanding and coping with depression, persistent depressive disorder, and other mood-related challenges.",
        "links": [
            {"label": "NIMH - Depression",
                "url": "https://www.nimh.nih.gov/health/topics/depression"},
            {"label": "Mayo Clinic - Depression",
                "url": "https://www.mayoclinic.org/diseases-conditions/depression/symptoms-causes/syc-20356007"}
        ]
    },
    "Anxiety & Panic Disorders": {
        "description": "Guidance on managing generalized anxiety, social anxiety, panic attacks, and phobias.",
        "links": [
            {"label": "ADAA - Anxiety & Depression", "url": "https://adaa.org/"},
            {"label": "NIMH - Anxiety Disorders",
                "url": "https://www.nimh.nih.gov/health/topics/anxiety-disorders"}
        ]
    },
    "Bipolar Disorder": {
        "description": "Understanding the complexities of bipolar disorder, including mood swings and treatment options.",
        "links": [
            {"label": "NIMH - Bipolar Disorder",
                "url": "https://www.nimh.nih.gov/health/topics/bipolar-disorder"}
        ]
    },
    "PTSD & Trauma": {
        "description": "Resources for individuals experiencing post-traumatic stress disorder and other trauma-related conditions.",
        "links": [
            {"label": "PTSD: National Center", "url": "https://www.ptsd.va.gov/"}
        ]
    },
    "OCD & Related Disorders": {
        "description": "Support and information for obsessive-compulsive disorder, body dysmorphic disorder, and hoarding disorder.",
        "links": [
            {"label": "IOCDF - OCD", "url": "https://iocdf.org/"}
        ]
    },
    "Coping Skills & Self-Care": {
        "description": "Practical strategies and techniques for stress management, emotional regulation, and daily well-being.",
        "links": [
            {"label": "HelpGuide - Stress Management",
                "url": "https://www.helpguide.org/articles/stress/stress-management.htm"}
        ]
    },
    "Therapy & Treatment Options": {
        "description": "Overview of various therapeutic approaches, including CBT, DBT, and finding a therapist.",
        "links": [
            {"label": "APA - Finding a Therapist",
                "url": "https://www.apa.org/helpcenter/choose-therapist"}
        ]
    }
}


import streamlit as st
from core.utils import save_conversations
from core.config import create_new_conversation

def render_sidebar():
    """Renders the left and right sidebars."""

    with st.sidebar:
        st.markdown("### 💬 Conversations")
        if "show_quick_start_prompts" not in st.session_state:
            st.session_state.show_quick_start_prompts = False
        if "pre_filled_chat_input" not in st.session_state:
            st.session_state.pre_filled_chat_input = ""
        if "send_chat_message" not in st.session_state:
            st.session_state.send_chat_message = False

        if st.button("➕ New Chat", key="new_chat", use_container_width=True, type="primary"):
            create_new_conversation()
            st.session_state.show_quick_start_prompts = True
            st.rerun()

        if st.session_state.show_quick_start_prompts:
            st.markdown("---")
            st.markdown("**Start with a common topic:**")
            quick_prompts = [
                "Feeling overwhelmed",
                "Need to vent about my day",
                "How to manage stress?",
                "Tell me about anxiety"
            ]
            qp_cols = st.columns(2)
            for i, prompt in enumerate(quick_prompts):
                with qp_cols[i % 2]:
                    if st.button(f"✨ {prompt}", key=f"qp_{i}", use_container_width=True):
                        st.session_state.pre_filled_chat_input = prompt
                        st.session_state.send_chat_message = True
                        st.session_state.show_quick_start_prompts = False
                        st.rerun()

            st.markdown("---")

        if st.session_state.conversations:
            if "delete_candidate" not in st.session_state:
                for i, convo in enumerate(st.session_state.conversations):
                    is_active = i == st.session_state.active_conversation
                    button_style_icon = "🟢" if is_active else "📝"

                    col1, col2 = st.columns([5, 1])
                    with col1:
                        if st.button(
                            f"{button_style_icon} {convo['title'][:22]}...",
                            key=f"convo_{i}",
                            help=f"Started: {convo['date']}",
                            use_container_width=True
                        ):
                            st.session_state.active_conversation = i
                            st.rerun()
                    with col2:
                        if st.button("🗑️", key=f"delete_{i}", type="primary"):
                            st.session_state.delete_candidate = i
                            st.rerun()

            else:
                st.warning("⚠️ Are you sure you want to delete this conversation?")
                col_confirm, col_cancel = st.columns(2)

                if col_confirm.button("Yes, delete", key="confirm_delete"):
                    del st.session_state.conversations[st.session_state.delete_candidate]
                    save_conversations(st.session_state.conversations)
                    del st.session_state.delete_candidate
                    st.session_state.active_conversation = -1
                    st.rerun()

                if col_cancel.button("Cancel", key="cancel_delete"):
                    del st.session_state.delete_candidate
                    st.rerun()
        else:
            st.info("No conversations yet. Start a new chat!")

        st.markdown("---")

        if st.button("🚨 Emergency Help", use_container_width=True, type="secondary"):
            st.session_state.show_emergency_page = True
            st.rerun()

        # --- Mood Tracker ---
        with st.expander("🧠 Mental Health Check", expanded=True):
            st.markdown("**How are you feeling today?**")

            mood_options_map = {
                "😔 Very Low": "very_low",
                "😐 Low": "low",
                "😊 Okay": "okay",
                "😄 Good": "good",
                "🌟 Great": "great"
            }
            mood_labels = list(mood_options_map.keys())

            selected_mood_label = st.radio(
                label="Mood Scale",
                options=mood_labels,
                index=2,
                key="mood_selector_radio",
                horizontal=True,
                label_visibility="collapsed"
            )

            current_mood_val = mood_options_map[selected_mood_label]
            st.session_state["current_mood_val"] = current_mood_val

            journal_prompts = {
                "very_low": "What's weighing on your mind today?",
                "low": "What are your thoughts right now?",
                "okay": "Anything specific on your mind today?",
                "good": "What made you feel good today?",
                "great": "What's making you shine today?"
            }

            st.markdown(f"**📝 {journal_prompts[current_mood_val]}**")
            journal_input = st.text_area("Your thoughts:", key="mood_journal_area", height=100)

            # Initialize states
            if "mood_journal_entry" not in st.session_state:
                st.session_state.mood_journal_entry = ""
            if "mood_tip_display" not in st.session_state:
                st.session_state.mood_tip_display = ""
            if "mood_entry_status" not in st.session_state:
                st.session_state.mood_entry_status = ""

            tips_for_mood = {
                "very_low": "Remember, it's okay not to be okay. Consider connecting with a professional.",
                "low": "Even small steps help. Try a brief mindful moment or gentle activity.",
                "okay": "Keep nurturing your well-being. What's one thing you can do to maintain this?",
                "good": "That's wonderful! Savor this feeling and perhaps share your positivity.",
                "great": "Fantastic! How can you carry this energy forward into your day?"
            }.get(current_mood_val, "A general tip for your mood.")

            st.markdown("")
            col1, col2 = st.columns(2)

            with col1:
                if st.button("Get Tip & Save Entry", key="save_mood_entry", use_container_width=True):
                    st.session_state.mood_tip_display = tips_for_mood
                    st.session_state.mood_entry_status = f"Your mood entry for '{selected_mood_label}' has been noted."
                    st.session_state.mood_journal_entry = ""

            with col2:
                if st.button("Ask TalkHeal", key="ask_peace_pulse_from_mood", use_container_width=True):
                    if st.session_state.mood_journal_area.strip():
                        st.session_state.pre_filled_chat_input = st.session_state.mood_journal_area
                        st.session_state.send_chat_message = True
                        st.session_state.mood_journal_entry = ""
                        st.session_state.mood_tip_display = ""
                        st.session_state.mood_entry_status = ""
                        st.rerun()
                    else:
                        st.warning("Please enter your thoughts before asking TalkHeal.")

            if st.session_state.mood_tip_display:
                st.success(st.session_state.mood_tip_display)
                st.session_state.mood_tip_display = ""

            if st.session_state.mood_entry_status:
                st.info(st.session_state.mood_entry_status)
                st.session_state.mood_entry_status = ""


        # --- 4. Resource Hub with Categories & Search ---
        with st.expander("📚 Resources & Knowledge Base"):
            st.markdown("**Explore topics or search for help:**")

            resource_search_query = st.text_input(
                "Search resources...", key="resource_search", placeholder="e.g., 'anxiety tips', 'therapy'", label_visibility="collapsed")

            if resource_search_query:
                filtered_topics = [
                    topic for topic in mental_health_resources_full
                    if resource_search_query.lower() in topic.lower() or
                    any(resource_search_query.lower() in link['label'].lower() for link in mental_health_resources_full[topic]['links']) or
                    resource_search_query.lower(
                    ) in mental_health_resources_full[topic]['description'].lower()
                ]

                if not filtered_topics:
                    st.info("No resources found matching your search.")
                else:
                    st.markdown("---")
                    st.markdown("**Matching Resources:**")
                    for topic in filtered_topics:
                        st.markdown(f"**{topic}**")
                        st.info(
                            mental_health_resources_full[topic]['description'])
                        for link in mental_health_resources_full[topic]['links']:
                            st.markdown(f"• [{link['label']}]({link['url']})")
                        st.markdown("---")
            else:
                resource_tabs = st.tabs(
                    list(mental_health_resources_full.keys()))

                for i, tab_title in enumerate(mental_health_resources_full.keys()):
                    with resource_tabs[i]:
                        topic_data = mental_health_resources_full[tab_title]
                        st.markdown(f"**{tab_title}**")
                        st.info(topic_data['description'])
                        for link in topic_data['links']:
                            st.markdown(f"• [{link['label']}]({link['url']})")
                        st.markdown("---")

        with st.expander("☎️ Crisis Support"):
            st.markdown("**24/7 Crisis Hotlines:**")
            for resource in GLOBAL_RESOURCES:
                st.markdown(
                    f"**{resource['name']}**: {resource['desc']} [Visit Website]({resource['url']})")

        # Theme toggle in sidebar
        with st.expander("🎨 Theme Settings"):
            current_theme = get_current_theme()
            is_dark = current_theme["name"] == "Dark"

            # Palette selector (only for light mode)
            if not is_dark:
                palette_names = [p["name"] for p in PALETTES]
                selected_palette = st.selectbox(
                    "Choose a soothing color palette:",
                    palette_names,
                    index=palette_names.index(
                        st.session_state.get("palette_name", "Light")),
                    key="palette_selector",
                )
                if selected_palette != st.session_state.get("palette_name", "Light"):
                    set_palette(selected_palette)

            # Current theme display with better styling
            st.markdown("""
            <div class="theme-info-box">
                <strong>Current Theme:</strong><br>
                <span>{} Mode</span>
            </div>
            """.format(current_theme['name']), unsafe_allow_html=True)

            # Theme toggle button with better styling
            button_text = "🌙 Dark Mode" if not is_dark else "☀️ Light Mode"
            button_color = "primary" if not is_dark else "secondary"

            if st.button(
                button_text,
                key="sidebar_theme_toggle",
                use_container_width=True,
                type=button_color
            ):
                toggle_theme()

        # Quizzes expander (no longer contains nested expander)
        with st.expander("🧪 Take PsyToolkit Verified Quizzes"):
            st.markdown("""
            Explore scientifically backed quizzes to better understand your mental well-being. These tools are for **self-awareness** and not clinical diagnosis.
            """)

            quizzes = [
                {
                    "name": "GAD-7 (Anxiety Assessment)",
                    "desc": "Measures severity of generalized anxiety symptoms.",
                    "url": "https://www.psytoolkit.org/cgi-bin/3.6.0/survey?s=u8bAf",
                    "score_info": """
                    Score Interpretation:
                    GAD-7 score runs from 0 to 21
                    - 0–4: Minimal anxiety  
                    - 5–9: Mild anxiety  
                    - 10–14: Moderate anxiety  
                    - 15–21: Severe anxiety
                    """
                },
                {
                    "name": "PHQ-9 (Depression Assessment)",
                    "desc": "Screens for presence and severity of depression.",
                    "url": "https://www.psytoolkit.org/cgi-bin/3.6.0/survey?s=Hj32b",
                    "score_info": """
                    Score Interpretation:
                    - 0–4: Mild depression  
                    - 5–9: Moderate depression  
                    - 10–14: Moderately severe depression  
                    - 15–19: Severe depression 
                    """
                },
                {
                    "name": "The WHO-5 Well-Being Index",
                    "desc": "Five simple non-intrusive questions to assess well-being. Score ranges from 0 (poor) to 100 (excellent).",
                    "url": "https://www.psytoolkit.org/cgi-bin/3.6.0/survey?s=POqLJ",
                    "score_info": """
                    Score Interpretation:
                    -if your score is 50 or lower you should consider 
                    -further checks on whether you suffer 
                    -from clinical depression
                    """
                },
               {
    "name": "Depression Anxiety Stress Scales (DASS)",
    "desc": "Measures depression, anxiety, and stress using one combined questionnaire.",
    "url": "https://www.psytoolkit.org/cgi-bin/3.6.0/survey?s=HvfDY",
    "score_info": "**Score Interpretation (per subscale):**\n\n- **Normal, Mild, Moderate, Severe, Extremely Severe**\n\n|          | Depression | Anxiety | Stress  |\n|----------|------------|---------|---------|\n| Normal   | 0-9        | 0-7     | 0-14    |\n| Mild     | 10-13      | 8-9     | 15-18   |\n| Moderate | 14-20      | 10-14   | 19-25   |\n| Severe   | 21-27      | 15-19   | 26-33   |\n| Extremely Severe | 28+ | 20+ | 34+ |"
}
            ]

            for quiz in quizzes:
                st.markdown(f"""
                **{quiz['name']}**  
                *{quiz['desc']}*  
                [🔗 Take Quiz]({quiz['url']})  
                {quiz['score_info']}
                """)

        # About section moved outside of any expander
        st.markdown("---")
        st.markdown("""
        **ℹ️ About TalkHeal**  
        Your compassionate mental health companion, designed to provide:
        
        • 24/7 emotional support  
        • Resource guidance  
        • Crisis intervention  
        • Professional referrals  
        
        **Remember:** This is not a substitute for professional mental health care.
        
        ---
        
        **Created with ❤️ by [Eccentric Explorer](https://eccentriccoder01.github.io/Me)**  
        *"It's absolutely okay not to be okay :)"*  
        
        📅 Enhanced Version - May 2025
        """)
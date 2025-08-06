import streamlit as st

def render_header():
    with st.container():
        # Only one column for header
        column = st.columns(1)[0]
        with column:
            st.markdown("""
            <div class="main-header" style="text-align:center;">
                <h1 style="margin-bottom:0;">TalkHeal</h1>
                <p style="margin-top:0;">Your Mental Health Companion 💙</p>
            </div>
            """, unsafe_allow_html=True)

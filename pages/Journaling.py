import streamlit as st
import sqlite3
import datetime
import base64
from uuid import uuid4

def get_base64_of_bin_file(bin_file_path):
    with open(bin_file_path, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

def set_background(main_bg_path, sidebar_bg_path=None):
    main_bg = get_base64_of_bin_file(main_bg_path)
    sidebar_bg = get_base64_of_bin_file(sidebar_bg_path) if sidebar_bg_path else main_bg

    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("data:image/png;base64,{main_bg}");
            background-size: cover;
            background-attachment: fixed;
            background-repeat: no-repeat;
        }}

        [data-testid="stSidebar"] {{
            background-color: rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(10px);
            -webkit-backdrop-filter: blur(10px);
            border-right: 2px solid rgba(245, 167, 208, 0.6);
            box-shadow: 4px 0 24px rgba(0,0,0,0.15);
        }}

        [data-testid="stSidebar"] > div:first-child {{
            background-image: url("data:image/png;base64,{sidebar_bg}");
            background-size: cover;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

def analyze_sentiment(entry: str) -> str:
    if any(word in entry.lower() for word in ['sad', 'tired', 'upset', 'angry']):
        return "Negative"
    elif any(word in entry.lower() for word in ['happy', 'grateful', 'joy']):
        return "Positive"
    return "Neutral"

DB_PATH = "journals.db"

def init_journal_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS journal_entries (
        id TEXT PRIMARY KEY,
        email TEXT,
        entry TEXT,
        sentiment TEXT,
        date TEXT
    )
    """)
    conn.commit()
    conn.close()

def save_entry(email, entry, sentiment):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO journal_entries (id, email, entry, sentiment, date)
    VALUES (?, ?, ?, ?, ?)
    """, (str(uuid4()), email, entry, sentiment, str(datetime.date.today())))
    conn.commit()
    conn.close()

def fetch_entries(email, sentiment_filter=None, start_date=None, end_date=None):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    query = """
        SELECT entry, sentiment, date FROM journal_entries
        WHERE email = ?
    """
    params = [email]

    if sentiment_filter and sentiment_filter != "All":
        query += " AND sentiment = ?"
        params.append(sentiment_filter)

    if start_date and end_date:
        query += " AND date BETWEEN ? AND ?"
        params.extend([start_date, end_date])

    rows = cursor.execute(query, params).fetchall()
    conn.close()
    return rows

def journaling_app():
    set_background("mint.png")  # Use your background image path or comment this line
    st.markdown(
        """
        <style>
        /* Text area input text */
        textarea.stTextArea > div > textarea {
            color: white !important;
            background-color: #222222 !important;
        }

        /* Text inside expander header */
        button[aria-expanded] {
            color: white !important;
        }

        /* Text inside expander content */
        .streamlit-expanderContent p, .streamlit-expanderContent div {
            color: white !important;
        }

        /* General Streamlit text */
        .stTextArea, .css-1d391kg, .stMarkdown, .css-1v0mbdj {
            color: white !important;
        }

        /* Placeholder text in textarea */
        textarea::placeholder {
            color: #ccc !important;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
    email = st.session_state.get("user_email")
    if not email:
        st.warning("⚠️ Please login from the main page to access your journal.")
        st.stop()

    st.title("📝 My Journal")
    st.markdown("Write about your day, thoughts, or anything you'd like to reflect on.")

    with st.form("journal_form"):
        journal_text = st.text_area("How are you feeling today?", height=200)
        submitted = st.form_submit_button("Submit Entry")

    if submitted and journal_text.strip():
        sentiment = analyze_sentiment(journal_text)
        save_entry(email, journal_text, sentiment)
        st.success(f"Entry saved! Sentiment: **{sentiment}**")

    st.markdown("---")
    st.subheader("📖 Your Journal Entries")

    filter_sentiment = st.selectbox("Filter by Sentiment", ["All", "Positive", "Neutral", "Negative"])

    col1, col2 = st.columns(2)
    with col1:
        start_date = st.date_input("Start Date", value=datetime.date.today().replace(day=1))
    with col2:
        end_date = st.date_input("End Date", value=datetime.date.today())

    entries = fetch_entries(email, sentiment_filter=filter_sentiment, start_date=start_date, end_date=end_date)

    if not entries:
        st.info("No entries found for selected filters.")
    else:
        for entry, sentiment, date in entries:
            with st.expander(f"{date} - Mood: {sentiment}"):
                st.write(entry)

init_journal_db()
journaling_app()

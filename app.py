import streamlit as st
from utils.auth import get_authenticator
from utils.session_helper import is_connected

st.set_page_config(
    page_title="Job Bank",
    page_icon="💼",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Initialize authenticator and check auth status
authenticator = get_authenticator()
authenticator.check_authentification()

# --- ALREADY LOGGED IN: Redirect to Job Board ---
if is_connected():
    st.switch_page("pages/job_board.py")

# --- NOT LOGGED IN: Simple Landing Page ---

st.write("")
st.write("")

# Logo / Title
st.markdown("## 💼 Job Bank")
st.write("Track your job applications in one place.")

st.write("")

# Sign in card
with st.container(border=True):
    st.write("**Sign in to continue**")
    st.write("")

    authorization_url = authenticator.get_authorization_url()
    st.markdown(
        f'''
        <a href="{authorization_url}" target="_self" style="
            display: inline-block;
            width: 100%;
            padding: 0.5rem 1rem;
            background-color: #FF4B4B;
            color: white;
            text-align: center;
            text-decoration: none;
            border-radius: 0.5rem;
            font-weight: 500;
        ">Continue with Google</a>
        ''',
        unsafe_allow_html=True
    )

st.write("")
st.write("")

# Simple feature list
st.caption("What you can do:")
st.markdown("""
- :material/search: Search jobs with custom queries
- :material/track_changes: Track application status
- :material/filter_list: Filter by company & status
""")

# Footer
st.divider()
st.caption("© 2025 Jonathan Mehmannavaz. All rights reserved.")

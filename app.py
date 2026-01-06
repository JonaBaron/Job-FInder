import streamlit as st
from auth import get_authenticator, check_auth, logout

st.set_page_config(
    page_title="Job Bank - Login",
    page_icon="🔐",
    layout="centered"
)

# Initialize authenticator and check auth status
authenticator = get_authenticator()
authenticator.check_authentification()

# --- ALREADY LOGGED IN ---
if st.session_state.get('connected', False):
    user_info = st.session_state.get('user_info', {})
    
    st.title("Job Bank App 📋")
    st.success(f"✅ Logged in as {user_info.get('name', 'User')}")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.image(user_info.get('picture', ''), width=100)
    
    with col2:
        st.write(f"**Name:** {user_info.get('name', 'N/A')}")
        st.write(f"**Email:** {user_info.get('email', 'N/A')}")
    
    st.divider()
    
    # Navigation to main app
    if st.button("🚀 Go to Job Board", type="primary", use_container_width=True):
        st.switch_page("pages/1_job_board.py")
    
    st.divider()
    
    if st.button("🚪 Logout", use_container_width=True):
        logout()
        st.rerun()

# --- NOT LOGGED IN ---
else:
    st.title("Job Bank App 📋")
    st.write("Welcome! Please sign in to continue.")
    
    st.divider()
    
    # Centered login button
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        authorization_url = authenticator.get_authorization_url()
        st.link_button(
            "🔐 Sign in with Google", 
            authorization_url,
            use_container_width=True,
            type="primary"
        )
    
    st.divider()
    
    st.info("ℹ️ This app helps you find and track job listings. Sign in to get started!")
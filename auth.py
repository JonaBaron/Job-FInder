import streamlit as st
from streamlit_google_auth import Authenticate
import os
from dotenv import load_dotenv

load_dotenv()

def get_authenticator():
    """Create and return the authenticator instance."""
    return Authenticate(
        secret_credentials_path='google_credentials.json',
        cookie_name='job_bank_auth',
        cookie_key=os.getenv('COOKIE_SECRET', 'change_this_secret_key'),
        redirect_uri=os.getenv('REDIRECT_URI', 'http://localhost:8501'),
    )

def check_auth():
    """Check if user is authenticated. Returns True if logged in."""
    authenticator = get_authenticator()
    authenticator.check_authentification()
    return st.session_state.get('connected', False)

def require_auth():
    """Require authentication to access page. Stops execution if not logged in."""
    if not check_auth():
        st.warning("⚠️ Please log in from the Home page to access this content.")
        st.switch_page("app.py")
        st.stop()

def get_user_info():
    """Get current user info."""
    return st.session_state.get('user_info', {})

def logout():
    """Log out the current user."""
    authenticator = get_authenticator()
    authenticator.logout()
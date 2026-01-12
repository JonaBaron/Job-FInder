import streamlit as st
from streamlit_google_auth import Authenticate
import os
import json
from pathlib import Path
from dotenv import load_dotenv
from utils.session_helper import is_connected, sync_user_to_db

load_dotenv()

def get_credentials_path():
    """Get the path to Google credentials, creating from secrets if on Streamlit Cloud."""
    local_path = Path('google_credentials.json')

    # If local file exists, use it
    if local_path.exists():
        return str(local_path)

    # On Streamlit Cloud: create credentials file from secrets
    if 'google_credentials' in st.secrets:
        credentials = dict(st.secrets['google_credentials'])
        # Convert nested AttrDict to regular dict
        if 'web' in credentials:
            credentials['web'] = dict(credentials['web'])
            if 'redirect_uris' in credentials['web']:
                credentials['web']['redirect_uris'] = list(credentials['web']['redirect_uris'])
            if 'javascript_origins' in credentials['web']:
                credentials['web']['javascript_origins'] = list(credentials['web']['javascript_origins'])

        # Write to temp file
        temp_path = Path('/tmp/google_credentials.json')
        temp_path.write_text(json.dumps(credentials))
        return str(temp_path)

    raise FileNotFoundError("Google credentials not found. Add google_credentials.json locally or configure Streamlit secrets.")

def get_authenticator():
    """Get or create the authenticator instance (cached in session state)."""
    if 'authenticator' not in st.session_state:
        st.session_state.authenticator = Authenticate(
            secret_credentials_path=get_credentials_path(),
            cookie_name='job_bank_auth',
            cookie_key=os.getenv('COOKIE_SECRET', st.secrets.get('COOKIE_SECRET', 'change_this_secret_key')),
            redirect_uri=os.getenv('REDIRECT_URI', st.secrets.get('REDIRECT_URI', 'http://localhost:8501')),
        )
    return st.session_state.authenticator

def check_auth():
    """Check if user is authenticated. Returns True if logged in."""
    authenticator = get_authenticator()
    authenticator.check_authentification()

    # Sync user to MongoDB if connected
    if is_connected():
        sync_user_to_db()

    return is_connected()

def require_auth():
    """Require authentication to access page. Stops execution if not logged in."""
    if not check_auth():
        st.warning("⚠️ Please log in from the Home page to access this content.")
        st.switch_page("app.py")
        st.stop()

def logout():
    """Log out the current user."""
    authenticator = get_authenticator()
    authenticator.logout()
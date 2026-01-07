import streamlit as st
from utils.db_user import (
    get_or_create_user,
    get_user_by_email,
    update_user_jsearch_api,
    update_user_mongo_uri,
    get_user_jsearch_api,
    get_user_mongo_uri,
    has_user_configured_api,
    has_user_configured_mongo,
    update_user_profile
)

# ============================================
# DEFAULT VALUES
# ============================================
DEFAULTS = {
    # Authentication
    'connected': False,
    'user_info': {},

    # User queries
    'queries': ["Montreal"],

    # API settings (loaded from MongoDB per-user)
    'JSearch_API_name': "",
    'JSearch_API_value': "",
    'MongoDB_Api_value': "",  # User's personal MongoDB URI for job storage

    # Display settings
    'items_per_row': 2,
    'num_of_jobs_to_find': 25,

    # Data storage
    'jobs': [],
    'companies': [],
}

# ============================================
# INITIALIZATION
# ============================================
def initialize_session_state():
    """Initialize all session state keys with defaults."""
    for key, default in DEFAULTS.items():
        if key not in st.session_state:
            st.session_state[key] = default

    # Special case: jobs list depends on queries length
    if st.session_state.jobs == []:
        st.session_state.jobs = [[] for _ in range(len(st.session_state.queries))]

    return st.session_state

def set_api_keys_in_session():
    """Initialize API key session values (loaded from DB on login)."""
    # API keys are now per-user and loaded from MongoDB on login
    # This just ensures the session keys exist with empty defaults
    if 'JSearch_API_name' not in st.session_state:
        set_value('JSearch_API_name', "")
    if 'JSearch_API_value' not in st.session_state:
        set_value('JSearch_API_value', "")
    if 'MongoDB_Api_value' not in st.session_state:
        set_value('MongoDB_Api_value', "")

# ============================================
# GETTERS & SETTERS
# ============================================
def get_value(key, default=None):
    """Get a value from session state with optional default."""
    return st.session_state.get(key, default if default is not None else DEFAULTS.get(key))

def set_value(key, value):
    """Set a value in session state."""
    st.session_state[key] = value

def has_key(key):
    """Check if a key exists in session state."""
    return key in st.session_state

# ============================================
# DATA HELPERS
# ============================================
def get_queries():
    return get_value('queries')

def set_queries(queries):
    set_value('queries', queries)

def add_query(query):
    queries = get_queries()
    if query not in queries:
        queries.append(query)
        set_queries(queries)

def remove_query(query):
    queries = get_queries()
    if query in queries:
        queries.remove(query)
        set_queries(queries)

def get_jobs(query_idx=None):
    jobs = get_value('jobs')
    if query_idx is not None:
        while len(jobs) <= query_idx:
            jobs.append([])
        return jobs[query_idx]
    return jobs

def set_jobs(jobs, query_idx=None):
    if query_idx is not None:
        all_jobs = get_value('jobs')
        while len(all_jobs) <= query_idx:
            all_jobs.append([])
        all_jobs[query_idx] = jobs
        set_value('jobs', all_jobs)
    else:
        set_value('jobs', jobs)

def get_companies():
    return get_value('companies')

def set_companies(companies):
    set_value('companies', companies)

def delete_job(job_id):
    """Delete a job by its ID from all query lists."""
    jobs = get_value('jobs')
    for query_idx, query_jobs in enumerate(jobs):
        jobs[query_idx] = [job for job in query_jobs if job.id != job_id]
    set_value('jobs', jobs)

# ============================================
# AUTH HELPERS
# ============================================
def is_connected():
    """Check if user is authenticated."""
    return get_value('connected', False)

def set_connected(value):
    """Set authentication status."""
    set_value('connected', value)

def get_user_info():
    """Get current user info dictionary."""
    return get_value('user_info', {})

def set_user_info(info):
    """Set user info dictionary."""
    set_value('user_info', info)

def get_user_name():
    """Get current user's name."""
    return get_user_info().get('name', 'User')

def get_user_email():
    """Get current user's email."""
    return get_user_info().get('email', '')

def get_user_picture():
    """Get current user's profile picture URL."""
    return get_user_info().get('picture', '')

# ============================================
# SETTINGS HELPERS
# ============================================
def get_items_per_row():
    return get_value('items_per_row')

def set_items_per_row(value):
    set_value('items_per_row', value)

def get_num_jobs_to_find():
    return get_value('num_of_jobs_to_find')

def set_num_jobs_to_find(value):
    set_value('num_of_jobs_to_find', value)

# ============================================
# RESET HELPERS
# ============================================
def reset_key(key):
    """Reset a specific key to its default value."""
    if key in DEFAULTS:
        st.session_state[key] = DEFAULTS[key]

def reset_all():
    """Reset all session state to defaults."""
    for key, default in DEFAULTS.items():
        st.session_state[key] = default

# ============================================
# MONGODB USER SYNC
# ============================================
def sync_user_to_db():
    """
    Sync current user to MongoDB on login.
    Creates user if not exists, loads their settings into session.
    """
    if not is_connected():
        return False

    email = get_user_email()
    if not email:
        return False

    # Get or create user in MongoDB
    user = get_or_create_user(
        email=email,
        name=get_user_name(),
        picture=get_user_picture()
    )

    if user:
        # Load user's API settings into session state
        load_user_settings_from_db(email)
        return True
    return False


def load_user_settings_from_db(email: str = None):
    """Load user's API keys and MongoDB URI from database into session."""
    if email is None:
        email = get_user_email()
    if not email:
        return

    # Load JSearch API settings
    api_name, api_key = get_user_jsearch_api(email)
    if api_key:
        set_value('JSearch_API_name', api_name or "")
        set_value('JSearch_API_value', api_key)

    # Load MongoDB URI
    mongo_uri = get_user_mongo_uri(email)
    if mongo_uri:
        set_value('MongoDB_Api_value', mongo_uri)


def save_jsearch_api_to_db(api_key: str, api_name: str = "x-rapidapi-key") -> bool:
    """Save user's JSearch API key to MongoDB."""
    email = get_user_email()
    if not email:
        return False

    success = update_user_jsearch_api(email, api_key, api_name)
    if success:
        set_value('JSearch_API_name', api_name)
        set_value('JSearch_API_value', api_key)
    return success


def save_mongo_uri_to_db(mongo_uri: str) -> bool:
    """Save user's personal MongoDB URI to database."""
    email = get_user_email()
    if not email:
        return False

    success = update_user_mongo_uri(email, mongo_uri)
    if success:
        set_value('MongoDB_Api_value', mongo_uri)
    return success


def user_has_jsearch_api() -> bool:
    """Check if current user has configured JSearch API."""
    email = get_user_email()
    if not email:
        return False
    return has_user_configured_api(email)


def user_has_mongo_uri() -> bool:
    """Check if current user has configured their MongoDB URI."""
    email = get_user_email()
    if not email:
        return False
    return has_user_configured_mongo(email)


def get_user_mongo_uri_from_session() -> str:
    """Get the user's MongoDB URI from session state."""
    return get_value('MongoDB_Api_value', '')


def get_jsearch_api_from_session() -> tuple:
    """Get JSearch API credentials from session. Returns (api_name, api_key)."""
    return get_value('JSearch_API_name', ''), get_value('JSearch_API_value', '')


# ============================================
# AUTO-INITIALIZE ON IMPORT
# ============================================
initialize_session_state()
set_api_keys_in_session()

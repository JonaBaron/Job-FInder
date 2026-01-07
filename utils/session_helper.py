import streamlit as st
import os
from dotenv import load_dotenv

# ============================================
# DEFAULT VALUES
# ============================================
DEFAULTS = {
    # Authentication
    'connected': False,
    'user_info': {},

    # User queries
    'queries': ["Montreal"],

    # API settings
    'JSearch_API_name': "",
    'JSearch_API_value': "",
    'MongoDB_Api_name': "",
    'MongoDB_Api_value': "",

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
    """Load API keys from environment variables."""
    load_dotenv()
    set_value('JSearch_API_name', os.getenv("JSearch_API_name", ""))
    set_value('JSearch_API_value', os.getenv("JSearch_API_value", ""))
    set_value('MongoDB_Api_name', os.getenv("MongoDB_Api_name", ""))
    set_value('MongoDB_Api_value', os.getenv("MongoDB_Api_value", ""))

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
# AUTO-INITIALIZE ON IMPORT
# ============================================
initialize_session_state()
set_api_keys_in_session()

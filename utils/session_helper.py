import streamlit as st
import os
from dotenv import load_dotenv

def initialize_session_state():
    # Queries default
    if 'queries' not in st.session_state:
        st.session_state.queries = ["Montreal"]
    # Settings defaults
    if 'JSearch_API_name' not in st.session_state:
        st.session_state.JSearch_API_name = ""
    if 'JSearch_API_value' not in st.session_state:
        st.session_state.JSearch_API_value = ""
    if 'MongoDB_Api_name' not in st.session_state:
        st.session_state.MongoDB_Api_name = ""
    if 'MongoDB_Api_value' not in st.session_state:
        st.session_state.MongoDB_Api_value = ""
    # Items per row default
    if 'items_per_row' not in st.session_state:
        st.session_state.items_per_row = 2
    # Jobs to find default
    if 'num_of_jobs_to_find' not in st.session_state:
        st.session_state.num_of_jobs_to_find = 25
    # Jobs per default
    if 'jobs' not in st.session_state:
        st.session_state.jobs = [[] for _ in range(len(st.session_state.queries))]
    # List of compagnies
    if 'companies' not in st.session_state:    
        st.session_state.companies = []
    
    return st.session_state


def set_api_keys_in_session():
    load_dotenv()
    st.session_state.JSearch_API_name = os.getenv("JSearch_API_name", "")
    st.session_state.JSearch_API_value = os.getenv("JSearch_API_value", "")
    st.session_state.MongoDB_Api_name = os.getenv("MongoDB_Api_name", "")
    st.session_state.MongoDB_Api_value = os.getenv("MongoDB_Api_value", "")

# Initialize FIRST, then set API keys
initialize_session_state()
set_api_keys_in_session()

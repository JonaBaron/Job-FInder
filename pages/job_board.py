import streamlit as st
from models.job import *
from components.job_card import *
from utils.job_finder import *
from components.dialog import *
from utils.session_helper import *
from utils.auth import logout
from natsort import natsorted

st.set_page_config(
    page_title="Job Bank",
    page_icon="📋",
    layout="wide"
)

# Session state initialization
state = initialize_session_state()
if state is None:
    st.error("Error initializing session state.")
    st.stop()

# ============================================
# SIDEBAR
# ============================================
# User profile section
if is_connected():
    with st.sidebar:
        col1, col2 = st.columns([1, 3])
        with col1:
            st.image(get_user_picture(), width=50)
        with col2:
            st.markdown(f"**{get_user_name()}**")
            st.caption(get_user_email())
        st.divider()

st.sidebar.title("Menu")

# Queries dialog
if st.sidebar.button("My Querries 📋"):
    my_queries_dialog()

# Analytics dialog
if st.sidebar.button("Analytics 📊"):
    st.warning("Analytics page is under development. Stay tuned!")

# Settings dialog
if st.sidebar.button("Settings ⚙️"):
    settings_dialog()

# Info dialog
if st.sidebar.button("Info ℹ️"):
    info_dialog()

#-- FILTERS ----------
# filter by status
st.sidebar.title("Filters")
st.sidebar.selectbox("Sort by status", 
    options=["All", "New - Not Viewed", "New - Viewed", "Applied", "Under Review", "Interview Scheduled", "Shortlisted", 
             "Rejected", "Offered", "Accepted", "Declined"],
    key="sort_status"
)

## IMPLEMENT COMPANY FILTER LATER
# filter by company
st.sidebar.selectbox("Filter by company", 
    options = ["All"] + state.companies,
    key="target_company"
)


# Number of Jobs per page
state.num_of_jobs_to_find = st.sidebar.number_input("Number of jobs to find", min_value=1, max_value=250, value=25, step=1)

# Job per line
state.items_per_row = st.sidebar.number_input("Jobs per line", min_value=1, max_value=6, value=2, step=1)

# Logout button
if st.sidebar.button("Logout", icon=":material/logout:", use_container_width=True):
    logout()
    st.switch_page("app.py")

# ============================================
# MAIN PAGE HEADER
# ============================================
# Welcome header
col_title, col_action = st.columns([4, 1])
with col_title:
    st.title("Job Board")
    if is_connected():
        st.markdown(f"Welcome back, **{get_user_name()}**!")
    else:
        st.markdown("Find your next opportunity")

with col_action:
    st.write("")  # Spacing
    if st.button("Refresh", icon=":material/refresh:", type="primary", use_container_width=True):
        # Clear jobs to force refresh
        state.jobs = [[] for _ in range(len(state.queries))]
        st.rerun()

# Quick stats
total_jobs = sum(len(jobs) for jobs in state.jobs)
active_queries = len(state.queries)

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Total Jobs", total_jobs)
with col2:
    st.metric("Active Queries", active_queries)
with col3:
    st.metric("Jobs per Page", state.num_of_jobs_to_find)
with col4:
    st.metric("Grid Layout", f"{state.items_per_row} cols")

st.divider()

# ============================================
# JOB LISTINGS
# ============================================
items_per_row = state.items_per_row

# Check if API is configured
if not is_api_configured():
    st.warning("Please configure your JSearch API key in Settings to search for jobs.")

for query_idx, query in enumerate(state.queries):
    with st.expander(f"**{query}** - Job Results", expanded=True):

        # Ensure jobs list is long enough for this query index
        while len(state.jobs) <= query_idx:
            state.jobs.append([])

        # Load jobs if empty
        if state.jobs[query_idx] == []:
            if not is_api_configured():
                st.info("Configure your API key in Settings to load jobs.")
            else:
                with st.spinner(f"Searching jobs for '{query}'..."):
                    state.jobs[query_idx] = find_jobs(query, 1, query_idx)

        # Get jobs for this query
        query_jobs = state.jobs[query_idx]

        # Update company list for filters
        state.companies = natsorted({job.get_company() for job in query_jobs})

        # Show job count for this query
        st.caption(f"Found **{len(query_jobs)}** jobs")

        # Filter by company
        company_target = state.get("target_company", "All")
        if company_target == "All":
            filtered_jobs = query_jobs
        else:
            filtered_jobs = [job for job in query_jobs if job.get_company() == company_target]
        
        # Filter by status
        sort_status = state.get("sort_status", "All")
        if sort_status != "All":
            target_status = status.get_status_num(sort_status)
            filtered_jobs = [job for job in filtered_jobs if job.get_status() == target_status]

        # Show filtered count if different from total
        if len(filtered_jobs) != len(query_jobs):
            st.caption(f"Showing **{len(filtered_jobs)}** of {len(query_jobs)} (filtered)")

        # Handle no results
        if not filtered_jobs:
            st.info("No jobs match your current filters. Try adjusting the filters in the sidebar.")
            continue

        total_items = min(state.num_of_jobs_to_find, len(filtered_jobs))
        
        # Now create grid with only filtered jobs
        for row in range(0, total_items, items_per_row):
            cols = st.columns(items_per_row)
            
            for i, col in enumerate(cols):
                item_num = row + i
                if item_num < total_items:
                    with col:
                        display_job = filtered_jobs[item_num]
                        display_job_card(display_job) 
                        if display_job.status == status.ACCEPTED or display_job.status == status.OFFERED:
                            st.balloons()
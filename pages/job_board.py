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
# HELPER FUNCTIONS
# ============================================
def load_more_jobs(query_idx, query):
    """Load more jobs for a specific query and append to existing jobs."""
    from utils.session_helper import get_pages_loaded, set_pages_loaded

    pages_per_load = 10  # Load 10 pages at once (up to 100 jobs per API call)
    current_pages = get_pages_loaded(query_idx)
    next_page = current_pages + 1

    new_jobs = find_jobs(query, pages_per_load, page=next_page)

    # Append new jobs, avoiding duplicates by link
    if new_jobs:
        existing_links = {job.get_WEBLink() for job in state.jobs[query_idx]}
        unique_jobs = [job for job in new_jobs if job.get_WEBLink() not in existing_links]
        state.jobs[query_idx].extend(unique_jobs)
        set_pages_loaded(query_idx, current_pages + pages_per_load)

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


# Number of Jobs to display
jobs_display_options = ["25", "50", "100", "200", "All"]
selected_display = st.sidebar.selectbox(
    "Jobs to display",
    options=jobs_display_options,
    index=0,
    key="jobs_display_select"
)

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
        # Clear jobs and pages_loaded to force refresh
        state.jobs = [[] for _ in range(len(state.queries))]
        state.pages_loaded = [0 for _ in range(len(state.queries))]
        st.rerun()

st.divider()

# ============================================
# JOB LISTINGS
# ============================================
items_per_row = state.items_per_row

# Check if API is configured
if not is_api_configured():
    st.warning("Please configure your JSearch API key in Settings to search for jobs.")

# Track seen job links to avoid showing duplicates across queries
seen_job_links = set()

for query_idx, query in enumerate(state.queries):
    with st.expander(f"**{query}** - Job Results", expanded=True):

        # Ensure jobs list is long enough for this query index
        while len(state.jobs) <= query_idx:
            state.jobs.append([])

        # Ensure pages_loaded list is long enough
        while len(state.pages_loaded) <= query_idx:
            state.pages_loaded.append(0)

        # Load jobs if empty (initial load with 10 pages = up to 100 jobs)
        if state.jobs[query_idx] == []:
            if not is_api_configured():
                st.info("Configure your API key in Settings to load jobs.")
            else:
                with st.spinner(f"Searching jobs for '{query}'..."):
                    pages_per_load = 10
                    state.jobs[query_idx] = find_jobs(query, pages_per_load, page=1)
                    state.pages_loaded[query_idx] = pages_per_load

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

        # Filter out duplicates (jobs already shown in previous queries)
        unique_jobs = [job for job in filtered_jobs if job.get_WEBLink() not in seen_job_links]
        duplicates_hidden = len(filtered_jobs) - len(unique_jobs)
        filtered_jobs = unique_jobs

        # Show filtered count if different from total
        if len(filtered_jobs) != len(query_jobs) or duplicates_hidden > 0:
            filter_msg = f"Showing **{len(filtered_jobs)}** of {len(query_jobs)}"
            if duplicates_hidden > 0:
                filter_msg += f" ({duplicates_hidden} duplicates hidden)"
            st.caption(filter_msg)

        # Handle no results
        if not filtered_jobs:
            st.info("No jobs match your current filters. Try adjusting the filters in the sidebar.")
            continue

        # Calculate total items to display based on selection
        if selected_display == "All":
            total_items = len(filtered_jobs)
        else:
            total_items = min(int(selected_display), len(filtered_jobs))
        
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

        # Add displayed jobs to seen set to hide them in subsequent queries
        for job in filtered_jobs[:total_items]:
            seen_job_links.add(job.get_WEBLink())

        # Load More button - fetches 10 more pages (up to 100 jobs) per click
        st.divider()
        col_load, col_info = st.columns([1, 2])
        with col_load:
            if st.button(
                "Load More Jobs",
                key=f"load_more_{query_idx}",
                type="secondary",
                use_container_width=True,
                icon=":material/add:"
            ):
                with st.spinner(f"Loading more jobs for '{query}'..."):
                    load_more_jobs(query_idx, query)
                st.rerun()
        with col_info:
            pages_loaded = state.pages_loaded[query_idx] if query_idx < len(state.pages_loaded) else 0
            st.caption(f"Pages loaded: {pages_loaded} | Jobs: {len(query_jobs)} | Each click loads ~100 more jobs")

# ============================================
# FOOTER
# ============================================
st.divider()
st.caption("© 2025 Jonathan Mehmannavaz. All rights reserved.")
import streamlit as st
from models.job import *
from components.job_card import *
from utils.job_finder import *
import os
from dotenv import load_dotenv
from components.dialog import *
from utils.session_helper import *
from natsort import natsorted

## to implement later
# db
# csv
# balloons: st.balloons()

st.set_page_config(
    page_title="Job Bank",
    page_icon="📋",
    layout= "wide"
)

#--session state initialization --

state = initialize_session_state()
if state is None:
    st.error("Error initializing session state.")
    st.stop()


#-- SIDEBAR ----------
# Dialog buttons menu
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


# Number of Jobs
state.num_of_jobs_to_find = st.sidebar.number_input("Number of jobs to find", min_value=1, max_value=250, value=25, step=1)

# Job per line
state.items_per_row = st.sidebar.number_input("Jobs per line", min_value=1, max_value=6, value=2, step=1)

#Button to log out
if st.sidebar.button("Logout", icon=":material/logout:"):
    st.sidebar.write("adsfdf")

# ---------- Main page ----------

st.title("Job bank App 📋")

with st.container(horizontal=True):
    st.write("This app helps you find job listings.")
    st.button("Refresh 🎲")

# # Dummy data to demonstrate layout
# # 100 elements
items_per_row = state.items_per_row

for query_idx, query in enumerate(state.queries):
    with st.expander("Querying jobs for: " + query):
        
        # Ensure jobs list is long enough for this query index
        while len(state.jobs) <= query_idx:
            state.jobs.append([])
        
        # Check if THIS query's jobs are empty
        if state.jobs[query_idx] == []:
            st.toast("refresh")
            state.jobs[query_idx] = find_jobs(query,1,query_idx)
        else:
            st.toast("no refresh")
        
        # Get jobs for THIS query
        query_jobs = state.jobs[query_idx]
        
        # List and sort the company names (from this query's jobs)
        state.companies = natsorted({job.get_company() for job in query_jobs})
   
        # Sort by company
        company_target = state.get("target_company", "All")
        if company_target == "All":
            filtered_jobs = query_jobs
        else:
            filtered_jobs = [job for job in query_jobs if job.get_company() == company_target]
        
        # Sort by status
        sort_status = state.get("sort_status", "All")
        if sort_status == "All":
            filtered_jobs = filtered_jobs
        else:
            target_status = status.get_status_num(sort_status)
            filtered_jobs = [job for job in filtered_jobs if job.get_status() == target_status]
            if not filtered_jobs: 
                st.warning("No job found with your criteria")
 
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


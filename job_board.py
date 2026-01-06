import streamlit as st
from job import *
from job_card import *
from job_finder import *
import os
from dotenv import load_dotenv
from dialog import *
from session import *
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
st.sidebar.title("Pages")

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
st.sidebar.number_input("Number of jobs to find", min_value=1, max_value=250, value=25, step=1, key="num_of_jobs_to_find")

## Job per line
st.sidebar.number_input("Jobs per line", min_value=1, max_value=3, value=2, step=1, key="items_per_row")

# ---------- Main page ----------

st.title("Job bank App 📋")

with st.container(horizontal=True):
    st.write("This app helps you find job listings.")
    st.button("Refresh 🎲")

# # Dummy data to demonstrate layout
# # 100 elements
items_per_row = state.items_per_row

for query_idx, query in enumerate(state.queries):
    with st.status("Querying jobs for: " + query):
        # Find jobs to a querry
        state.jobs = dummy_find_jobs(query_idx)
        
        # List and sort the company names
        state.companies = natsorted({job.get_company() for job in state.jobs})
   
        # Sort by compagny
        company_target = state.get("target_company", "All")
        if company_target == "All":
            filtered_jobs = state.jobs
        else:
            filtered_jobs = [job for job in state.jobs if job.get_company() == company_target]


        # Sort by status
        sort_status = state.get("sort_status", "All")
        if sort_status == "All":
            filtered_jobs = filtered_jobs
        else:
            target_status = status.get_status_num(sort_status)
            filtered_jobs = [job for job in filtered_jobs if job.get_status() == target_status]
            if not filtered_jobs: 
                st.warning("No job found with your critearia")
 
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
                        # small animation
                        if display_job.status == status.ACCEPTED or display_job.status == status.OFFERED:
                            st.balloons()


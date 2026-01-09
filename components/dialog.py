import streamlit as st
import os
from dotenv import load_dotenv
from utils.session_helper import (
    get_queries, set_queries, get_jobs, set_jobs, get_value, set_value,
    save_jsearch_api_to_db, is_connected, get_user_email
)
from utils.db_jobs import sync_jobs_to_db

#Info dialog
@st.dialog("Info ℹ️")
def info_dialog():
    st.write("# Job Bank")
    st.write("### Made by Jonathan Mehmannavaz")
    st.write("""
    ## An app made with intention

    This Job Bank App is designed to help users find and manage job listings efficiently. Below are some key features and information about the app:

    ### Features:
    - **Job Search**: Find job listings based on your queries
    - **Job Status Tracking**: Keep track of the status of each job application
    - **Custom Queries**: Add and manage your own job search queries
    - **Filters**: Sort and filter job listings based on status and company
    - **Load More**: Efficiently load more jobs with pagination

    ### How to Use:
    1. Sign in with your Google account
    2. Configure your API keys in Settings
    3. Add job search queries in "My Queries"
    4. Browse and track your job applications

    ### Follow Me!
    """)
    with st.container(horizontal=True):
        st.link_button("GitHub", icon=":material/code:", url="https://github.com/JonaBaron")
        st.link_button("LinkedIn", icon=":material/work:", url="https://www.linkedin.com/in/jonathan-mehmannavaz/")
        st.link_button("Webpage", icon=":material/web:", url="https://jonabaron.github.io/")

    st.divider()
    st.caption("© 2025 Jonathan Mehmannavaz. All rights reserved.")
    st.caption("Licensed under the MIT License.")
   
@st.dialog("My Queries 📋")
def my_queries_dialog():
    queries = get_queries()
    jobs = get_jobs()
    to_delete = None

    for i, q in enumerate(queries):
        col_input, col_btn = st.columns([5, 1])
        with col_input:
            queries[i] = st.text_input(
                f"Query {i+1}", value=q, key=f"prev_query_{id(q)}_{i}"
            )
        with col_btn:
            st.write("")
            if st.button("", icon=":material/delete:", key=f"delete_{id(q)}_{i}"):
                to_delete = i

    if to_delete is not None:
        queries.pop(to_delete)
        jobs.pop(to_delete)
        set_queries(queries)
        set_jobs(jobs)
        # Sync to DB after deleting query
        email = get_user_email()
        if email:
            sync_jobs_to_db(email, queries, jobs)
        st.rerun()

    user_input = st.text_input("Add a query to your list:", key="new_query")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Add Query"):
            if user_input.strip():
                queries.append(user_input)
                jobs.append([])
                set_queries(queries)
                set_jobs(jobs)
                # Sync to DB after adding query
                email = get_user_email()
                if email:
                    sync_jobs_to_db(email, queries, jobs)
                st.success("Query added successfully!")
                st.rerun()
            else:
                st.warning("Please enter a query first.")
    with col2:
        if st.button("Submit Queries"):
            st.rerun()

#Settings dialog
@st.dialog("Settings ⚙️")
def settings_dialog():
    load_dotenv()

    if not is_connected():
        st.error("Please log in to save settings.")
        return

    st.write("## API Key Configuration")

    # JSearch Section
    st.write("### JSearch Key Configuration")
    jsearch_api_name = st.text_input(
        "Enter your JSearch api name",
        placeholder="ex: x-api-key",
        value=get_value("JSearch_API_name", ""),
        key="Api_name"
    )
    jsearch_api_value = st.text_input(
        "Enter your JSearch api key",
        placeholder="ex: your_api_key_12345",
        value=get_value("JSearch_API_value", ""),
        key="Api_value",
        type="password"
    )
    st.write("You can get your API key from [here](https://www.openwebninja.com/jsearch).")

    if st.button("Save JSearch API", use_container_width=True):
        if jsearch_api_value:
            api_name = jsearch_api_name if jsearch_api_name else "x-rapidapi-key"
            save_jsearch_api_to_db(jsearch_api_value, api_name)
            # Clear jobs and pages_loaded to trigger fresh fetch with new API key
            queries = get_queries()
            set_jobs([[] for _ in range(len(queries))])
            set_value('pages_loaded', [0 for _ in range(len(queries))])
            st.success("JSearch API saved! Refreshing jobs...")
            st.rerun()
        else:
            st.warning("Please enter an API key.")


# Edit Link dialog
@st.dialog("Edit Job Link")
def edit_link_dialog(job_instance, query_idx: int):
    """Dialog to edit a job's link when the original doesn't work."""
    from utils.db_jobs import update_job_link
    from utils.session_helper import get_user_email

    st.write(f"**{job_instance.get_title()}**")
    st.caption(f"{job_instance.get_company()}")

    st.write("**Current Link:**")
    current_link = job_instance.get_WEBLink()
    st.code(current_link if current_link else "No link available")

    new_link = st.text_input(
        "Enter new link:",
        placeholder="https://example.com/job/apply",
        key="new_job_link"
    )

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Cancel", use_container_width=True):
            st.rerun()
    with col2:
        if st.button("Save Link", use_container_width=True, type="primary"):
            if new_link.strip():
                old_link = current_link
                job_instance.set_WEBLink(new_link.strip())

                # Save to database
                email = get_user_email()
                if email:
                    update_job_link(email, query_idx, job_instance.id, old_link, new_link.strip())

                st.success("Link updated!")
                st.rerun()
            else:
                st.warning("Please enter a valid URL.")

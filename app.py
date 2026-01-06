import streamlit as st
from job import status
from job_card import *
from job_finder import find_jobs
import os
from dotenv import load_dotenv
from dialog import *
## to implement later
# db
# csv
# balloons: st.balloons()

#-- SIDEBAR ----------

st.session_state.queries = ["Computer Engineering - Canada - internship", "Electrical Engineering - Canada - internship",
             "Software Engineering - Canada - internship", "Data Science - Canada - internship"]

st.sidebar.title("Pages")
#Option 1
if st.sidebar.button("My Querries 📋"):
    my_queries_dialog()

#Option 2
if st.sidebar.button("Analytics 📊"):
    st.warning("Analytics page is under development. Stay tuned!")

if st.sidebar.button("Settings ⚙️"):
    settings_dialog()



#Option 3
if st.sidebar.button("Info ℹ️"):
    info_dialog()

#-- FILTERS ----------
st.sidebar.title("Filters")
st.sidebar.selectbox("Sort by status", 
    options=["All", "New - Not Viewed", "New - Viewed", "Applied", "Under Review", "Interview Scheduled", "Shortlisted", 
             "Rejected", "Offered", "Accepted", "Declined"],
    key="sort_status"
)

## IMPLEMENT COMPANY FILTER LATER
st.sidebar.selectbox("Filter by company", 
    options=["All", "Company A", "Company B", "Company C"],
    key="filter_company"
)

## Job per line
st.session_state.jobs_per_line = 2
st.session_state.jobs_per_line = st.sidebar.number_input("Jobs per line", min_value=1, max_value=3, value=2, step=1, key="jobs_number_per_line")

# ---------- APP ----------
st.title("Job bank App 📋")

with st.container(horizontal=True):
    st.write("This app helps you find job listings.")
    st.button("Refresh 🎲")


def display_job_card(job_instance):

    type = job_instance.get_status()

    if type == status.NEW_NOT_VIEWED:
        new_not_viewed(job_instance)
    
    elif type == status.NEW_VIEWED:
        new_viewed(job_instance)

    elif type == status.APPLIED:
        applied(job_instance)
    
    elif type == status.UNDER_REVIEW:
        under_review(job_instance)
    
    elif type == status.INTERVIEW_SCHEDULED:
        interview_scheduled(job_instance)

    elif type == status.SHORTLISTED:
        shortlisted(job_instance)

    elif type == status.REJECTED:
        rejected(job_instance)

    elif type == status.OFFERED:
        offered(job_instance)

    elif type == status.ACCEPTED:
        accepted(job_instance)

    elif type == status.DECLINED:
        declined(job_instance)


# # Dummy data to demonstrate layout
# # 100 elements, 4 per row = 25 rows

total_items = 100
items_per_row = st.session_state.jobs_per_line
for query_idx, query in enumerate(st.session_state.get('queries', ["Computer Engineering - Canada - internship"])):
    with st.status("Querying jobs for: " + query):
        for row in range(0, total_items, items_per_row):
            cols = st.columns(items_per_row)
            
            for i, col in enumerate(cols):
                item_num = row + i + 1
                if item_num <= total_items:
                    with col:
                        if item_num % 10 == 1:
                            display_job_card(job(
                            id=f"{query_idx}_{item_num}",
                            title=f"Job Title {item_num}",
                            company=f"Company {item_num}",
                            location=f"Location {item_num}",
                            link=f"http://example.com/job{item_num}",
                            status=status.NEW_NOT_VIEWED
                        ))
                        elif item_num % 10 == 2:
                            display_job_card(job(
                            id=f"{query_idx}_{item_num}",
                            title=f"Job Title {item_num}",
                            company=f"Company {item_num}",
                            location=f"Location {item_num}",
                            link=f"http://example.com/job{item_num}",
                            status=status.NEW_VIEWED
                        ))
                        elif item_num % 10 == 3:
                            display_job_card(job(
                            id=f"{query_idx}_{item_num}",
                            title=f"Job Title {item_num}",
                            company=f"Company {item_num}",
                            location=f"Location {item_num}",
                            link=f"http://example.com/job{item_num}",
                            status=status.APPLIED
                        ))
                        elif item_num % 10 == 4:
                            display_job_card(job(
                            id=f"{query_idx}_{item_num}",
                            title=f"Job Title {item_num}",
                            company=f"Company {item_num}",
                            location=f"Location {item_num}",
                            link=f"http://example.com/job{item_num}",
                            status=status.UNDER_REVIEW
                        ))
                        elif item_num % 10 == 5:
                            display_job_card(job(
                            id=f"{query_idx}_{item_num}",
                            title=f"Job Title {item_num}",
                            company=f"Company {item_num}",
                            location=f"Location {item_num}",
                            link=f"http://example.com/job{item_num}",
                            status=status.INTERVIEW_SCHEDULED
                        ))
                        elif item_num % 10 == 6:
                            display_job_card(job(
                            id=f"{query_idx}_{item_num}",
                            title=f"Job Title {item_num}",
                            company=f"Company {item_num}",
                            location=f"Location {item_num}",
                            link=f"http://example.com/job{item_num}",
                            status=status.SHORTLISTED
                        ))
                        elif item_num % 10 == 7:
                            display_job_card(job(
                            id=f"{query_idx}_{item_num}",
                            title=f"Job Title {item_num}",
                            company=f"Company {item_num}",
                            location=f"Location {item_num}",
                            link=f"http://example.com/job{item_num}",
                            status=status.REJECTED
                        ))
                        elif item_num % 10 == 8:
                            display_job_card(job(
                            id=f"{query_idx}_{item_num}",
                            title=f"Job Title {item_num}",
                            company=f"Company {item_num}",
                            location=f"Location {item_num}",
                            link=f"http://example.com/job{item_num}",
                            status=status.OFFERED
                        ))
                        elif item_num % 10 == 9:
                            display_job_card(job(
                            id=f"{query_idx}_{item_num}",
                            title=f"Job Title {item_num}",
                            company=f"Company {item_num}",
                            location=f"Location {item_num}",
                            link=f"http://example.com/job{item_num}",
                            status=status.ACCEPTED
                        ))
                        else:
                            display_job_card(job(
                            id=f"{query_idx}_{item_num}",
                            title=f"Job Title {item_num}",
                            company=f"Company {item_num}",
                            location=f"Location {item_num}",
                            link=f"http://example.com/job{item_num}",
                            status=status.DECLINED
                        ))



# list_jobs = find_jobs()

# total_items = list_jobs.__len__() 
# items_per_row = 2

# for row in range(0, total_items, items_per_row):
#     cols = st.columns(2)
    
#     for i, col in enumerate(cols):
#         item_num = row + i + 1
#         if item_num <= total_items:
#             with col:
#                 display_job_card(job(
#                     id=list_jobs[item_num - 1].id,
#                     title=list_jobs[item_num - 1].title,
#                     company=list_jobs[item_num - 1].company,
#                     location=list_jobs[item_num - 1].location,
#                     link=list_jobs[item_num - 1].link,
#                     status=list_jobs[item_num - 1].status
#                 ))
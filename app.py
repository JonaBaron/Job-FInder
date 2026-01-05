import streamlit as st
from job import status
from job_card import *
from job_finder import find_jobs

# ---------- APP ----------
st.title("Job bank App 📋")

with st.container(horizontal=True):
    st.write("This app helps you find job listings.")
    st.button("Refresh 🎲")

st.sidebar.title("Pages")
st.sidebar.button("Home 🏠")
st.sidebar.button("My Querries 📋")
st.sidebar.button("Analytics 📊")

st.sidebar.selectbox("Sort by status", 
    options=["All", "New - Not Viewed", "New - Viewed", "Applied", "Under Review", "Interview Scheduled", "Shortlisted", 
             "Rejected", "Offered", "Accepted", "Declined"],
    key="sort_status"
)



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
items_per_row = 2
with st.status("Fetching latest job listings..."):
    for row in range(0, total_items, items_per_row):
        cols = st.columns(2)
        
        for i, col in enumerate(cols):
            item_num = row + i + 1
            if item_num <= total_items:
                with col:
                    if item_num % 10 == 1:
                        display_job_card(job(
                        id=item_num,
                        title=f"Job Title {item_num}",
                        company=f"Company {item_num}",
                        location=f"Location {item_num}",
                        link=f"http://example.com/job{item_num}",
                        status=status.NEW_NOT_VIEWED
                    ))
                    elif item_num % 10 == 2:
                        display_job_card(job(
                        id=item_num,
                        title=f"Job Title {item_num}",
                        company=f"Company {item_num}",
                        location=f"Location {item_num}",
                        link=f"http://example.com/job{item_num}",
                        status=status.NEW_VIEWED
                    ))
                    elif item_num % 10 == 3:
                        display_job_card(job(
                        id=item_num,
                        title=f"Job Title {item_num}",
                        company=f"Company {item_num}",
                        location=f"Location {item_num}",
                        link=f"http://example.com/job{item_num}",
                        status=status.APPLIED
                    ))
                    elif item_num % 10 == 4:
                        display_job_card(job(
                        id=item_num,
                        title=f"Job Title {item_num}",
                        company=f"Company {item_num}",
                        location=f"Location {item_num}",
                        link=f"http://example.com/job{item_num}",
                        status=status.UNDER_REVIEW
                    ))
                    elif item_num % 10 == 5:
                        display_job_card(job(
                        id=item_num,
                        title=f"Job Title {item_num}",
                        company=f"Company {item_num}",
                        location=f"Location {item_num}",
                        link=f"http://example.com/job{item_num}",
                        status=status.INTERVIEW_SCHEDULED
                    ))
                    elif item_num % 10 == 6:
                        display_job_card(job(
                        id=item_num,
                        title=f"Job Title {item_num}",
                        company=f"Company {item_num}",
                        location=f"Location {item_num}",
                        link=f"http://example.com/job{item_num}",
                        status=status.SHORTLISTED
                    ))
                    elif item_num % 10 == 7:
                        display_job_card(job(
                        id=item_num,
                        title=f"Job Title {item_num}",
                        company=f"Company {item_num}",
                        location=f"Location {item_num}",
                        link=f"http://example.com/job{item_num}",
                        status=status.REJECTED
                    ))
                    elif item_num % 10 == 8:
                        display_job_card(job(
                        id=item_num,
                        title=f"Job Title {item_num}",
                        company=f"Company {item_num}",
                        location=f"Location {item_num}",
                        link=f"http://example.com/job{item_num}",
                        status=status.OFFERED
                    ))
                    elif item_num % 10 == 9:
                        display_job_card(job(
                        id=item_num,
                        title=f"Job Title {item_num}",
                        company=f"Company {item_num}",
                        location=f"Location {item_num}",
                        link=f"http://example.com/job{item_num}",
                        status=status.ACCEPTED
                    ))
                    else:
                        display_job_card(job(
                        id=item_num,
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
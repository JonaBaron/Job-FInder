import streamlit as st
from job import status
from job_card import *

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


# Dummy data to demonstrate layout
# 100 elements, 4 per row = 25 rows
total_items = 100
items_per_row = 2

for row in range(0, total_items, items_per_row):
    cols = st.columns(2)
    
    for i, col in enumerate(cols):
        item_num = row + i + 1
        if item_num <= total_items:
            with col:
                display_job_card(job(
                    id=item_num,
                    title=f"Job Title {item_num}",
                    company=f"Company {item_num}",
                    location=f"Location {item_num}",
                    link=f"http://example.com/job{item_num}",
                    status=status.NEW_NOT_VIEWED
                ))
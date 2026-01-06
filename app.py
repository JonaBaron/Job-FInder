import streamlit as st
from job import status
from job_card import *
from job_finder import find_jobs

## to implement later
# db
# csv
# balloons: st.balloons()


#-- SIDEBAR ----------

#Option 1 dialog
@st.dialog("Info ℹ️")
def info_dialog():
    st.write("# Made by Jonathan Mehmannavaz👋")
    st.write("""
    ## An app made with intention  🎯

    This Job Bank App is designed to help users find and manage job listings efficiently. Below are some key features and information about the app:

    ### Features:
    - **Job Search**: Find job listings based on your queries.
    - **Job Status Tracking**: Keep track of the status of each job application.
    - **Custom Queries**: Add and manage your own job search queries.
    - **Filters**: Sort and filter job listings based on status and company.

    ### How to Use:
    1. ....
 

    ### Follow ME!
    """)
    with st.container(horizontal=True): 
        st.link_button("GitHub", icon=":material/code:", url="https://github.com/JonaBaron")
        st.link_button("LinkedIn", icon=":material/work:", url="https://www.linkedin.com/in/jonathan-mehmannavaz/")
        st.link_button("Webpage", icon=":material/web:", url="https://jonabaron.github.io/")
   

st.session_state.queries = ["Computer Engineering - Canada - internship", "Electrical Engineering - Canada - internship",
             "Software Engineering - Canada - internship", "Data Science - Canada - internship"]


#Option 2 dialog
@st.dialog("My Queries 📋")
def my_queries_dialog():
    
    to_delete = None
    
    for i, q in enumerate(st.session_state.queries):
        col_input, col_btn = st.columns([5, 1])
        with col_input:
            st.session_state.queries[i] = st.text_input(
                f"Query {i+1}", value=q, key=f"prev_query_{id(q)}_{i}"
            )
        with col_btn:
            st.write("") 
            if st.button("", icon=":material/delete:", key=f"delete_{id(q)}_{i}"):
                to_delete = i
    
    if to_delete is not None:
        st.session_state.queries.pop(to_delete)
        st.rerun()
    
    user_input = st.text_input("Add a query to your list:", key="new_query")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Add Query"):
            if user_input.strip():
                st.session_state.queries.append(user_input)
                st.success("Query added successfully!")
                st.rerun()
            else:
                st.warning("Please enter a query first.")
    with col2:
        if st.button("Submit Queries"):
            st.rerun()

#Option 3 dialog
@st.dialog("Settings ⚙️")
def settings_dialog():

    st.write("## API Key Configuration")
    st.write("### JSearch Key Configuration")
    st.text_input("Enter your JSearch api name", placeholder="ex: x-api-key", key="Api_name")
    st.text_input("Enter your JSearch api key", placeholder="ex: your_api_key_12345", key="Api_value")
    st.write("You can get your API key from [here](https://www.openwebninja.com/jsearch).")

    st.write("### MongoDB Key Configuration")
    st.text_input("Enter your MongoDB api name", placeholder="ex: x-api-key", key="MongoDB_Api_name")
    st.text_input("Enter your MongoDB api key", placeholder="ex: your_api_key_12345", key="MongoDB_Api_value")
    st.write("You can get your API key from [here](https://www.mongodb.com/).")
    

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
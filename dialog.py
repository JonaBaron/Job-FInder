import streamlit as st
import os
from dotenv import load_dotenv

#Info dialog
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
   
#My Queries dialog
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

#Settings dialog
@st.dialog("Settings ⚙️")
def settings_dialog():

    load_dotenv()
    os.getenv("JSearch_API_name", st.session_state.get("Api_name", ""))
    os.getenv("JSearch_API_value", st.session_state.get("Api_value", ""))
    os.getenv("MongoDB_Api_name", st.session_state.get("MongoDB_Api_name", ""))
    os.getenv("MongoDB_Api_value", st.session_state.get("MongoDB_Api_value", ""))

    st.write("## API Key Configuration")
    st.write("### JSearch Key Configuration")
    st.text_input("Enter your JSearch api name", placeholder="ex: x-api-key", key="Api_name")
    st.text_input("Enter your JSearch api key", placeholder="ex: your_api_key_12345", key="Api_value")
    st.write("You can get your API key from [here](https://www.openwebninja.com/jsearch).")

    st.write("### MongoDB Key Configuration")
    st.text_input("Enter your MongoDB api name", placeholder="ex: x-api-key", key="MongoDB_Api_name")
    st.text_input("Enter your MongoDB api key", placeholder="ex: your_api_key_12345", key="MongoDB_Api_value")
    st.write("You can get your API key from [here](https://www.mongodb.com/).")

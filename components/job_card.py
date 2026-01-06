import streamlit as st
from models.job import job, status
import webbrowser


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

def new_not_viewed(job_instance):
    with st.container(border=True):
        st.write(job_instance.get_title())
        st.write(f"{job_instance.get_company()}, {job_instance.get_location()}")
        
        # Blue pill badges with margin for spacing
        st.markdown(
            '<span style="background-color: #3454D1; color: white; padding: 4px 12px; border-radius: 16px; font-size: 14px; margin-right: 8px;">New</span>'
            '<span style="background-color: #E63946; color: white; padding: 4px 12px; border-radius: 16px; font-size: 14px;">Not viewed</span>',
            unsafe_allow_html=True
        )
        
        def update_status():
            webbrowser.open(job_instance.get_WEBLink())
            job_instance.set_status(status.NEW_VIEWED)

        flex = st.container(horizontal=True)
        flex.button("Link", key=f"link_{job_instance.id}",on_click=update_status)       
        flex.button("Details", key=f"details_{job_instance.id}") 
        flex.button("Change Link", key=f"change_link_{job_instance.id}")

        st.selectbox("Change of Status", 
            options=["New - Not Viewed"],
            key=f"status_{job_instance.id}",
            index=status.NEW_NOT_VIEWED - 1
        )   

def new_viewed(job_instance):
    with st.container(border=True):
        st.write(job_instance.get_title())
        st.write(f"{job_instance.get_company()}, {job_instance.get_location()}")
        
        # Blue pill badges with margin for spacing
        st.markdown(
            '<span style="background-color: #3454D1; color: white; padding: 4px 12px; border-radius: 16px; font-size: 14px; margin-right: 8px;">New</span>'
            '<span style="background-color: #3C887E; color: white; padding: 4px 12px; border-radius: 16px; font-size: 14px;">Viewed</span>',
            unsafe_allow_html=True
        )
        
        flex = st.container(horizontal=True)
        flex.link_button("Link", job_instance.get_WEBLink())
        flex.button("Details", key=f"details_{job_instance.id}")
        flex.button("Change Link", key=f"change_link_{job_instance.id}")
        
        def update_status():
            new_status_str = st.session_state[f"status_{job_instance.id}"]
            new_status_num = status.get_status_num(new_status_str)
            job_instance.set_status(new_status_num)

        st.selectbox("Change of Status", 
            options=["New - Not Viewed", "New - Viewed", "Applied", "Under Review", "Interview Scheduled", "Shortlisted", "Rejected", "Offered", "Accepted", "Declined"],
            key=f"status_{job_instance.id}",
            index=status.NEW_VIEWED - 1,
            on_change=update_status
        )


def applied(job_instance):
    with st.container(border=True):
        st.write(job_instance.get_title())
        st.write(f"{job_instance.get_company()}, {job_instance.get_location()}")
        
        # Green pill badge for applied
        st.markdown(
            '<span style="background-color: #4CAF50; color: white; padding: 4px 12px; border-radius: 16px; font-size: 14px; margin-right: 8px;">Applied</span>',
            unsafe_allow_html=True
        )
        
        flex = st.container(horizontal=True)
        flex.link_button("Link", job_instance.get_WEBLink())
        flex.button("Details", key=f"details_{job_instance.id}")
        flex.button("Change Link", key=f"change_link_{job_instance.id}")

        def update_status():
            new_status_str = st.session_state[f"status_{job_instance.id}"]
            new_status_num = status.get_status_num(new_status_str)
            job_instance.set_status(new_status_num)
    
        st.selectbox("Change of Status", 
            options=["New - Not Viewed", "New - Viewed", "Applied", "Under Review", "Interview Scheduled", "Shortlisted", "Rejected", "Offered", "Accepted", "Declined"],
            key=f"status_{job_instance.id}",
            index=status.APPLIED - 1,
            on_change=update_status
        )

def under_review(job_instance):
    with st.container(border=True):
        st.write(job_instance.get_title())
        st.write(f"{job_instance.get_company()}, {job_instance.get_location()}")
        
        # Orange pill badge for under review
        st.markdown(
            '<span style="background-color: #FF9800; color: white; padding: 4px 12px; border-radius: 16px; font-size: 14px; margin-right: 8px;">under review</span>', 
            unsafe_allow_html=True
        )
        
        flex = st.container(horizontal=True)
        flex.link_button("Link", job_instance.get_WEBLink())
        flex.button("Details", key=f"details_{job_instance.id}")
        flex.button("Change Link", key=f"change_link_{job_instance.id}")

        def update_status():
            new_status_str = st.session_state[f"status_{job_instance.id}"]
            new_status_num = status.get_status_num(new_status_str)
            job_instance.set_status(new_status_num)

        st.selectbox("Change of Status", 
            options=["New - Not Viewed", "New - Viewed", "Applied", "Under Review", "Interview Scheduled", "Shortlisted", "Rejected", "Offered", "Accepted", "Declined"],
            key=f"status_{job_instance.id}",
            index=status.UNDER_REVIEW - 1,
            on_change=update_status
        )

def interview_scheduled(job_instance):
    with st.container(border=True):
        st.write(job_instance.get_title())
        st.write(f"{job_instance.get_company()}, {job_instance.get_location()}")
        
        # Purple pill badge for interview scheduled
        st.markdown(
            '<span style="background-color: #9C27B0; color: white; padding: 4px 12px; border-radius: 16px; font-size: 14px; margin-right: 8px;">interview scheduled</span>',
            unsafe_allow_html=True
        )
        
        flex = st.container(horizontal=True)
        flex.link_button("Link", job_instance.get_WEBLink())
        flex.button("Details", key=f"details_{job_instance.id}")
        flex.button("Change Link", key=f"change_link_{job_instance.id}")

        def update_status():
            new_status_str = st.session_state[f"status_{job_instance.id}"]
            new_status_num = status.get_status_num(new_status_str)
            job_instance.set_status(new_status_num)

        st.selectbox("Change of Status", 
            options=["New - Not Viewed", "New - Viewed", "Applied", "Under Review", "Interview Scheduled", "Shortlisted", "Rejected", "Offered", "Accepted", "Declined"],
            key=f"status_{job_instance.id}",
            index=status.INTERVIEW_SCHEDULED - 1,
            on_change= update_status
        )

def shortlisted(job_instance):
    with st.container(border=True):
        st.write(job_instance.get_title())
        st.write(f"{job_instance.get_company()}, {job_instance.get_location()}")
        
        # Teal pill badge for shortlisted
        st.markdown(
            '<span style="background-color: #F6C28B; color: white; padding: 4px 12px; border-radius: 16px; font-size: 14px; margin-right: 8px;">shortlisted</span>',
            unsafe_allow_html=True
        )
        
        flex = st.container(horizontal=True)
        flex.link_button("Link", job_instance.get_WEBLink())
        flex.button("Details", key=f"details_{job_instance.id}")
        flex.button("Change Link", key=f"change_link_{job_instance.id}")

        def update_status():
            new_status_str = st.session_state[f"status_{job_instance.id}"]
            new_status_num = status.get_status_num(new_status_str)
            job_instance.set_status(new_status_num)

        st.selectbox("Change of Status", 
            options=["New - Not Viewed", "New - Viewed", "Applied", "Under Review", "Interview Scheduled", "Shortlisted", "Rejected", "Offered", "Accepted", "Declined"],
            key=f"status_{job_instance.id}",
            index=status.SHORTLISTED - 1,
            on_change= update_status
        )


def rejected(job_instance):
    with st.container(border=True):
        st.write(job_instance.get_title())
        st.write(f"{job_instance.get_company()}, {job_instance.get_location()}")
        
        # Red pill badge for rejected
        st.markdown(
            '<span style="background-color: #F44336; color: white; padding: 4px 12px; border-radius: 16px; font-size: 14px; margin-right: 8px;">rejected</span>',
            unsafe_allow_html=True
        )
        
        flex = st.container(horizontal=True)
        flex.link_button("Link", job_instance.get_WEBLink())
        flex.button("Details", key=f"details_{job_instance.id}")
        flex.button("Change Link", key=f"change_link_{job_instance.id}")

        def update_status():
            new_status_str = st.session_state[f"status_{job_instance.id}"]
            new_status_num = status.get_status_num(new_status_str)
            job_instance.set_status(new_status_num)

        st.selectbox("Change of Status", 
            options=["New - Not Viewed", "New - Viewed", "Applied", "Under Review", "Interview Scheduled", "Shortlisted", "Rejected", "Offered", "Accepted", "Declined"],
            key=f"status_{job_instance.id}",
            index=status.REJECTED - 1,
            on_change=update_status
        )

def offered(job_instance):
    with st.container(border=True):
        st.write(job_instance.get_title())
        st.write(f"{job_instance.get_company()}, {job_instance.get_location()}")
        
        # Gold pill badge for offered
        st.markdown(
            '<span style="background-color: #FFD700; color: black; padding: 4px 12px; border-radius: 16px; font-size: 14px; margin-right: 8px;">offered</span>',
            unsafe_allow_html=True
        )
        
        flex = st.container(horizontal=True)
        flex.link_button("Link", job_instance.get_WEBLink())
        flex.button("Details", key=f"details_{job_instance.id}")
        flex.button("Change Link", key=f"change_link_{job_instance.id}")

        def update_status():
            new_status_str = st.session_state[f"status_{job_instance.id}"]
            new_status_num = status.get_status_num(new_status_str)
            job_instance.set_status(new_status_num)

        st.selectbox("Change of Status", 
            options=["New - Not Viewed", "New - Viewed", "Applied", "Under Review", "Interview Scheduled", "Shortlisted", "Rejected", "Offered", "Accepted", "Declined"],
            key=f"status_{job_instance.id}",
            index=status.OFFERED - 1,
            on_change= update_status
        )        


def accepted(job_instance):
    with st.container(border=True):
        st.write(job_instance.get_title())
        st.write(f"{job_instance.get_company()}, {job_instance.get_location()}")
        
        # Green pill badge for accepted
        st.markdown(
            '<span style="background-color: #4CAF50; color: white; padding: 4px 12px; border-radius: 16px; font-size: 14px; margin-right: 8px;">accepted</span>',
            unsafe_allow_html=True
        )
        
        flex = st.container(horizontal=True)
        flex.link_button("Link", job_instance.get_WEBLink())
        flex.button("Details", key=f"details_{job_instance.id}")
        flex.button("Change Link", key=f"change_link_{job_instance.id}")

        def update_status():
            new_status_str = st.session_state[f"status_{job_instance.id}"]
            new_status_num = status.get_status_num(new_status_str)
            job_instance.set_status(new_status_num)

        st.selectbox("Change of Status", 
            options=["New - Not Viewed", "New - Viewed", "Applied", "Under Review", "Interview Scheduled", "Shortlisted", "Rejected", "Offered", "Accepted", "Declined"],
            key=f"status_{job_instance.id}",
            index=status.ACCEPTED - 1, 
            on_change= update_status
        )
                    

def declined(job_instance):
    with st.container(border=True):
        st.write(job_instance.get_title())
        st.write(f"{job_instance.get_company()}, {job_instance.get_location()}")
        
        st.markdown(
            '<span style="background-color: #9E9E9E; color: white; padding: 4px 12px; border-radius: 16px; font-size: 14px; margin-right: 8px;">declined</span>',
            unsafe_allow_html=True
        )
        
        flex = st.container(horizontal=True)
        flex.link_button("Link", job_instance.get_WEBLink())
        flex.button("Details", key=f"details_{job_instance.id}")  
        flex.button("Change Link", key=f"change_link_{job_instance.id}")
        
        def update_status():
            new_status_str = st.session_state[f"status_{job_instance.id}"]
            new_status_num = status.get_status_num(new_status_str)
            job_instance.set_status(new_status_num)
        
        current_status_index = job_instance.get_status() - 1
        
        st.selectbox(
            "Change of Status", 
            options=["New - Not Viewed", "New - Viewed", "Applied", "Under Review", 
                     "Interview Scheduled", "Shortlisted", "Rejected", "Offered", 
                     "Accepted", "Declined"],
            key=f"status_{job_instance.id}",
            index=current_status_index,
            on_change=update_status
        )
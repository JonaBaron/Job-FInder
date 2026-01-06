import streamlit as st
from job import job, status




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
        
        flex = st.container(horizontal=True)
        flex.link_button("Link", job_instance.get_WEBLink())
        flex.button("View Details", key=f"details_{job_instance.id}")
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
        flex.button("View Details", key=f"details_{job_instance.id}")
        st.selectbox("Change of Status", 
            options=["New - Not Viewed", "New - Viewed", "Applied", "Under Review", "Interview Scheduled", "Shortlisted", "Rejected", "Offered", "Accepted", "Declined"],
            key=f"status_{job_instance.id}",
            index=status.NEW_VIEWED - 1
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
        flex.button("View Details", key=f"details_{job_instance.id}")
        st.selectbox("Change of Status", 
            options=["New - Not Viewed", "New - Viewed", "Applied", "Under Review", "Interview Scheduled", "Shortlisted", "Rejected", "Offered", "Accepted", "Declined"],
            key=f"status_{job_instance.id}",
            index=status.APPLIED - 1
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
        flex.button("View Details", key=f"details_{job_instance.id}")
        st.selectbox("Change of Status", 
            options=["New - Not Viewed", "New - Viewed", "Applied", "Under Review", "Interview Scheduled", "Shortlisted", "Rejected", "Offered", "Accepted", "Declined"],
            key=f"status_{job_instance.id}",
            index=status.UNDER_REVIEW - 1
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
        flex.button("View Details", key=f"details_{job_instance.id}")
        st.selectbox("Change of Status", 
            options=["New - Not Viewed", "New - Viewed", "Applied", "Under Review", "Interview Scheduled", "Shortlisted", "Rejected", "Offered", "Accepted", "Declined"],
            key=f"status_{job_instance.id}",
            index=status.INTERVIEW_SCHEDULED - 1
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
        flex.button("View Details", key=f"details_{job_instance.id}")
        st.selectbox("Change of Status", 
            options=["New - Not Viewed", "New - Viewed", "Applied", "Under Review", "Interview Scheduled", "Shortlisted", "Rejected", "Offered", "Accepted", "Declined"],
            key=f"status_{job_instance.id}",
            index=status.SHORTLISTED - 1
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
        flex.button("View Details", key=f"details_{job_instance.id}")
        st.selectbox("Change of Status", 
            options=["New - Not Viewed", "New - Viewed", "Applied", "Under Review", "Interview Scheduled", "Shortlisted", "Rejected", "Offered", "Accepted", "Declined"],
            key=f"status_{job_instance.id}",
            index=status.REJECTED - 1
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
        flex.button("View Details", key=f"details_{job_instance.id}")
        st.selectbox("Change of Status", 
            options=["New - Not Viewed", "New - Viewed", "Applied", "Under Review", "Interview Scheduled", "Shortlisted", "Rejected", "Offered", "Accepted", "Declined"],
            key=f"status_{job_instance.id}",
            index=status.OFFERED - 1
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
        flex.button("View Details", key=f"details_{job_instance.id}")
        st.selectbox("Change of Status", 
            options=["New - Not Viewed", "New - Viewed", "Applied", "Under Review", "Interview Scheduled", "Shortlisted", "Rejected", "Offered", "Accepted", "Declined"],
            key=f"status_{job_instance.id}",
            index=status.ACCEPTED - 1
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
        flex.button("View Details", key=f"details_{job_instance.id}")  
        st.selectbox("Change of Status", 
            options=["New - Not Viewed", "New - Viewed", "Applied", "Under Review", "Interview Scheduled", "Shortlisted", "Rejected", "Offered", "Accepted", "Declined"],
            key=f"status_{job_instance.id}",
            index= status.DECLINED - 1
        )
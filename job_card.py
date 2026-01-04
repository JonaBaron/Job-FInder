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
        flex.button("Apply Now", key=f"apply_{job_instance.id}")
        flex.button("View Details", key=f"view_{job_instance.id}")   
    
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
        flex.button("Apply Now", key=f"apply_{job_instance.id}")
        flex.button("View Details", key=f"view_{job_instance.id}")

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
        flex.button("View Application Status", key=f"status_{job_instance.id}")
        flex.button("View Details", key=f"view_{job_instance.id}")

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
        flex.button("View Application Status", key=f"status_{job_instance.id}")
        flex.button("View Details", key=f"view_{job_instance.id}")

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
        flex.button("View Interview Details", key=f"interview_{job_instance.id}")
        flex.button("View Details", key=f"view_{job_instance.id}")

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
        flex.button("View Application Status", key=f"status_{job_instance.id}")
        flex.button("View Details", key=f"view_{job_instance.id}")


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
        flex.button("View Feedback", key=f"feedback_{job_instance.id}")
        flex.button("View Details", key=f"view_{job_instance.id}")

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
        flex.button("View Offer Details", key=f"offer_{job_instance.id}")
        flex.button("View Details", key=f"view_{job_instance.id}")

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
        flex.button("View Onboarding Details", key=f"onboard_{job_instance.id}")
        flex.button("View Details", key=f"view_{job_instance.id}")

def declined(job_instance):
    with st.container(border=True):
        st.write(job_instance.get_title())
        st.write(f"{job_instance.get_company()}, {job_instance.get_location()}")
        
        # Grey pill badge for declined
        st.markdown(
            '<span style="background-color: #9E9E9E; color: white; padding: 4px 12px; border-radius: 16px; font-size: 14px; margin-right: 8px;">declined</span>',
            unsafe_allow_html=True
        )
        
        flex = st.container(horizontal=True)
        flex.button("View Details", key=f"view_{job_instance.id}")

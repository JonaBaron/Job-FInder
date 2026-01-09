import streamlit as st
from models.job import job, status
from utils.session_helper import get_value, set_value, get_user_email, get_queries, get_jobs
from utils.db_jobs import sync_jobs_to_db
import webbrowser


def display_job_card(job_instance, query_idx: int = 0):
    """Display a job card with the appropriate status styling."""
    job_type = job_instance.get_status()

    if job_type == status.NEW_NOT_VIEWED:
        new_not_viewed(job_instance, query_idx)
    elif job_type == status.NEW_VIEWED:
        new_viewed(job_instance, query_idx)
    elif job_type == status.APPLIED:
        applied(job_instance, query_idx)
    elif job_type == status.UNDER_REVIEW:
        under_review(job_instance, query_idx)
    elif job_type == status.INTERVIEW_SCHEDULED:
        interview_scheduled(job_instance, query_idx)
    elif job_type == status.SHORTLISTED:
        shortlisted(job_instance, query_idx)
    elif job_type == status.REJECTED:
        rejected(job_instance, query_idx)
    elif job_type == status.OFFERED:
        offered(job_instance, query_idx)
    elif job_type == status.ACCEPTED:
        accepted(job_instance, query_idx)
    elif job_type == status.DECLINED:
        declined(job_instance, query_idx)


def request_edit_link(job_instance, query_idx: int):
    """Store job info in session state to trigger edit link dialog."""
    set_value('edit_link_job', job_instance)
    set_value('edit_link_query_idx', query_idx)


def handle_link_click(job_instance):
    """Log link click and open the link."""
    job_instance.log_link_click()
    webbrowser.open(job_instance.get_WEBLink())


def sync_after_change():
    """Sync jobs to database after any change."""
    email = get_user_email()
    if email:
        queries = get_queries()
        jobs = get_jobs()
        sync_jobs_to_db(email, queries, jobs)

def new_not_viewed(job_instance, query_idx: int):
    with st.container(border=True):
        st.write(job_instance.get_title())
        st.write(f"{job_instance.get_company()}, {job_instance.get_location()}")

        st.markdown(
            '<span style="background-color: #3454D1; color: white; padding: 4px 12px; border-radius: 16px; font-size: 14px; margin-right: 8px;">New</span>'
            '<span style="background-color: #E63946; color: white; padding: 4px 12px; border-radius: 16px; font-size: 14px;">Not viewed</span>',
            unsafe_allow_html=True
        )

        def on_link_click():
            handle_link_click(job_instance)
            job_instance.set_status(status.NEW_VIEWED)
            sync_after_change()

        flex = st.container(horizontal=True)
        flex.button("Link", key=f"link_{job_instance.id}", on_click=on_link_click)
        flex.button("Details", key=f"details_{job_instance.id}")
        if flex.button("Edit Link", key=f"change_link_{job_instance.id}"):
            request_edit_link(job_instance, query_idx)
            st.rerun()

        st.selectbox("Change of Status",
            options=["New - Not Viewed"],
            key=f"status_{job_instance.id}",
            index=status.NEW_NOT_VIEWED - 1
        )   

def new_viewed(job_instance, query_idx: int):
    with st.container(border=True):
        st.write(job_instance.get_title())
        st.write(f"{job_instance.get_company()}, {job_instance.get_location()}")

        st.markdown(
            '<span style="background-color: #3454D1; color: white; padding: 4px 12px; border-radius: 16px; font-size: 14px; margin-right: 8px;">New</span>'
            '<span style="background-color: #3C887E; color: white; padding: 4px 12px; border-radius: 16px; font-size: 14px;">Viewed</span>',
            unsafe_allow_html=True
        )

        flex = st.container(horizontal=True)
        if flex.button("Link", key=f"link_{job_instance.id}"):
            handle_link_click(job_instance)
        flex.button("Details", key=f"details_{job_instance.id}")
        if flex.button("Edit Link", key=f"change_link_{job_instance.id}"):
            request_edit_link(job_instance, query_idx)
            st.rerun()

        def update_status():
            new_status_str = get_value(f"status_{job_instance.id}")
            new_status_num = status.get_status_num(new_status_str)
            job_instance.set_status(new_status_num)
            sync_after_change()

        st.selectbox("Change of Status",
            options=["New - Not Viewed", "New - Viewed", "Applied", "Under Review", "Interview Scheduled", "Shortlisted", "Rejected", "Offered", "Accepted", "Declined"],
            key=f"status_{job_instance.id}",
            index=status.NEW_VIEWED - 1,
            on_change=update_status
        )


def applied(job_instance, query_idx: int):
    with st.container(border=True):
        st.write(job_instance.get_title())
        st.write(f"{job_instance.get_company()}, {job_instance.get_location()}")

        st.markdown(
            '<span style="background-color: #4CAF50; color: white; padding: 4px 12px; border-radius: 16px; font-size: 14px; margin-right: 8px;">Applied</span>',
            unsafe_allow_html=True
        )

        flex = st.container(horizontal=True)
        if flex.button("Link", key=f"link_{job_instance.id}"):
            handle_link_click(job_instance)
        flex.button("Details", key=f"details_{job_instance.id}")
        if flex.button("Edit Link", key=f"change_link_{job_instance.id}"):
            request_edit_link(job_instance, query_idx)
            st.rerun()

        def update_status():
            new_status_str = get_value(f"status_{job_instance.id}")
            new_status_num = status.get_status_num(new_status_str)
            job_instance.set_status(new_status_num)
            sync_after_change()

        st.selectbox("Change of Status",
            options=["New - Not Viewed", "New - Viewed", "Applied", "Under Review", "Interview Scheduled", "Shortlisted", "Rejected", "Offered", "Accepted", "Declined"],
            key=f"status_{job_instance.id}",
            index=status.APPLIED - 1,
            on_change=update_status
        )


def under_review(job_instance, query_idx: int):
    with st.container(border=True):
        st.write(job_instance.get_title())
        st.write(f"{job_instance.get_company()}, {job_instance.get_location()}")

        st.markdown(
            '<span style="background-color: #FF9800; color: white; padding: 4px 12px; border-radius: 16px; font-size: 14px; margin-right: 8px;">Under Review</span>',
            unsafe_allow_html=True
        )

        flex = st.container(horizontal=True)
        if flex.button("Link", key=f"link_{job_instance.id}"):
            handle_link_click(job_instance)
        flex.button("Details", key=f"details_{job_instance.id}")
        if flex.button("Edit Link", key=f"change_link_{job_instance.id}"):
            request_edit_link(job_instance, query_idx)
            st.rerun()

        def update_status():
            new_status_str = get_value(f"status_{job_instance.id}")
            new_status_num = status.get_status_num(new_status_str)
            job_instance.set_status(new_status_num)
            sync_after_change()

        st.selectbox("Change of Status",
            options=["New - Not Viewed", "New - Viewed", "Applied", "Under Review", "Interview Scheduled", "Shortlisted", "Rejected", "Offered", "Accepted", "Declined"],
            key=f"status_{job_instance.id}",
            index=status.UNDER_REVIEW - 1,
            on_change=update_status
        )


def interview_scheduled(job_instance, query_idx: int):
    with st.container(border=True):
        st.write(job_instance.get_title())
        st.write(f"{job_instance.get_company()}, {job_instance.get_location()}")

        st.markdown(
            '<span style="background-color: #9C27B0; color: white; padding: 4px 12px; border-radius: 16px; font-size: 14px; margin-right: 8px;">Interview Scheduled</span>',
            unsafe_allow_html=True
        )

        flex = st.container(horizontal=True)
        if flex.button("Link", key=f"link_{job_instance.id}"):
            handle_link_click(job_instance)
        flex.button("Details", key=f"details_{job_instance.id}")
        if flex.button("Edit Link", key=f"change_link_{job_instance.id}"):
            request_edit_link(job_instance, query_idx)
            st.rerun()

        def update_status():
            new_status_str = get_value(f"status_{job_instance.id}")
            new_status_num = status.get_status_num(new_status_str)
            job_instance.set_status(new_status_num)
            sync_after_change()

        st.selectbox("Change of Status",
            options=["New - Not Viewed", "New - Viewed", "Applied", "Under Review", "Interview Scheduled", "Shortlisted", "Rejected", "Offered", "Accepted", "Declined"],
            key=f"status_{job_instance.id}",
            index=status.INTERVIEW_SCHEDULED - 1,
            on_change=update_status
        )


def shortlisted(job_instance, query_idx: int):
    with st.container(border=True):
        st.write(job_instance.get_title())
        st.write(f"{job_instance.get_company()}, {job_instance.get_location()}")

        st.markdown(
            '<span style="background-color: #F6C28B; color: white; padding: 4px 12px; border-radius: 16px; font-size: 14px; margin-right: 8px;">Shortlisted</span>',
            unsafe_allow_html=True
        )

        flex = st.container(horizontal=True)
        if flex.button("Link", key=f"link_{job_instance.id}"):
            handle_link_click(job_instance)
        flex.button("Details", key=f"details_{job_instance.id}")
        if flex.button("Edit Link", key=f"change_link_{job_instance.id}"):
            request_edit_link(job_instance, query_idx)
            st.rerun()

        def update_status():
            new_status_str = get_value(f"status_{job_instance.id}")
            new_status_num = status.get_status_num(new_status_str)
            job_instance.set_status(new_status_num)
            sync_after_change()

        st.selectbox("Change of Status",
            options=["New - Not Viewed", "New - Viewed", "Applied", "Under Review", "Interview Scheduled", "Shortlisted", "Rejected", "Offered", "Accepted", "Declined"],
            key=f"status_{job_instance.id}",
            index=status.SHORTLISTED - 1,
            on_change=update_status
        )


def rejected(job_instance, query_idx: int):
    with st.container(border=True):
        st.write(job_instance.get_title())
        st.write(f"{job_instance.get_company()}, {job_instance.get_location()}")

        st.markdown(
            '<span style="background-color: #F44336; color: white; padding: 4px 12px; border-radius: 16px; font-size: 14px; margin-right: 8px;">Rejected</span>',
            unsafe_allow_html=True
        )

        flex = st.container(horizontal=True)
        if flex.button("Link", key=f"link_{job_instance.id}"):
            handle_link_click(job_instance)
        flex.button("Details", key=f"details_{job_instance.id}")
        if flex.button("Edit Link", key=f"change_link_{job_instance.id}"):
            request_edit_link(job_instance, query_idx)
            st.rerun()

        def update_status():
            new_status_str = get_value(f"status_{job_instance.id}")
            new_status_num = status.get_status_num(new_status_str)
            job_instance.set_status(new_status_num)
            sync_after_change()

        st.selectbox("Change of Status",
            options=["New - Not Viewed", "New - Viewed", "Applied", "Under Review", "Interview Scheduled", "Shortlisted", "Rejected", "Offered", "Accepted", "Declined"],
            key=f"status_{job_instance.id}",
            index=status.REJECTED - 1,
            on_change=update_status
        )


def offered(job_instance, query_idx: int):
    with st.container(border=True):
        st.write(job_instance.get_title())
        st.write(f"{job_instance.get_company()}, {job_instance.get_location()}")

        st.markdown(
            '<span style="background-color: #FFD700; color: black; padding: 4px 12px; border-radius: 16px; font-size: 14px; margin-right: 8px;">Offered</span>',
            unsafe_allow_html=True
        )

        flex = st.container(horizontal=True)
        if flex.button("Link", key=f"link_{job_instance.id}"):
            handle_link_click(job_instance)
        flex.button("Details", key=f"details_{job_instance.id}")
        if flex.button("Edit Link", key=f"change_link_{job_instance.id}"):
            request_edit_link(job_instance, query_idx)
            st.rerun()

        def update_status():
            new_status_str = get_value(f"status_{job_instance.id}")
            new_status_num = status.get_status_num(new_status_str)
            job_instance.set_status(new_status_num)
            sync_after_change()

        st.selectbox("Change of Status",
            options=["New - Not Viewed", "New - Viewed", "Applied", "Under Review", "Interview Scheduled", "Shortlisted", "Rejected", "Offered", "Accepted", "Declined"],
            key=f"status_{job_instance.id}",
            index=status.OFFERED - 1,
            on_change=update_status
        )


def accepted(job_instance, query_idx: int):
    with st.container(border=True):
        st.write(job_instance.get_title())
        st.write(f"{job_instance.get_company()}, {job_instance.get_location()}")

        st.markdown(
            '<span style="background-color: #4CAF50; color: white; padding: 4px 12px; border-radius: 16px; font-size: 14px; margin-right: 8px;">Accepted</span>',
            unsafe_allow_html=True
        )

        flex = st.container(horizontal=True)
        if flex.button("Link", key=f"link_{job_instance.id}"):
            handle_link_click(job_instance)
        flex.button("Details", key=f"details_{job_instance.id}")
        if flex.button("Edit Link", key=f"change_link_{job_instance.id}"):
            request_edit_link(job_instance, query_idx)
            st.rerun()

        def update_status():
            new_status_str = get_value(f"status_{job_instance.id}")
            new_status_num = status.get_status_num(new_status_str)
            job_instance.set_status(new_status_num)
            sync_after_change()

        st.selectbox("Change of Status",
            options=["New - Not Viewed", "New - Viewed", "Applied", "Under Review", "Interview Scheduled", "Shortlisted", "Rejected", "Offered", "Accepted", "Declined"],
            key=f"status_{job_instance.id}",
            index=status.ACCEPTED - 1,
            on_change=update_status
        )


def declined(job_instance, query_idx: int):
    with st.container(border=True):
        st.write(job_instance.get_title())
        st.write(f"{job_instance.get_company()}, {job_instance.get_location()}")

        st.markdown(
            '<span style="background-color: #9E9E9E; color: white; padding: 4px 12px; border-radius: 16px; font-size: 14px; margin-right: 8px;">Declined</span>',
            unsafe_allow_html=True
        )

        flex = st.container(horizontal=True)
        if flex.button("Link", key=f"link_{job_instance.id}"):
            handle_link_click(job_instance)
        flex.button("Details", key=f"details_{job_instance.id}")
        if flex.button("Edit Link", key=f"change_link_{job_instance.id}"):
            request_edit_link(job_instance, query_idx)
            st.rerun()

        def update_status():
            new_status_str = get_value(f"status_{job_instance.id}")
            new_status_num = status.get_status_num(new_status_str)
            job_instance.set_status(new_status_num)
            sync_after_change()

        st.selectbox("Change of Status",
            options=["New - Not Viewed", "New - Viewed", "Applied", "Under Review", "Interview Scheduled", "Shortlisted", "Rejected", "Offered", "Accepted", "Declined"],
            key=f"status_{job_instance.id}",
            index=status.DECLINED - 1,
            on_change=update_status
        )
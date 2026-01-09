from datetime import datetime


class job:

    def __init__(self, id, title, company, location, link, status):
        self.id = id
        self.title = title
        self.company = company
        self.location = location
        self.link = link
        self.status = status
        self.applied_date = None
        self.viewed_date = None
        self.created_at = datetime.utcnow().isoformat()
        # History tracking
        self.history = {
            "status_changes": [],
            "link_clicks": [],
            "link_edits": []
        }

    # Getters
    def get_title(self):
        return self.title

    def get_company(self):
        return self.company

    def get_location(self):
        return self.location

    def get_WEBLink(self):
        return self.link

    def get_status(self):
        return self.status

    def get_history(self):
        return self.history

    # Setters
    def set_WEBLink(self, new_link):
        old_link = self.link
        self.link = new_link
        # Log link edit
        self.history["link_edits"].append({
            "old_link": old_link,
            "new_link": new_link,
            "timestamp": datetime.utcnow().isoformat()
        })

    def set_status(self, new_status):
        old_status = self.status
        self.status = new_status
        # Log status change
        self.history["status_changes"].append({
            "from": old_status,
            "to": new_status,
            "timestamp": datetime.utcnow().isoformat()
        })

    def log_link_click(self):
        """Log when user clicks on the job link."""
        self.history["link_clicks"].append({
            "timestamp": datetime.utcnow().isoformat()
        })
            


class status:
    # Different types of job status
    # 1. New Job, Not Viewed
    NEW_NOT_VIEWED = 1
    # 2. New Job, Viewed
    NEW_VIEWED = 2
    # 3. Applied Job
    APPLIED = 3
    # 4. Under Review Job
    UNDER_REVIEW = 4
    # 5. Interview Scheduled Job
    INTERVIEW_SCHEDULED = 5
    # 6. Shortlisted Job
    SHORTLISTED = 6
    # 7. Rejected Job
    REJECTED = 7
    # 8. Offered Job
    OFFERED = 8
    # 9. Accepted Job
    ACCEPTED = 9
    # 10. Declined Job
    DECLINED = 10

    def get_status_num(status_str):
        status_dict = {
            "New - Not Viewed": status.NEW_NOT_VIEWED,
            "New - Viewed": status.NEW_VIEWED,
            "Applied": status.APPLIED,
            "Under Review": status.UNDER_REVIEW,
            "Interview Scheduled": status.INTERVIEW_SCHEDULED,
            "Shortlisted": status.SHORTLISTED,
            "Rejected": status.REJECTED,
            "Offered": status.OFFERED,
            "Accepted": status.ACCEPTED,
            "Declined": status.DECLINED
        }
        return status_dict.get(status_str, None)



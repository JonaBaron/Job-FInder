class job: 

    def __init__(self, id , title, company, location, link, status):
        self.id = id
        self.title = title
        self.company = company
        self.location = location
        self.link = link
        self.status = status
        self.applied_date = None  # To be set when the user applies for the job
        self.viewed_date = None  # To be set when the user views the job details

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

    # Setters if user find new link job position
    def set_WEBLink(self, link):
            self.link = link

    def set_status(self, status):
            self.status = status
            


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



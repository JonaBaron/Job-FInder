class job: 

    def __init__(self, id , title, company, location, link, status):
        self.id = id
        self.title = title
        self.company = company
        self.location = location
        self.link = link
        self.status = status
        self.applied_date = None  # To be set when the user applies for the job
        self.isNew = True  # Flag to indicate if the job is new or has been viewed
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

    # Setters if user find new link job position
    def set_WEBLink(self, link):
            self.link = link


class status:
    NEW = "New"
    APPLIED = "Applied"
    UNDER_REVIEW = "Under Review"
    INTERVIEW_SCHEDULED = "Interview Scheduled"
    SHORTLISTED = "Shortlisted"
    REJECTED = "Rejected"



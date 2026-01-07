import requests
import os
import uuid
from dotenv import load_dotenv
from models.job import job, status

# Import function to load API keys
def load_api_keys():
    load_dotenv()
    api_key_name = os.getenv("JSearch_API_name")
    api_key_value = os.getenv("JSearch_API_value")
    url = "https://api.openwebninja.com/jsearch/search"
    return api_key_name, api_key_value , url

# Dummy function to generate job data for testing
def dummy_find_jobs(query_idx=0, total_items=100):
    """Generate dummy job data with cycling statuses"""
    status_map = {
        1: status.NEW_NOT_VIEWED,
        2: status.NEW_VIEWED,
        3: status.APPLIED,
        4: status.UNDER_REVIEW,
        5: status.INTERVIEW_SCHEDULED,
        6: status.SHORTLISTED,
        7: status.REJECTED,
        8: status.OFFERED,
        9: status.ACCEPTED,
        0: status.DECLINED,
    }
    
    return [
        job(
            id=str(uuid.uuid4()),
            title=f"Job Title {i}",
            company=f"Company {i}",
            location=f"Location {i}",
            link=f"http://example.com/job{i}",
            status=status_map[i % 10]
        )
        for i in range(1, total_items + 1)
    ]

#hard coded jobs
fake_jobs = [
    # Tech
    job(id=1, title="Senior Software Engineer", company="TechNova Solutions", location="San Francisco, CA", link="http://example.com/job1", status=status.NEW_NOT_VIEWED),
    job(id=2, title="Data Scientist", company="DataMind Analytics", location="Austin, TX", link="", status=status.APPLIED),
    
    # Healthcare
    job(id=3, title="Registered Nurse", company="Sunrise Medical Center", location="Boston, MA", link="", status=status.UNDER_REVIEW),
    job(id=4, title="Physical Therapist", company="ActiveLife Rehabilitation", location="Denver, CO", link="", status=status.NEW_VIEWED),
    job(id=5, title="Pharmacy Technician", company="MedPlus Pharmacy", location="Chicago, IL", link="", status=status.OFFERED),
    
    # Food & Hospitality
    job(id=6, title="Executive Chef", company="Golden Fork Restaurant", location="New York, NY", link="", status=status.REJECTED),
    job(id=7, title="Hotel Manager", company="Oceanview Resort", location="Miami, FL", link="", status=status.INTERVIEW_SCHEDULED),
    job(id=8, title="Barista", company="Bean & Brew Coffee", location="Seattle, WA", link="", status=status.NEW_NOT_VIEWED),
    
    # Education
    job(id=9, title="High School Math Teacher", company="Westbrook Academy", location="Portland, OR", link="", status=status.OFFERED),
    job(id=10, title="University Professor", company="Lakefield University", location="Toronto, ON", link="", status=status.NEW_NOT_VIEWED),
    job(id=11, title="School Counselor", company="Maplewood Elementary", location="Vancouver, BC", link="", status=status.SHORTLISTED),
    
    # Construction & Trades
    job(id=12, title="Electrician", company="BrightSpark Electric", location="Phoenix, AZ", link="", status=status.UNDER_REVIEW),
    job(id=13, title="Plumber", company="FlowRight Plumbing", location="Houston, TX", link="", status=status.ACCEPTED),
    job(id=14, title="Construction Manager", company="BuildWell Inc.", location="Atlanta, GA", link="", status=status.OFFERED),
    
    # Arts & Entertainment
    job(id=15, title="Graphic Designer", company="Creative Spark Studio", location="Los Angeles, CA", link="", status=status.DECLINED),
    job(id=16, title="Video Editor", company="Visionary Films", location="Nashville, TN", link="", status=status.REJECTED),
    job(id=17, title="Museum Curator", company="Heritage Art Museum", location="Washington, DC", link="", status=status.SHORTLISTED),
    
    # Finance & Business
    job(id=18, title="Financial Analyst", company="Summit Capital Group", location="Charlotte, NC", link="", status=status.NEW_NOT_VIEWED),
    job(id=19, title="Accountant", company="TrustLedger Accounting", location="Dallas, TX", link="", status=status.NEW_NOT_VIEWED),
    job(id=20, title="Marketing Manager", company="BrandBoost Agency", location="Montreal, QC", link="", status=status.UNDER_REVIEW),
]


# Test function to demonstrate job finding
def find_jobs_test():

    api_key_name, api_key_value , url = load_api_keys()

    headers = {
        api_key_name: api_key_value
    }

    params = {
        "query": "Montreal",
        "num_pages": 2
    }

    response = requests.get(url, headers=headers, params=params)
    data = response.json()

    # Print nicely
    for job in data.get('data', []):
        print(f"Title: {job.get('job_title')}")
        print(f"Company: {job.get('employer_name')}")
        print(f"Location: {job.get('job_city')}, {job.get('job_state')}")
        print(f"Link: {job.get('job_apply_link')}")
        print('-' * 50)




# Main function to find jobs and return list of job instances
def find_jobs(query="Computer Engineering - Canada - internship", num_pages=2,query_idx=0):

    api_key_name, api_key_value , url = load_api_keys()

    headers = {
        api_key_name: api_key_value
    }

    params = {
        "query": query,
        "num_pages": num_pages
    }

    response = requests.get(url, headers=headers, params=params)
    data = response.json()

    for job_data in data.get('data', []):  # Changed from 'job' to 'job_data'
        print(f"Title: {job_data.get('job_title')}")
        print(f"Company: {job_data.get('employer_name')}")
        print(f"Location: {job_data.get('job_city')}, {job_data.get('job_state')}")
        print(f"Link: {job_data.get('job_apply_link')}")
        print('-' * 50)

    return [
        job(
            id=str(uuid.uuid4()),
            title=job_data.get('job_title'),
            company=job_data.get('employer_name'),
            location=f"{job_data.get('job_city')}, {job_data.get('job_state')}",
            link=job_data.get('job_apply_link'),
            status=status.NEW_NOT_VIEWED
        )
        for job_data in data.get('data', [])
    ]

if __name__ == "__main__":
    find_jobs_test()
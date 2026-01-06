import requests
import os
from dotenv import load_dotenv
from job import job, status

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
            id=f"{query_idx}_{i}",
            title=f"Job Title {i}",
            company=f"Company {i}",
            location=f"Location {i}",
            link=f"http://example.com/job{i}",
            status=status_map[i % 10]
        )
        for i in range(1, total_items + 1)
    ]



# Test function to demonstrate job finding
def find_jobs_test():

    api_key_name, api_key_value , url = load_api_keys()

    headers = {
        api_key_name: api_key_value
    }

    params = {
        "query": "Electrical Engineering - Canada - internship",
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
def find_jobs(query="Computer Engineering - Canada - internship", num_pages=2):

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

    return [
        job(
            id=i,
            title=job_data.get('job_title'),
            company=job_data.get('employer_name'),
            location=f"{job_data.get('job_city')}, {job_data.get('job_state')}",
            link=job_data.get('job_apply_link'),
            status=status.NEW_NOT_VIEWED
        )
        for i, job_data in enumerate(response.json().get('data', []), start=1)
    ]

if __name__ == "__main__":
    find_jobs_test()
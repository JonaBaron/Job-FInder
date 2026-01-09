import requests
import uuid
from models.job import job, status
from utils.session_helper import get_jsearch_api_from_session

# JSearch API URL
JSEARCH_URL = "https://api.openwebninja.com/jsearch/search"

def load_api_keys():
    """Load API keys from session (user-specific, stored in MongoDB)."""
    api_key_name, api_key_value = get_jsearch_api_from_session()
    return api_key_name, api_key_value, JSEARCH_URL


def is_api_configured():
    """Check if JSearch API is configured."""
    api_key_name, api_key_value = get_jsearch_api_from_session()
    return bool(api_key_name and api_key_value)

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
def find_jobs(query="Computer Engineering - Canada - internship", num_pages=10, query_idx=0, page=1):
    """
    Find jobs using JSearch API.

    Args:
        query: Search query string
        num_pages: Number of pages to fetch (10 jobs per page, max 10 pages = 100 jobs per call)
        query_idx: Index of the query in the queries list
        page: Starting page number for pagination

    Returns:
        List of job instances
    """
    # Check if API is configured
    if not is_api_configured():
        return []

    api_key_name, api_key_value, url = load_api_keys()

    headers = {
        api_key_name: api_key_value
    }

    params = {
        "query": query,
        "num_pages": num_pages,
        "page": page
    }

    response = requests.get(url, headers=headers, params=params)
    data = response.json()

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
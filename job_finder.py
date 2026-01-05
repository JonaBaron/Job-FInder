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

    jobs_list = []

    for job_data in data.get('data', []):
        job_instance = job(
            id=jobs_list.__len__() + 1,
            title=job_data.get('job_title'),
            company=job_data.get('employer_name'),
            location=f"{job_data.get('job_city')}, {job_data.get('job_state')}",
            link=job_data.get('job_apply_link'),
            status=status.NEW_NOT_VIEWED
        )
        jobs_list.append(job_instance)

    return jobs_list

if __name__ == "__main__":
    find_jobs_test()
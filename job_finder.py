import requests
import os
from dotenv import load_dotenv

load_dotenv()
api_key_name = os.getenv("JSearch_API_name")
api_key_value = os.getenv("JSearch_API_value")

url = "https://api.openwebninja.com/jsearch/search"

headers = {
    api_key_name: api_key_value
}

params = {
    "query": "Electrical Engineering - Canada - internship",
    "num_pages": 100
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
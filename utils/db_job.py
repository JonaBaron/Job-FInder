from pymongo import MongoClient
from datetime import datetime
from typing import List, Optional
from models.job import status as JobStatus


JOBS_COLLECTION = "jobs"
DEFAULT_DB_NAME = "job_finder_jobs"


def get_user_job_db(mongo_uri: str, db_name: str = None):
    """
    Get MongoDB connection to user's personal job database.
    Uses the user's own MongoDB URI.
    """
    if not mongo_uri:
        raise ValueError("MongoDB URI is required")
    client = MongoClient(mongo_uri)
    db = client[db_name or DEFAULT_DB_NAME]
    return client, db


def get_jobs_collection(mongo_uri: str, db_name: str = None):
    """Get the jobs collection from user's MongoDB."""
    client, db = get_user_job_db(mongo_uri, db_name)
    return client, db[JOBS_COLLECTION]


def create_job(
    mongo_uri: str,
    user_email: str,
    job_id: str,
    title: str,
    company: str,
    location: str,
    initial_link: str = None,
    job_status: int = JobStatus.NEW_NOT_VIEWED,
    db_name: str = None
) -> dict:
    """
    Create a new job entry in user's job database.
    Returns the created job document.
    """
    client, collection = get_jobs_collection(mongo_uri, db_name)
    try:
        now = datetime.utcnow()
        job_doc = {
            "job_id": job_id,
            "user_email": user_email,
            "title": title,
            "company": company,
            "location": location,
            "initial_link": initial_link,
            "user_links": [],  # User-added working links
            "status": job_status,
            "status_history": [
                {
                    "status": job_status,
                    "changed_at": now,
                    "note": "Initial status"
                }
            ],
            "first_fetched_at": now,
            "created_at": now,
            "updated_at": now,
        }
        result = collection.insert_one(job_doc)
        job_doc["_id"] = result.inserted_id
        return job_doc
    finally:
        client.close()


def get_job_by_id(mongo_uri: str, job_id: str, user_email: str, db_name: str = None) -> dict:
    """Get a job by its ID for a specific user."""
    client, collection = get_jobs_collection(mongo_uri, db_name)
    try:
        return collection.find_one({"job_id": job_id, "user_email": user_email})
    finally:
        client.close()


def get_all_jobs(mongo_uri: str, user_email: str, db_name: str = None) -> List[dict]:
    """Get all jobs for a specific user."""
    client, collection = get_jobs_collection(mongo_uri, db_name)
    try:
        return list(collection.find({"user_email": user_email}))
    finally:
        client.close()


def get_jobs_by_status(mongo_uri: str, user_email: str, job_status: int, db_name: str = None) -> List[dict]:
    """Get all jobs with a specific status for a user."""
    client, collection = get_jobs_collection(mongo_uri, db_name)
    try:
        return list(collection.find({"user_email": user_email, "status": job_status}))
    finally:
        client.close()


def update_job_status(
    mongo_uri: str,
    job_id: str,
    user_email: str,
    new_status: int,
    note: str = None,
    db_name: str = None
) -> bool:
    """
    Update job status and add to status history.
    Returns True if update was successful.
    """
    client, collection = get_jobs_collection(mongo_uri, db_name)
    try:
        now = datetime.utcnow()
        status_entry = {
            "status": new_status,
            "changed_at": now,
            "note": note
        }
        result = collection.update_one(
            {"job_id": job_id, "user_email": user_email},
            {
                "$set": {
                    "status": new_status,
                    "updated_at": now
                },
                "$push": {
                    "status_history": status_entry
                }
            }
        )
        return result.modified_count > 0
    finally:
        client.close()


def add_user_link(
    mongo_uri: str,
    job_id: str,
    user_email: str,
    link: str,
    description: str = None,
    db_name: str = None
) -> bool:
    """
    Add a user-provided working link to a job.
    Returns True if update was successful.
    """
    client, collection = get_jobs_collection(mongo_uri, db_name)
    try:
        link_entry = {
            "url": link,
            "description": description,
            "added_at": datetime.utcnow()
        }
        result = collection.update_one(
            {"job_id": job_id, "user_email": user_email},
            {
                "$push": {"user_links": link_entry},
                "$set": {"updated_at": datetime.utcnow()}
            }
        )
        return result.modified_count > 0
    finally:
        client.close()


def remove_user_link(
    mongo_uri: str,
    job_id: str,
    user_email: str,
    link_url: str,
    db_name: str = None
) -> bool:
    """
    Remove a user-provided link from a job.
    Returns True if update was successful.
    """
    client, collection = get_jobs_collection(mongo_uri, db_name)
    try:
        result = collection.update_one(
            {"job_id": job_id, "user_email": user_email},
            {
                "$pull": {"user_links": {"url": link_url}},
                "$set": {"updated_at": datetime.utcnow()}
            }
        )
        return result.modified_count > 0
    finally:
        client.close()


def get_job_status_history(mongo_uri: str, job_id: str, user_email: str, db_name: str = None) -> List[dict]:
    """Get the full status history of a job."""
    job = get_job_by_id(mongo_uri, job_id, user_email, db_name)
    if job:
        return job.get("status_history", [])
    return []


def get_job_links(mongo_uri: str, job_id: str, user_email: str, db_name: str = None) -> dict:
    """
    Get all links for a job (initial and user-added).
    Returns dict with 'initial_link' and 'user_links'.
    """
    job = get_job_by_id(mongo_uri, job_id, user_email, db_name)
    if job:
        return {
            "initial_link": job.get("initial_link"),
            "user_links": job.get("user_links", [])
        }
    return {"initial_link": None, "user_links": []}


def delete_job(mongo_uri: str, job_id: str, user_email: str, db_name: str = None) -> bool:
    """Delete a job. Returns True if deletion was successful."""
    client, collection = get_jobs_collection(mongo_uri, db_name)
    try:
        result = collection.delete_one({"job_id": job_id, "user_email": user_email})
        return result.deleted_count > 0
    finally:
        client.close()


def job_exists(mongo_uri: str, job_id: str, user_email: str, db_name: str = None) -> bool:
    """Check if a job already exists for a user."""
    job = get_job_by_id(mongo_uri, job_id, user_email, db_name)
    return job is not None


def bulk_create_jobs(
    mongo_uri: str,
    user_email: str,
    jobs: List[dict],
    db_name: str = None
) -> int:
    """
    Bulk create jobs from a list of job dictionaries.
    Each job dict should have: job_id, title, company, location, initial_link (optional)
    Returns the number of jobs created.
    """
    client, collection = get_jobs_collection(mongo_uri, db_name)
    try:
        now = datetime.utcnow()
        job_docs = []
        for job in jobs:
            job_status = job.get("status", JobStatus.NEW_NOT_VIEWED)
            job_doc = {
                "job_id": job["job_id"],
                "user_email": user_email,
                "title": job["title"],
                "company": job["company"],
                "location": job["location"],
                "initial_link": job.get("initial_link") or job.get("link"),
                "user_links": [],
                "status": job_status,
                "status_history": [
                    {
                        "status": job_status,
                        "changed_at": now,
                        "note": "Initial status"
                    }
                ],
                "first_fetched_at": now,
                "created_at": now,
                "updated_at": now,
            }
            job_docs.append(job_doc)

        if job_docs:
            result = collection.insert_many(job_docs)
            return len(result.inserted_ids)
        return 0
    finally:
        client.close()


def update_job_details(
    mongo_uri: str,
    job_id: str,
    user_email: str,
    title: str = None,
    company: str = None,
    location: str = None,
    db_name: str = None
) -> bool:
    """Update job details (title, company, location)."""
    client, collection = get_jobs_collection(mongo_uri, db_name)
    try:
        update_fields = {"updated_at": datetime.utcnow()}
        if title is not None:
            update_fields["title"] = title
        if company is not None:
            update_fields["company"] = company
        if location is not None:
            update_fields["location"] = location

        result = collection.update_one(
            {"job_id": job_id, "user_email": user_email},
            {"$set": update_fields}
        )
        return result.modified_count > 0
    finally:
        client.close()


def get_jobs_count_by_status(mongo_uri: str, user_email: str, db_name: str = None) -> dict:
    """Get count of jobs grouped by status for a user."""
    client, collection = get_jobs_collection(mongo_uri, db_name)
    try:
        pipeline = [
            {"$match": {"user_email": user_email}},
            {"$group": {"_id": "$status", "count": {"$sum": 1}}}
        ]
        result = list(collection.aggregate(pipeline))
        return {item["_id"]: item["count"] for item in result}
    finally:
        client.close()
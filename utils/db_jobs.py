from pymongo import MongoClient
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

# Jobs MongoDB connection
JOBS_MONGO_URI = os.getenv("JOBS_MONGO_URI")
JOBS_DB_NAME = os.getenv("JOBS_DB_NAME", "jobs_db")
JOBS_COLLECTION = "user_jobs"


def get_jobs_db_connection():
    """Get MongoDB client and database connection for jobs."""
    client = MongoClient(JOBS_MONGO_URI)
    db = client[JOBS_DB_NAME]
    return client, db


def get_jobs_collection():
    """Get the jobs collection."""
    client, db = get_jobs_db_connection()
    return client, db[JOBS_COLLECTION]


# ============================================
# LOAD USER DATA
# ============================================
def load_user_data(email: str) -> dict:
    """
    Load user's queries and jobs from database.
    Returns dict with 'queries' and 'jobs' lists.
    """
    client, collection = get_jobs_collection()
    try:
        user_data = collection.find_one({"user_id": email})
        if user_data:
            return {
                "queries": user_data.get("queries", []),
                "jobs": user_data.get("jobs", [])
            }
        return {"queries": [], "jobs": []}
    finally:
        client.close()


def get_user_queries(email: str) -> list:
    """Get user's saved queries."""
    data = load_user_data(email)
    return [q.get("query_text") for q in data.get("queries", [])]


def get_user_jobs(email: str) -> list:
    """Get user's saved jobs grouped by query index."""
    data = load_user_data(email)
    return data.get("jobs", [])


# ============================================
# SAVE USER DATA
# ============================================
def save_user_data(email: str, queries: list, jobs: list) -> bool:
    """
    Save user's queries and jobs to database.
    Handles deduplication by job link within each query.

    Args:
        email: User's email (user_id)
        queries: List of query strings
        jobs: List of lists, each containing job dicts for that query
    """
    client, collection = get_jobs_collection()
    try:
        # Build queries structure
        queries_data = []
        for query in queries:
            queries_data.append({
                "query_text": query,
                "created_at": datetime.utcnow()
            })

        # Build jobs structure with deduplication
        jobs_data = []
        for query_idx, query_jobs in enumerate(jobs):
            seen_links = set()
            deduplicated_jobs = []

            for job in query_jobs:
                job_dict = job_to_dict(job)
                link = job_dict.get("link", "")

                # Skip duplicates within same query
                if link and link in seen_links:
                    continue
                seen_links.add(link)
                deduplicated_jobs.append(job_dict)

            jobs_data.append(deduplicated_jobs)

        # Upsert user data
        result = collection.update_one(
            {"user_id": email},
            {
                "$set": {
                    "user_id": email,
                    "queries": queries_data,
                    "jobs": jobs_data,
                    "updated_at": datetime.utcnow()
                },
                "$setOnInsert": {
                    "created_at": datetime.utcnow()
                }
            },
            upsert=True
        )
        return result.modified_count > 0 or result.upserted_id is not None
    finally:
        client.close()


def job_to_dict(job) -> dict:
    """Convert job object to dictionary for storage."""
    if isinstance(job, dict):
        return job

    # Get existing history or create new
    history = getattr(job, 'history', None) or {
        "status_changes": [],
        "link_clicks": [],
        "link_edits": []
    }

    return {
        "job_id": job.id,
        "title": job.get_title(),
        "company": job.get_company(),
        "location": job.get_location(),
        "link": job.get_WEBLink(),
        "current_status": job.get_status(),
        "history": history,
        "created_at": getattr(job, 'created_at', datetime.utcnow().isoformat())
    }


# ============================================
# HISTORY LOGGING
# ============================================
def log_status_change(email: str, query_idx: int, job_id: str, from_status: int, to_status: int) -> bool:
    """Log a status change for a job."""
    client, collection = get_jobs_collection()
    try:
        # Find the job and append to status_changes
        result = collection.update_one(
            {
                "user_id": email,
                f"jobs.{query_idx}.job_id": job_id
            },
            {
                "$push": {
                    f"jobs.{query_idx}.$.history.status_changes": {
                        "from": from_status,
                        "to": to_status,
                        "timestamp": datetime.utcnow().isoformat()
                    }
                },
                "$set": {
                    f"jobs.{query_idx}.$.current_status": to_status,
                    "updated_at": datetime.utcnow()
                }
            }
        )
        return result.modified_count > 0
    finally:
        client.close()


def log_link_click(email: str, query_idx: int, job_id: str) -> bool:
    """Log when user clicks on a job link."""
    client, collection = get_jobs_collection()
    try:
        result = collection.update_one(
            {
                "user_id": email,
                f"jobs.{query_idx}.job_id": job_id
            },
            {
                "$push": {
                    f"jobs.{query_idx}.$.history.link_clicks": {
                        "timestamp": datetime.utcnow().isoformat()
                    }
                },
                "$set": {
                    "updated_at": datetime.utcnow()
                }
            }
        )
        return result.modified_count > 0
    finally:
        client.close()


def update_job_link(email: str, query_idx: int, job_id: str, old_link: str, new_link: str) -> bool:
    """Update a job's link and log the change."""
    client, collection = get_jobs_collection()
    try:
        result = collection.update_one(
            {
                "user_id": email,
                f"jobs.{query_idx}.job_id": job_id
            },
            {
                "$set": {
                    f"jobs.{query_idx}.$.link": new_link,
                    "updated_at": datetime.utcnow()
                },
                "$push": {
                    f"jobs.{query_idx}.$.history.link_edits": {
                        "old_link": old_link,
                        "new_link": new_link,
                        "timestamp": datetime.utcnow().isoformat()
                    }
                }
            }
        )
        return result.modified_count > 0
    finally:
        client.close()


# ============================================
# SYNC HELPERS
# ============================================
def sync_jobs_to_db(email: str, queries: list, jobs: list) -> bool:
    """
    Sync current session jobs to database.
    Merges with existing data, preserving history.
    """
    client, collection = get_jobs_collection()
    try:
        # Load existing data
        existing = collection.find_one({"user_id": email})
        existing_jobs = existing.get("jobs", []) if existing else []

        # Build job history map from existing data
        history_map = {}  # {job_id: history}
        for query_jobs in existing_jobs:
            for job in query_jobs:
                if isinstance(job, dict):
                    job_id = job.get("job_id")
                    if job_id:
                        history_map[job_id] = job.get("history", {
                            "status_changes": [],
                            "link_clicks": [],
                            "link_edits": []
                        })

        # Build new jobs data, preserving history
        jobs_data = []
        global_seen_links = set()

        for query_idx, query_jobs in enumerate(jobs):
            seen_links = set()
            deduplicated_jobs = []

            for job in query_jobs:
                job_dict = job_to_dict(job)
                link = job_dict.get("link", "")
                job_id = job_dict.get("job_id")

                # Skip duplicates
                if link and (link in seen_links or link in global_seen_links):
                    continue

                if link:
                    seen_links.add(link)
                    global_seen_links.add(link)

                # Preserve existing history if available
                if job_id and job_id in history_map:
                    job_dict["history"] = history_map[job_id]

                deduplicated_jobs.append(job_dict)

            jobs_data.append(deduplicated_jobs)

        # Build queries data
        queries_data = [{"query_text": q, "created_at": datetime.utcnow()} for q in queries]

        # Save to database
        result = collection.update_one(
            {"user_id": email},
            {
                "$set": {
                    "user_id": email,
                    "queries": queries_data,
                    "jobs": jobs_data,
                    "updated_at": datetime.utcnow()
                },
                "$setOnInsert": {
                    "created_at": datetime.utcnow()
                }
            },
            upsert=True
        )
        return result.modified_count > 0 or result.upserted_id is not None
    finally:
        client.close()


def load_jobs_from_db(email: str) -> tuple:
    """
    Load jobs from database and convert to job objects.
    Returns (queries, jobs) tuple.
    """
    from models.job import job as Job, status

    data = load_user_data(email)
    queries = [q.get("query_text") for q in data.get("queries", [])]

    jobs_data = data.get("jobs", [])
    jobs = []

    for query_jobs in jobs_data:
        query_job_objects = []
        for job_dict in query_jobs:
            job_obj = Job(
                id=job_dict.get("job_id"),
                title=job_dict.get("title"),
                company=job_dict.get("company"),
                location=job_dict.get("location"),
                link=job_dict.get("link"),
                status=job_dict.get("current_status", status.NEW_NOT_VIEWED)
            )
            # Attach history to job object
            job_obj.history = job_dict.get("history", {
                "status_changes": [],
                "link_clicks": [],
                "link_edits": []
            })
            query_job_objects.append(job_obj)
        jobs.append(query_job_objects)

    return queries, jobs

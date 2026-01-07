from pymongo import MongoClient
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

# Main MongoDB connection (fixed - stores user data)
MONGO_URI = os.getenv("MONGO_URI")
DB_NAME = os.getenv("MONGO_DB_NAME")
USERS_COLLECTION = "users"


def get_db_connection():
    """Get MongoDB client and database connection."""
    client = MongoClient(MONGO_URI)
    db = client[DB_NAME]
    return client, db


def get_users_collection():
    """Get the users collection."""
    client, db = get_db_connection()
    return client, db[USERS_COLLECTION]


def create_user(email: str, name: str = None, picture: str = None) -> dict:
    """
    Create a new user in the database.
    Returns the created user document.
    """
    client, collection = get_users_collection()
    try:
        user = {
            "email": email,
            "name": name,
            "picture": picture,
            "mongo_uri": None,  # User's own MongoDB URI
            "jsearch_api_key": None,  # User's own JSearch API key
            "jsearch_api_name": None,  # User's JSearch API header name
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow(),
        }
        result = collection.insert_one(user)
        user["_id"] = result.inserted_id
        return user
    finally:
        client.close()


def get_user_by_email(email: str) -> dict:
    """Get a user by their email address."""
    client, collection = get_users_collection()
    try:
        return collection.find_one({"email": email})
    finally:
        client.close()


def get_or_create_user(email: str, name: str = None, picture: str = None) -> dict:
    """Get existing user or create a new one if not exists."""
    user = get_user_by_email(email)
    if user is None:
        user = create_user(email, name, picture)
    return user


def update_user_mongo_uri(email: str, mongo_uri: str) -> bool:
    """
    Update user's personal MongoDB URI.
    Returns True if update was successful.
    """
    client, collection = get_users_collection()
    try:
        result = collection.update_one(
            {"email": email},
            {
                "$set": {
                    "mongo_uri": mongo_uri,
                    "updated_at": datetime.utcnow()
                }
            }
        )
        return result.modified_count > 0
    finally:
        client.close()


def update_user_jsearch_api(email: str, api_key: str, api_name: str = "x-rapidapi-key") -> bool:
    """
    Update user's JSearch API credentials.
    Returns True if update was successful.
    """
    client, collection = get_users_collection()
    try:
        result = collection.update_one(
            {"email": email},
            {
                "$set": {
                    "jsearch_api_key": api_key,
                    "jsearch_api_name": api_name,
                    "updated_at": datetime.utcnow()
                }
            }
        )
        return result.modified_count > 0
    finally:
        client.close()


def get_user_mongo_uri(email: str) -> str:
    """Get user's personal MongoDB URI."""
    user = get_user_by_email(email)
    if user:
        return user.get("mongo_uri")
    return None


def get_user_jsearch_api(email: str) -> tuple:
    """
    Get user's JSearch API credentials.
    Returns (api_name, api_key) tuple.
    """
    user = get_user_by_email(email)
    if user:
        return user.get("jsearch_api_name"), user.get("jsearch_api_key")
    return None, None


def delete_user(email: str) -> bool:
    """Delete a user by email. Returns True if deletion was successful."""
    client, collection = get_users_collection()
    try:
        result = collection.delete_one({"email": email})
        return result.deleted_count > 0
    finally:
        client.close()


def update_user_profile(email: str, name: str = None, picture: str = None) -> bool:
    """Update user profile info (name, picture)."""
    client, collection = get_users_collection()
    try:
        update_fields = {"updated_at": datetime.utcnow()}
        if name is not None:
            update_fields["name"] = name
        if picture is not None:
            update_fields["picture"] = picture

        result = collection.update_one(
            {"email": email},
            {"$set": update_fields}
        )
        return result.modified_count > 0
    finally:
        client.close()


def has_user_configured_api(email: str) -> bool:
    """Check if user has configured their own JSearch API key."""
    user = get_user_by_email(email)
    if user:
        return user.get("jsearch_api_key") is not None
    return False


def has_user_configured_mongo(email: str) -> bool:
    """Check if user has configured their own MongoDB URI."""
    user = get_user_by_email(email)
    if user:
        return user.get("mongo_uri") is not None
    return False

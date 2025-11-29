"""
Database configuration and connection utilities
"""

import os
from dotenv import load_dotenv
from supabase import create_client, Client

# Load environment variables
load_dotenv()

# Get Supabase credentials from environment
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")


def get_supabase_client() -> Client:
    """
    Create and return a Supabase client instance

    Returns:
        Client: Supabase client for database operations

    Raises:
        ValueError: If SUPABASE_URL or SUPABASE_KEY are not set
    """
    if not SUPABASE_URL or not SUPABASE_KEY:
        raise ValueError(
            "Missing Supabase credentials. Please set SUPABASE_URL and SUPABASE_KEY in .env file"
        )

    return create_client(SUPABASE_URL, SUPABASE_KEY)


def get_current_week_id() -> str:
    """
    Get current week ID in ISO format (e.g., "2025-W48")

    Returns:
        str: Week ID in format "YYYY-Wxx"
    """
    from datetime import datetime

    now = datetime.now()
    # Get ISO calendar week
    iso_year, iso_week, _ = now.isocalendar()
    return f"{iso_year}-W{iso_week:02d}"


def test_connection() -> bool:
    """
    Test the Supabase connection

    Returns:
        bool: True if connection successful, False otherwise
    """
    try:
        client = get_supabase_client()
        # Try a simple query to test connection
        response = client.table("hiring_signals").select("count", count="exact").limit(0).execute()
        print(f"✅ Successfully connected to Supabase!")
        print(f"   Current week ID: {get_current_week_id()}")
        return True
    except Exception as e:
        print(f"❌ Failed to connect to Supabase: {e}")
        return False


if __name__ == "__main__":
    # Test connection when run directly
    test_connection()

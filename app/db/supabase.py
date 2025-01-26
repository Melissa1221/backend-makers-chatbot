"""Supabase client configuration."""
from functools import lru_cache
from supabase import create_client, Client
from app.core.config import get_settings

@lru_cache()
def get_supabase() -> Client:
    """Get cached Supabase client instance."""
    settings = get_settings()
    if not settings.SUPABASE_URL or not settings.SUPABASE_KEY:
        raise ValueError(
            "Missing Supabase credentials. Please set SUPABASE_URL and SUPABASE_KEY in .env file"
        )
    return create_client(settings.SUPABASE_URL, settings.SUPABASE_KEY) 
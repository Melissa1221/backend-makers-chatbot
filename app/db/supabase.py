"""Supabase client configuration."""
from functools import lru_cache
from supabase import create_client, Client
from app.core.config import get_settings
from dotenv import load_dotenv
import os

load_dotenv()

@lru_cache()
def get_supabase() -> Client:
    """Get cached Supabase client instance."""
    settings = get_settings()
    if not settings.SUPABASE_URL or not settings.SUPABASE_KEY:
        raise ValueError(
            "Missing Supabase credentials. Please set SUPABASE_URL and SUPABASE_KEY in .env file"
        )
    return create_client(settings.SUPABASE_URL, settings.SUPABASE_KEY)

def get_supabase_client():
    """
    Crea y retorna una instancia del cliente de Supabase
    usando las credenciales del archivo .env
    """
    supabase_url = os.getenv("SUPABASE_URL")
    supabase_key = os.getenv("SUPABASE_KEY")
    
    if not supabase_url or not supabase_key:
        raise ValueError(
            "Las variables de entorno SUPABASE_URL y SUPABASE_KEY deben estar configuradas"
        )
    
    return create_client(supabase_url, supabase_key) 
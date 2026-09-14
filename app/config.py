import os
from dotenv import load_dotenv
from supabase import create_client, Client

# Load environment variables from .env file if present
load_dotenv()

class Settings:
    """Application settings loaded from environment variables."""

    SUPABASE_URL: str = os.getenv("SUPABASE_URL", "https://your_project_url.supabase.co")
    SUPABASE_KEY: str = os.getenv("SUPABASE_KEY", "your_anon_key")
    PORT: int = int(os.getenv("PORT", "8000"))

settings = Settings()

# Initialize Supabase client
supabase: Client = create_client(settings.SUPABASE_URL, settings.SUPABASE_KEY)

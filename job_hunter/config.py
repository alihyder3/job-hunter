"""Configuration manager for API credentials."""

import os
from typing import Optional
from dotenv import load_dotenv


class CredentialsManager:
    """Manages API credentials from environment variables."""
    
    def __init__(self) -> None:
        """Initialize and load environment variables."""
        load_dotenv()
        
    def fetch_adzuna_app_id(self) -> Optional[str]:
        """Retrieve Adzuna application ID."""
        return os.getenv("ADZUNA_APP_ID")
    
    def fetch_adzuna_app_key(self) -> Optional[str]:
        """Retrieve Adzuna application key."""
        return os.getenv("ADZUNA_APP_KEY")
    
    def validate_adzuna_credentials(self) -> bool:
        """Check if Adzuna credentials are configured."""
        return bool(self.fetch_adzuna_app_id() and self.fetch_adzuna_app_key())

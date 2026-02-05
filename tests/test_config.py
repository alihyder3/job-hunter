"""Tests for configuration manager."""

import os
from job_hunter.config import CredentialsManager


def test_credentials_manager_init() -> None:
    """Test credentials manager initialization."""
    manager = CredentialsManager()
    assert manager is not None


def test_fetch_adzuna_credentials_not_set() -> None:
    """Test fetching credentials when not set."""
    os.environ.pop("ADZUNA_APP_ID", None)
    os.environ.pop("ADZUNA_APP_KEY", None)
    
    manager = CredentialsManager()
    assert manager.fetch_adzuna_app_id() is None
    assert manager.fetch_adzuna_app_key() is None


def test_fetch_adzuna_credentials_when_set() -> None:
    """Test fetching credentials when set."""
    os.environ["ADZUNA_APP_ID"] = "test_id_123"
    os.environ["ADZUNA_APP_KEY"] = "test_key_456"
    
    manager = CredentialsManager()
    assert manager.fetch_adzuna_app_id() == "test_id_123"
    assert manager.fetch_adzuna_app_key() == "test_key_456"
    
    os.environ.pop("ADZUNA_APP_ID", None)
    os.environ.pop("ADZUNA_APP_KEY", None)


def test_validate_adzuna_credentials_missing() -> None:
    """Test validation when credentials are missing."""
    os.environ.pop("ADZUNA_APP_ID", None)
    os.environ.pop("ADZUNA_APP_KEY", None)
    
    manager = CredentialsManager()
    assert manager.validate_adzuna_credentials() is False


def test_validate_adzuna_credentials_present() -> None:
    """Test validation when credentials are present."""
    os.environ["ADZUNA_APP_ID"] = "valid_id"
    os.environ["ADZUNA_APP_KEY"] = "valid_key"
    
    manager = CredentialsManager()
    assert manager.validate_adzuna_credentials() is True
    
    os.environ.pop("ADZUNA_APP_ID", None)
    os.environ.pop("ADZUNA_APP_KEY", None)


def test_validate_adzuna_credentials_partial() -> None:
    """Test validation with only one credential set."""
    os.environ["ADZUNA_APP_ID"] = "only_id"
    os.environ.pop("ADZUNA_APP_KEY", None)
    
    manager = CredentialsManager()
    assert manager.validate_adzuna_credentials() is False
    
    os.environ.pop("ADZUNA_APP_ID", None)

"""Tests for API clients."""

from job_hunter.clients import AdzunaAPIClient, RemotiveAPIClient, ArbeitnowAPIClient


def test_adzuna_client_initialization() -> None:
    """Test Adzuna client can be initialized."""
    client = AdzunaAPIClient("test_app_id", "test_app_key")
    assert client.application_id == "test_app_id"
    assert client.application_key == "test_app_key"


def test_remotive_client_initialization() -> None:
    """Test Remotive client can be initialized."""
    client = RemotiveAPIClient()
    assert client is not None
    assert client.API_ENDPOINT == "https://remotive.com/api/remote-jobs"


def test_arbeitnow_client_initialization() -> None:
    """Test Arbeitnow client can be initialized."""
    client = ArbeitnowAPIClient()
    assert client is not None
    assert client.API_ENDPOINT == "https://www.arbeitnow.com/api/job-board-api"


def test_adzuna_base_endpoint() -> None:
    """Test Adzuna base endpoint is correct."""
    assert AdzunaAPIClient.BASE_ENDPOINT == "https://api.adzuna.com/v1/api/jobs"

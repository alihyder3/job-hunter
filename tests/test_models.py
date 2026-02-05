"""Tests for data models."""

from datetime import datetime
from job_hunter.models import JobPosting


def test_job_posting_creation() -> None:
    """Test creating a job posting instance."""
    posting = JobPosting(
        employer_name="TechCorp",
        role_title="Senior Developer",
        role_details="Looking for experienced developer",
        application_url="https://example.com/apply"
    )
    
    assert posting.employer_name == "TechCorp"
    assert posting.role_title == "Senior Developer"
    assert posting.submission_deadline is None


def test_job_posting_to_row_dict() -> None:
    """Test conversion to dictionary format."""
    posting = JobPosting(
        employer_name="DataInc",
        role_title="Data Analyst",
        role_details="Analyze data sets",
        application_url="https://example.com/job",
        submission_deadline="2026-03-01"
    )
    
    result = posting.to_row_dict()
    
    assert result["Company"] == "DataInc"
    assert result["Title"] == "Data Analyst"
    assert result["Description"] == "Analyze data sets"
    assert result["Apply Link"] == "https://example.com/job"
    assert result["Deadline"] == "2026-03-01"


def test_job_posting_missing_deadline() -> None:
    """Test that missing deadline shows as not specified."""
    posting = JobPosting(
        employer_name="StartupXYZ",
        role_title="Engineer",
        role_details="Build stuff",
        application_url="https://example.com"
    )
    
    result = posting.to_row_dict()
    assert result["Deadline"] == "Not specified"


def test_job_posting_with_optional_fields() -> None:
    """Test posting with all optional fields."""
    now = datetime.now()
    posting = JobPosting(
        employer_name="CompanyABC",
        role_title="Manager",
        role_details="Manage team",
        application_url="https://example.com",
        submission_deadline="2026-12-31",
        discovered_date=now,
        source_platform="TestAPI",
        location_info="Remote"
    )
    
    assert posting.discovered_date == now
    assert posting.source_platform == "TestAPI"
    assert posting.location_info == "Remote"

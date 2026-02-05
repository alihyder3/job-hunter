"""Data structures for job postings."""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class JobPosting:
    """Represents a single job opportunity from any source."""
    
    employer_name: str
    role_title: str
    role_details: str
    application_url: str
    submission_deadline: Optional[str] = None
    discovered_date: Optional[datetime] = None
    source_platform: Optional[str] = None
    location_info: Optional[str] = None
    
    def to_row_dict(self) -> dict[str, str]:
        """Convert to dictionary for export."""
        return {
            "Company": self.employer_name,
            "Title": self.role_title,
            "Description": self.role_details,
            "Apply Link": self.application_url,
            "Deadline": self.submission_deadline or "Not specified"
        }

"""API client implementations for job search platforms."""

from abc import ABC, abstractmethod
from datetime import datetime, timedelta
from typing import Optional
import requests

from .models import JobPosting


class JobSearchClient(ABC):
    """Abstract base for job search API clients."""
    
    @abstractmethod
    def search_opportunities(
        self,
        search_terms: str,
        nation: str,
        municipalities: list[str],
        days_back: int
    ) -> list[JobPosting]:
        """Fetch job postings matching criteria."""
        pass


class AdzunaAPIClient(JobSearchClient):
    """Client for Adzuna job search API."""
    
    BASE_ENDPOINT = "https://api.adzuna.com/v1/api/jobs"
    
    def __init__(self, application_id: str, application_key: str) -> None:
        """Initialize with credentials."""
        self.application_id = application_id
        self.application_key = application_key
    
    def search_opportunities(
        self,
        search_terms: str,
        nation: str,
        municipalities: list[str],
        days_back: int
    ) -> list[JobPosting]:
        """Search Adzuna for jobs."""
        postings: list[JobPosting] = []
        
        country_lower = nation.lower()
        location_filter = " OR ".join(municipalities) if municipalities else ""
        
        query_params: dict[str, str | int] = {
            "app_id": self.application_id,
            "app_key": self.application_key,
            "results_per_page": 50,
            "what": search_terms,
            "where": location_filter,
            "max_days_old": days_back,
            "content-type": "application/json"
        }
        
        endpoint_url = f"{self.BASE_ENDPOINT}/{country_lower}/search/1"
        
        try:
            response = requests.get(endpoint_url, params=query_params, timeout=15)
            response.raise_for_status()
            data = response.json()
            
            for job_entry in data.get("results", []):
                posting = JobPosting(
                    employer_name=job_entry.get("company", {}).get("display_name", "Unknown"),
                    role_title=job_entry.get("title", "No title"),
                    role_details=job_entry.get("description", "No description available")[:500],
                    application_url=job_entry.get("redirect_url", ""),
                    discovered_date=datetime.now(),
                    source_platform="Adzuna",
                    location_info=job_entry.get("location", {}).get("display_name", "")
                )
                postings.append(posting)
                
        except requests.RequestException as error:
            print(f"Adzuna API error: {error}")
        
        return postings


class RemotiveAPIClient(JobSearchClient):
    """Client for Remotive job search API."""
    
    API_ENDPOINT = "https://remotive.com/api/remote-jobs"
    
    def search_opportunities(
        self,
        search_terms: str,
        nation: str,
        municipalities: list[str],
        days_back: int
    ) -> list[JobPosting]:
        """Search Remotive for remote jobs."""
        postings: list[JobPosting] = []
        
        query_params: dict[str, str | int] = {
            "search": search_terms,
            "limit": 50
        }
        
        try:
            response = requests.get(self.API_ENDPOINT, params=query_params, timeout=15)
            response.raise_for_status()
            data = response.json()
            
            cutoff_date = datetime.now() - timedelta(days=days_back)
            
            for job_entry in data.get("jobs", []):
                pub_date_str = job_entry.get("publication_date", "")
                try:
                    pub_date = datetime.fromisoformat(pub_date_str.replace("Z", "+00:00"))
                    if pub_date < cutoff_date:
                        continue
                except (ValueError, AttributeError):
                    continue
                
                posting = JobPosting(
                    employer_name=job_entry.get("company_name", "Unknown"),
                    role_title=job_entry.get("title", "No title"),
                    role_details=job_entry.get("description", "No description")[:500],
                    application_url=job_entry.get("url", ""),
                    discovered_date=pub_date,
                    source_platform="Remotive",
                    location_info=job_entry.get("candidate_required_location", "Remote")
                )
                postings.append(posting)
                
        except requests.RequestException as error:
            print(f"Remotive API error: {error}")
        
        return postings


class ArbeitnowAPIClient(JobSearchClient):
    """Client for Arbeitnow job search API."""
    
    API_ENDPOINT = "https://www.arbeitnow.com/api/job-board-api"
    
    def search_opportunities(
        self,
        search_terms: str,
        nation: str,
        municipalities: list[str],
        days_back: int
    ) -> list[JobPosting]:
        """Search Arbeitnow for jobs."""
        postings: list[JobPosting] = []
        
        try:
            response = requests.get(self.API_ENDPOINT, timeout=15)
            response.raise_for_status()
            data = response.json()
            
            cutoff_date = datetime.now() - timedelta(days=days_back)
            search_lower = search_terms.lower()
            
            for job_entry in data.get("data", []):
                title_text = job_entry.get("title", "").lower()
                if search_lower not in title_text:
                    continue
                
                created_str = job_entry.get("created_at", "")
                try:
                    created_date = datetime.fromtimestamp(int(created_str))
                    if created_date < cutoff_date:
                        continue
                except (ValueError, TypeError):
                    continue
                
                posting = JobPosting(
                    employer_name=job_entry.get("company_name", "Unknown"),
                    role_title=job_entry.get("title", "No title"),
                    role_details=job_entry.get("description", "No description")[:500],
                    application_url=job_entry.get("url", ""),
                    discovered_date=created_date,
                    source_platform="Arbeitnow",
                    location_info=job_entry.get("location", "")
                )
                postings.append(posting)
                
        except requests.RequestException as error:
            print(f"Arbeitnow API error: {error}")
        
        return postings

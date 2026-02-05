"""Command-line interface for job search aggregator."""

import argparse
import sys
from typing import List

from .clients import AdzunaAPIClient, RemotiveAPIClient, ArbeitnowAPIClient, JobSearchClient
from .config import CredentialsManager
from .exporters import DataExporter
from .models import JobPosting


class JobSearchOrchestrator:
    """Coordinates job searches across multiple platforms."""
    
    def __init__(self, credentials: CredentialsManager) -> None:
        """Initialize orchestrator with credentials."""
        self.credentials = credentials
        self.active_clients: List[JobSearchClient] = []
        
        if credentials.validate_adzuna_credentials():
            adzuna_client = AdzunaAPIClient(
                credentials.fetch_adzuna_app_id() or "",
                credentials.fetch_adzuna_app_key() or ""
            )
            self.active_clients.append(adzuna_client)
        
        self.active_clients.append(RemotiveAPIClient())
        self.active_clients.append(ArbeitnowAPIClient())
    
    def execute_search(
        self,
        keywords: str,
        country: str,
        cities: List[str],
        days: int
    ) -> List[JobPosting]:
        """Run search across all active clients."""
        all_results: List[JobPosting] = []
        
        for client in self.active_clients:
            platform_results = client.search_opportunities(
                search_terms=keywords,
                nation=country,
                municipalities=cities,
                days_back=days
            )
            all_results.extend(platform_results)
        
        return all_results


def create_argument_parser() -> argparse.ArgumentParser:
    """Build CLI argument parser."""
    parser = argparse.ArgumentParser(
        description="Multi-platform job search aggregator",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  job-hunter --keywords "python developer" --country us --cities "New York" "San Francisco" --days 7
  job-hunter -k "data scientist" -c gb -t "London" -d 14 --output jobs.xlsx
        """
    )
    
    parser.add_argument(
        "-k", "--keywords",
        required=True,
        help="Job search keywords or terms"
    )
    
    parser.add_argument(
        "-c", "--country",
        required=True,
        help="Country code (e.g., us, gb, de)"
    )
    
    parser.add_argument(
        "-t", "--cities",
        nargs="+",
        default=[],
        help="One or more city names to search in"
    )
    
    parser.add_argument(
        "-d", "--days",
        type=int,
        choices=range(7, 15),
        metavar="DAYS",
        default=7,
        help="Filter jobs posted within last N days (7-14)"
    )
    
    parser.add_argument(
        "-o", "--output",
        default="job_results",
        help="Output filename without extension (default: job_results)"
    )
    
    parser.add_argument(
        "-f", "--format",
        choices=["csv", "xlsx", "both"],
        default="both",
        help="Export format (default: both)"
    )
    
    return parser


def main() -> None:
    """Main CLI entry point."""
    parser = create_argument_parser()
    args = parser.parse_args()
    
    credentials = CredentialsManager()
    
    print("=== Job Hunter - Multi-Platform Search ===\n")
    print(f"Keywords: {args.keywords}")
    print(f"Country: {args.country}")
    print(f"Cities: {', '.join(args.cities) if args.cities else 'All'}")
    print(f"Days back: {args.days}")
    print()
    
    orchestrator = JobSearchOrchestrator(credentials)
    
    if not orchestrator.active_clients:
        print("ERROR: No API clients available. Check credentials.")
        sys.exit(1)
    
    print(f"Active sources: {len(orchestrator.active_clients)}")
    print("Searching...\n")
    
    results = orchestrator.execute_search(
        keywords=args.keywords,
        country=args.country,
        cities=args.cities,
        days=args.days
    )
    
    print(f"Found {len(results)} job postings\n")
    
    if not results:
        print("No jobs found matching your criteria.")
        return
    
    if args.format in ["csv", "both"]:
        csv_filename = f"{args.output}.csv"
        DataExporter.save_as_csv(results, csv_filename)
    
    if args.format in ["xlsx", "both"]:
        xlsx_filename = f"{args.output}.xlsx"
        DataExporter.save_as_xlsx(results, xlsx_filename)
    
    print("\n=== Search Complete ===")


if __name__ == "__main__":
    main()

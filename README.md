# Job Hunter 🎯

A powerful Python CLI tool that aggregates job postings from multiple public APIs (Adzuna, Remotive, and Arbeitnow). Search for jobs using keywords, filter by location and date, and export results to CSV or Excel formats.

## Features

- 🔍 **Multi-Platform Search**: Searches across Adzuna, Remotive, and Arbeitnow simultaneously
- 🌍 **Location Filtering**: Filter by country and multiple cities
- 📅 **Date Range**: Find jobs posted within the last 7-14 days
- 📊 **Multiple Export Formats**: Export to CSV, XLSX, or both
- 🔐 **Secure Configuration**: API keys managed via environment variables
- 🎨 **Type-Safe**: Full type hints for better code quality
- ✅ **Well-Tested**: Comprehensive test suite included

## Requirements

- Python 3.12 or higher
- API credentials for Adzuna (optional, Remotive and Arbeitnow don't require keys)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/alihyder3/job-hunter.git
cd job-hunter
```

2. Install the package:
```bash
pip install -e .
```

3. Set up environment variables (copy the example file):
```bash
cp .env.example .env
```

4. Edit `.env` and add your Adzuna API credentials:
```
ADZUNA_APP_ID=your_app_id_here
ADZUNA_APP_KEY=your_app_key_here
```

To obtain Adzuna API keys, visit: https://developer.adzuna.com/

## Usage

### Basic Search

Search for Python developer jobs in the US:
```bash
job-hunter --keywords "python developer" --country us --days 7
```

### Search with Multiple Cities

Search in specific cities:
```bash
job-hunter --keywords "data scientist" --country gb --cities "London" "Manchester" "Edinburgh" --days 14
```

### Custom Output

Specify output filename and format:
```bash
job-hunter -k "frontend engineer" -c de -t "Berlin" -d 10 -o results -f xlsx
```

### Full Example

```bash
job-hunter \
  --keywords "machine learning engineer" \
  --country us \
  --cities "San Francisco" "New York" "Seattle" \
  --days 7 \
  --output ml_jobs \
  --format both
```

## Command-Line Options

| Option | Short | Description | Required | Default |
|--------|-------|-------------|----------|---------|
| `--keywords` | `-k` | Job search keywords | Yes | - |
| `--country` | `-c` | Country code (e.g., us, gb, de) | Yes | - |
| `--cities` | `-t` | One or more city names | No | All |
| `--days` | `-d` | Days back to search (7-14) | No | 7 |
| `--output` | `-o` | Output filename (no extension) | No | job_results |
| `--format` | `-f` | Export format: csv, xlsx, or both | No | both |

## Output Format

Results are exported with the following columns:

- **Company**: Employer name
- **Title**: Job title/position
- **Description**: Job description (truncated to 500 characters)
- **Apply Link**: URL to apply for the position
- **Deadline**: Application deadline (if available)

## Development

### Install Development Dependencies

```bash
pip install -e ".[dev]"
```

### Run Tests

```bash
pytest
```

### Run Tests with Coverage

```bash
pytest --cov=job_hunter --cov-report=html
```

### Type Checking

```bash
mypy job_hunter
```

## Project Structure

```
job-hunter/
├── job_hunter/
│   ├── __init__.py       # Package initialization
│   ├── cli.py            # Command-line interface
│   ├── clients.py        # API client implementations
│   ├── config.py         # Configuration management
│   ├── exporters.py      # Data export utilities
│   └── models.py         # Data models
├── tests/
│   ├── __init__.py
│   ├── test_clients.py
│   ├── test_config.py
│   ├── test_exporters.py
│   └── test_models.py
├── .env.example          # Environment variables template
├── .gitignore           # Git ignore rules
├── LICENSE              # MIT License
├── pyproject.toml       # Project configuration
└── README.md            # This file
```

## API Sources

### Adzuna
- **Requires**: API key (free tier available)
- **Coverage**: Multiple countries with detailed job listings
- **Website**: https://developer.adzuna.com/

### Remotive
- **Requires**: No API key
- **Coverage**: Remote jobs worldwide
- **Website**: https://remotive.com/

### Arbeitnow
- **Requires**: No API key
- **Coverage**: European job market focus
- **Website**: https://www.arbeitnow.com/

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Troubleshooting

### No results found
- Check your keywords are not too specific
- Verify the country code is correct (use 2-letter ISO codes)
- Try increasing the `--days` parameter
- Ensure your internet connection is working

### Adzuna API errors
- Verify your API credentials in the `.env` file
- Check if you've exceeded your API rate limit
- Ensure the country code is supported by Adzuna

### Import errors
- Make sure you've installed the package: `pip install -e .`
- Verify Python version is 3.12 or higher: `python --version`

## Support

For issues, questions, or contributions, please visit the [GitHub repository](https://github.com/alihyder3/job-hunter).
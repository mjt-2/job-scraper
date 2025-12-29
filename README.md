# Job Scraper

Finds entry-level data jobs in Canada.

## What it does

Searches for entry-level positions in:
- Data Analyst
- Data Engineer  
- Software Developer
- Business Analyst

Filters out senior roles and creates a webpage with job listings.

## Setup
```bash
pip install requests pandas openpyxl matplotlib seaborn
```

Get API keys from https://developer.adzuna.com/

Create `config.py`:
```python
APP_ID = "your_app_id"
APP_KEY = "your_api_key"
```

## Run it
```bash
python scraper.py
```

Opens in your browser with job listings from the last 3 days.

## Files

- `scraper.py` - Main job finder
- `analyzer.py` - Creates charts and analysis
- `requirements.txt` - Dependencies

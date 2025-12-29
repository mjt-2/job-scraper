import requests
import pandas as pd
from datetime import datetime
import webbrowser
import os

# YOUR API CREDENTIALS
APP_ID = "605233a1"
APP_KEY = "12a886c373fa40fcfc075fe3a5a84947"

def is_entry_level(title, description):
    """
    Filter to ONLY keep entry-level positions
    """
    text = (str(title) + " " + str(description)).lower()
    
    # EXCLUDE if these words appear
    exclude_keywords = [
        'senior', 'sr.', 'sr ', 'lead', 'principal', 'staff',
        'manager', 'director', 'head of', 'chief', 'vp',
        '5+ years', '5 years', '3+ years', '3 years',
        'experienced', 'expert'
    ]
    
    for keyword in exclude_keywords:
        if keyword in text:
            return False
    
    # INCLUDE if these words appear
    include_keywords = [
        'junior', 'jr.', 'jr ', 'entry', 'entry-level',
        'graduate', 'new grad', 'associate', 'co-op',
        'intern', '0-2 years', '0-1 year', 'early career'
    ]
    
    for keyword in include_keywords:
        if keyword in text:
            return True
    
    return False

def scrape_entry_level_jobs(job_titles, location="Canada", days=3):
    """
    Scrape entry-level jobs from last X days
    """
    
    base_url = "https://api.adzuna.com/v1/api/jobs/ca/search"
    all_jobs = []
    
    print(f"\nSearching jobs posted in last {days} days...")
    print(f"Location: {location}")
    print("="*60)
    
    for job_title in job_titles:
        print(f"\nSearching: {job_title}...", end=" ")
        
        results_per_page = 50
        num_pages = 4
        
        for page in range(1, num_pages + 1):
            url = f"{base_url}/{page}"
            
            params = {
                "app_id": APP_ID,
                "app_key": APP_KEY,
                "what": job_title,
                "where": location,
                "results_per_page": results_per_page,
                "max_days_old": days,
                "content-type": "application/json"
            }
            
            try:
                response = requests.get(url, params=params)
                response.raise_for_status()
                data = response.json()
                
                if 'results' in data and len(data['results']) > 0:
                    
                    for job in data['results']:
                        title = job.get('title', '')
                        description = job.get('description', '')
                        
                        if is_entry_level(title, description):
                            job_data = {
                                'Title': title,
                                'Company': job.get('company', {}).get('display_name', 'N/A'),
                                'Location': job.get('location', {}).get('display_name', 'N/A'),
                                'Salary Min': job.get('salary_min', ''),
                                'Salary Max': job.get('salary_max', ''),
                                'Posted': job.get('created', 'N/A'),
                                'Job Type': job_title,
                                'Apply URL': job.get('redirect_url', 'N/A')
                            }
                            all_jobs.append(job_data)
                else:
                    break
                    
            except Exception as e:
                print(f"Error: {e}")
                break
        
        print(f"Done")
    
    return pd.DataFrame(all_jobs)

if __name__ == "__main__":
    
    print("\n" + "="*60)
    print("ENTRY-LEVEL JOB FINDER")
    print("="*60)
    print("Data Source: Adzuna API")
    print("             (aggregates from Indeed, LinkedIn, company sites)")
    print("="*60)
    
    job_types = [
        "data analyst",
        "data engineer",
        "software developer",
        "business analyst"
    ]
    
    DAYS = 3  # Last 3 days
    
    # Scrape jobs
    df = scrape_entry_level_jobs(
        job_titles=job_types,
        location="Canada",
        days=DAYS
    )
    
    if len(df) == 0:
        print("\n" + "="*60)
        print("NO JOBS FOUND")
        print("="*60)
        exit()
    
    # Remove duplicates
    df = df.drop_duplicates(subset=['Title', 'Company'])
    
    print("\n" + "="*60)
    print(f"FOUND: {len(df)} ENTRY-LEVEL JOBS")
    print("="*60)
    
    # Save Excel (backup)
    filename = 'entry_level_jobs.xlsx'
    df.to_excel(filename, index=False)
    
    # CREATE WEBSITE
    html_file = 'jobs.html'
    
    html = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Entry-Level Jobs</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
            background: #f5f5f5;
        }}
        h1 {{
            color: #333;
            text-align: center;
        }}
        .stats {{
            background: white;
            padding: 20px;
            border-radius: 8px;
            margin-bottom: 20px;
            text-align: center;
        }}
        .job {{
            background: white;
            padding: 20px;
            margin-bottom: 15px;
            border-radius: 8px;
            border-left: 4px solid #4CAF50;
        }}
        .job-title {{
            font-size: 20px;
            font-weight: bold;
            color: #333;
            margin-bottom: 10px;
        }}
        .company {{
            color: #666;
            font-size: 16px;
            margin-bottom: 5px;
        }}
        .location {{
            color: #999;
            font-size: 14px;
            margin-bottom: 10px;
        }}
        .apply-btn {{
            display: inline-block;
            background: #4CAF50;
            color: white;
            padding: 10px 20px;
            text-decoration: none;
            border-radius: 5px;
            margin-top: 10px;
        }}
        .apply-btn:hover {{
            background: #45a049;
        }}
    </style>
</head>
<body>
    <h1>Entry-Level Jobs - {datetime.now().strftime('%B %d, %Y')}</h1>
    <div class="stats">
        <strong>{len(df)} jobs found</strong> | Last {DAYS} days | Canada
    </div>
"""
    
    for idx, row in df.iterrows():
        html += f"""
    <div class="job">
        <div class="job-title">{row['Title']}</div>
        <div class="company">{row['Company']}</div>
        <div class="location">{row['Location']}</div>
        <div>Posted: {row['Posted']}</div>
        <a href="{row['Apply URL']}" target="_blank" class="apply-btn">Apply Now</a>
    </div>
"""
    
    html += """
</body>
</html>
"""
    
    with open(html_file, 'w', encoding='utf-8') as f:
        f.write(html)
    
    # AUTO-OPEN IN BROWSER
    webbrowser.open('file://' + os.path.realpath(html_file))
    
    print(f"\nOpened jobs in your browser!")
    print(f"Files saved: {filename} and {html_file}")
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import re
from collections import Counter

# Load the data
df = pd.read_excel('adzuna_jobs_all.xlsx')
entry_df = pd.read_excel('adzuna_entry_level.xlsx')

print("=" * 60)
print("JOB MARKET ANALYSIS - ONTARIO DATA ROLES")
print("=" * 60)

# 1. SKILL EXTRACTION
print("\n1. EXTRACTING SKILLS FROM JOB DESCRIPTIONS...")

skills = {
    'SQL': ['sql', 'mysql', 'postgresql', 'tsql', 't-sql', 'pl/sql'],
    'Python': ['python', 'pandas', 'numpy', 'scikit-learn', 'sklearn'],
    'Tableau': ['tableau'],
    'Power BI': ['power bi', 'powerbi', 'power-bi'],
    'Excel': ['excel', 'advanced excel', 'vba'],
    'R': [r'\br\b', 'r programming', 'rstudio'],
    'Java': ['java'],
    'AWS': ['aws', 'amazon web services', 's3', 'ec2'],
    'Azure': ['azure', 'microsoft azure'],
    'Spark': ['spark', 'pyspark', 'apache spark'],
    'Hadoop': ['hadoop'],
    'Machine Learning': ['machine learning', 'ml ', 'scikit', 'tensorflow', 'pytorch'],
    'Statistics': ['statistics', 'statistical analysis', 'statistical modeling'],
    'Data Visualization': ['data visualization', 'data viz', 'dashboarding']
}

def extract_skills(description):
    if pd.isna(description):
        return []
    
    description_lower = str(description).lower()
    found_skills = []
    
    for skill_name, patterns in skills.items():
        for pattern in patterns:
            if re.search(pattern, description_lower):
                found_skills.append(skill_name)
                break
    
    return found_skills

df['skills'] = df['description'].apply(extract_skills)

# Count skill frequencies
all_skills = []
for skill_list in df['skills']:
    all_skills.extend(skill_list)

skill_counts = Counter(all_skills)

print("\nMost Requested Skills:")
print("-" * 40)
total_jobs = len(df)
for skill, count in skill_counts.most_common(10):
    percentage = (count / total_jobs) * 100
    print(f"{skill:20s} {count:4d} jobs ({percentage:5.1f}%)")

# 2. SALARY ANALYSIS
print("\n\n2. SALARY ANALYSIS...")
print("-" * 40)

# Filter jobs with salary info
salary_df = df[(df['salary_min'].notna()) & (df['salary_max'].notna())]
salary_df['salary_avg'] = (salary_df['salary_min'] + salary_df['salary_max']) / 2

print(f"Jobs with salary info: {len(salary_df)} out of {len(df)} ({len(salary_df)/len(df)*100:.1f}%)")

if len(salary_df) > 0:
    print(f"\nOverall Salary Stats:")
    print(f"  Average: ${salary_df['salary_avg'].mean():,.0f}")
    print(f"  Median:  ${salary_df['salary_avg'].median():,.0f}")
    print(f"  Min:     ${salary_df['salary_avg'].min():,.0f}")
    print(f"  Max:     ${salary_df['salary_avg'].max():,.0f}")
    
    # By job type
    print(f"\nAverage Salary by Role:")
    for role in df['search_term'].unique():
        role_salary = salary_df[salary_df['search_term'] == role]['salary_avg']
        if len(role_salary) > 0:
            print(f"  {role:20s} ${role_salary.mean():,.0f}")

# 3. LOCATION ANALYSIS
print("\n\n3. TOP HIRING LOCATIONS...")
print("-" * 40)
top_locations = df['location'].value_counts().head(10)
for location, count in top_locations.items():
    print(f"{location:30s} {count:4d} jobs")

# 4. TOP HIRING COMPANIES
print("\n\n4. TOP HIRING COMPANIES...")
print("-" * 40)
top_companies = df['company'].value_counts().head(10)
for company, count in top_companies.items():
    print(f"{company:30s} {count:4d} jobs")

# 5. ENTRY-LEVEL INSIGHTS
print("\n\n5. ENTRY-LEVEL JOB INSIGHTS...")
print("-" * 40)
print(f"Total entry-level jobs: {len(entry_df)}")
print(f"Percentage of total: {len(entry_df)/len(df)*100:.1f}%")

entry_distribution = entry_df['search_term'].value_counts()
print(f"\nEntry-level jobs by type:")
for role, count in entry_distribution.items():
    print(f"  {role:20s} {count:4d} jobs")

# 6. CREATE VISUALIZATIONS
print("\n\n6. CREATING VISUALIZATIONS...")
print("-" * 40)

# Set style
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 8)

# Visualization 1: Top Skills Bar Chart
fig, axes = plt.subplots(2, 2, figsize=(15, 12))

top_10_skills = skill_counts.most_common(10)
skills_names = [s[0] for s in top_10_skills]
skills_counts = [s[1] for s in top_10_skills]

axes[0, 0].barh(skills_names, skills_counts, color='steelblue')
axes[0, 0].set_xlabel('Number of Job Postings')
axes[0, 0].set_title('Top 10 Most Requested Skills')
axes[0, 0].invert_yaxis()

# Visualization 2: Jobs by Role
role_counts = df['search_term'].value_counts()
axes[0, 1].bar(role_counts.index, role_counts.values, color=['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728'])
axes[0, 1].set_ylabel('Number of Jobs')
axes[0, 1].set_title('Job Postings by Role Type')
axes[0, 1].tick_params(axis='x', rotation=45)

# Visualization 3: Entry-level vs Total
entry_comparison = pd.DataFrame({
    'Total Jobs': df['search_term'].value_counts(),
    'Entry-Level': entry_df['search_term'].value_counts()
}).fillna(0)

entry_comparison.plot(kind='bar', ax=axes[1, 0], color=['steelblue', 'orange'])
axes[1, 0].set_ylabel('Number of Jobs')
axes[1, 0].set_title('Total vs Entry-Level Jobs by Role')
axes[1, 0].tick_params(axis='x', rotation=45)
axes[1, 0].legend()

# Visualization 4: Top Locations
top_10_locations = df['location'].value_counts().head(10)
axes[1, 1].barh(range(len(top_10_locations)), top_10_locations.values, color='coral')
axes[1, 1].set_yticks(range(len(top_10_locations)))
axes[1, 1].set_yticklabels(top_10_locations.index)
axes[1, 1].set_xlabel('Number of Jobs')
axes[1, 1].set_title('Top 10 Hiring Locations')
axes[1, 1].invert_yaxis()

plt.tight_layout()
plt.savefig('job_market_analysis.png', dpi=300, bbox_inches='tight')
print("Saved: job_market_analysis.png")

# 7. SAVE DETAILED ANALYSIS
print("\n7. SAVING DETAILED ANALYSIS...")

# Create formatted Excel
    filename = 'entry_level_jobs_24h.xlsx'
    df.to_excel(filename, index=False)
    
    # CREATE WEBSITE INSTEAD
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
        <strong>{len(df)} jobs found</strong> | Last 24 hours | Canada
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
    import webbrowser
    import os
    webbrowser.open('file://' + os.path.realpath(html_file))
    
    print(f"\nOpened jobs in your browser!")
    print(f"Files saved: {filename} and {html_file}")
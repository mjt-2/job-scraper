# Job Scraper for Entry-Level Positions

I built this because I got tired of manually checking Indeed and LinkedIn every day for entry-level data jobs. Now I just run this script and get a clean list of jobs I can actually apply to.

## What It Does

Pulls job postings from Adzuna (which aggregates from Indeed, LinkedIn, company sites, etc.) and filters them to show only entry-level positions. No more scrolling past "Senior Data Scientist - 10 years experience required" listings.

## Why I Made This

Honestly, job hunting sucks. I was spending hours clicking through job boards, copying links, and losing track of what I'd already seen. This automates all of that - I run it once a day and get fresh postings in a nice format I can actually use.

## Getting Started

You'll need Python installed. If you don't have it, grab it from python.org.

**Clone this:**
```bash
git clone https://github.com/YOUR_USERNAME/job-scraper.git
cd job-scraper
```

**Install the packages:**
```bash
pip install requests pandas openpyxl matplotlib seaborn
```

**Get API access:**
- Go to developer.adzuna.com and make an account (it's free)
- They'll give you an App ID and API Key
- Make a file called `config.py` and put this in it:
```python
APP_ID = "your_app_id"
APP_KEY = "your_api_key"
```

**Run it:**
```bash
python scraper.py
```

It'll open your browser with all the jobs. Click "Apply Now" on the ones you want.

## How It Works

The scraper searches for data analyst, data engineer, software developer, and business analyst roles. It grabs about 200 jobs per category, then filters out anything with "senior", "manager", "5+ years experience", etc. in the title or description.

What you get is a list of jobs that are actually entry-level - junior roles, associate positions, new grad opportunities, that kind of thing.

## The Files

- `scraper.py` - the main script, finds entry-level jobs from the last 3 days
- `adzuna_scraper.py` - pulls a bigger dataset (600+ jobs) if you want to do analysis
- `analyzer.py` - creates charts showing which skills are most requested, salary ranges, top companies hiring, etc.
- `config.py` - your API keys (don't commit this to GitHub!)

## What I Learned

This was my first real project using APIs and web scraping. Learned a ton about:
- Working with REST APIs
- Filtering and cleaning data with pandas
- Building something I actually use every day

The analyzer part was interesting too - turns out SQL shows up in like 85% of data analyst job postings. Good to know.

## Limitations

The free API tier gives you 250 calls per month. Each run uses about 8 calls (4 job types, 2 pages each on average). So you can run it ~30 times a month, which is about once a day. Honestly that's enough.

If you hit the limit, just wait til next month or make another free account with a different email.

## Stuff I Want to Add

- Maybe hook it up to Google Sheets so I can check from my phone
- Could add email notifications for new jobs
- Thinking about building a thing that matches jobs to my resume

For now though, it does what I need it to do.

## Using This for Your Own Job Search

Feel free to fork this and modify it. You might want to change the job types being searched (line 91 in scraper.py), or adjust the location from "Canada" to wherever you're looking for work.

The entry-level filter is pretty aggressive - if it's missing jobs you think it should catch, you can add more keywords to the `include_keywords` list on line 25.

## Notes

Built this while finishing up my Computer Engineering degree at McMaster. Currently looking for data analyst positions in Ontario, so if you're hiring... well, you can see I know how to code.

Data comes from Adzuna's API which aggregates postings from a bunch of different sources. It updates daily so you're getting current listings, not jobs from 3 weeks ago that are already filled.

## License

Do whatever you want with this code. MIT License.
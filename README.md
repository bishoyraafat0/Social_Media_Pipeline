# Social Media Pipeline

## Overview
This project is a **data engineering pipeline** that fetches, transforms, and analyzes social media data from **YouTube** and **X (Twitter)**. The goal is to compute engagement metrics, identify top posts, and provide insights for daily social media activity.  
- **Keyword tracked:** `Python`  
- **Data sources:** YouTube API & X (Twitter) API  
The pipeline fetches posts containing the keyword, normalizes the data into a unified schema, calculates engagement metrics, and saves the results into both CSV files and a SQLite database.  
> **Note on Twitter Data:** Some engagement metrics from Twitter (likes, comments, etc.) may appear empty. This is due to the **limitations of the free Twitter API**, which does not provide full engagement data. Full metrics require a Paid API tier. The pipeline is fully functional, and missing Twitter data is expected under the free tier.

---

## Features
- Fetch posts from multiple social media platforms (YouTube & Twitter)  
- Normalize and transform data into a unified format  
- Calculate engagement metrics: likes, comments, shares, and overall engagement score  
- Compute daily engagement metrics per platform  
- Identify top 3 posts per platform and top 5 overall  
- Compute 7-day moving average of engagement  
- Save results in CSV and SQLite  
- Logging for error handling and process tracking  

---

## Requirements
- Python 3.8+  
- Packages: `pandas`, `requests`, `python-dotenv`  

Install dependencies via pip:
```bash
pip install -r requirements.txt
```
Or individually:
```bash
pip install pandas requests python-dotenv
```

---

## Setup
1. Clone the repository:
```bash
git clone https://github.com/bishoyraafat0/Social_Media_Pipeline.git
cd Social_Media_Pipeline
```

2. Create a `.env` file in the root folder with your API keys:
```env
YT_API_KEY=your_youtube_api_key
X_BEARER_TOKEN=your_x_twitter_bearer_token
```

> **Note:** Do not share your `.env` file publicly.  

---

## Running the Pipeline
Execute the pipeline script:
```bash
python main.py
```

This will:  
- Fetch posts containing the keyword `Python` from YouTube & X (Twitter)  
- Transform and analyze the data  
- Save results in:  
  - `social_data.db` (SQLite database)  
  - `daily_metrics.csv`  
  - `top_posts.csv`  
  - `moving_averages.csv`  

---

## Optional Automation
You can schedule the pipeline to run automatically every day using:  
- **Windows:** Task Scheduler  
- **Linux/Mac:** Cron Job  

---

## Logging
All pipeline logs are saved to:
```
pipeline.log
```
This includes info messages, warnings, and errors encountered during execution.

---

## Project Structure
```
Social_Media_Pipeline/
│
├── main.py           # Main pipeline script
├── fetch.py          # Fetch data from APIs
├── transform.py      # Transform and normalize data
├── analyze.py        # Analyze data and compute metrics
├── utils.py          # Helper functions and logging
├── .env              # API keys (not tracked in git)
├── requirements.txt  # Python dependencies
└── README.md         # This file
```

---

## Author
**Bishoy Raafat** – Data Engineer & Social Media Analytics Enthusiast

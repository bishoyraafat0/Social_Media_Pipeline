import requests
import pandas as pd
from datetime import datetime, timedelta, timezone
import time
from utils import load_env_vars, log_message

def fetch_youtube(keyword, days=7, max_results=20):
    """Fetch data from YouTube API"""
    try:
        env_vars = load_env_vars()
        url = "https://www.googleapis.com/youtube/v3/search"
        published_after = (datetime.now(timezone.utc) - timedelta(days=days)).isoformat()
        
        params = {
            "part": "snippet",
            "q": keyword,
            "type": "video",
            "order": "date",
            "maxResults": max_results,
            "publishedAfter": published_after,
            "key": env_vars['YT_API_KEY']
        }
        
        r = requests.get(url, params=params)
        r.raise_for_status()
        data = r.json()
        
        rows = []
        for item in data.get("items", []):
            video_id = item["id"].get("videoId")
            if not video_id:
                continue
            snippet = item["snippet"]
            
            # Fetch video statistics
            stats_url = "https://www.googleapis.com/youtube/v3/videos"
            stats_params = {
                "part": "statistics",
                "id": video_id,
                "key": env_vars['YT_API_KEY']
            }
            stats_r = requests.get(stats_url, params=stats_params)
            stats_r.raise_for_status()
            stats = stats_r.json().get("items", [{}])[0].get("statistics", {})
            
            rows.append({
                "post_id": video_id,
                "platform": "YouTube",
                "author_id": snippet.get("channelId", ""),
                "content": snippet.get("title", "") + " " + snippet.get("description", ""),
                "like_count": int(stats.get("likeCount", 0)),
                "comment_count": int(stats.get("commentCount", 0)),
                "share_count": 0,  # YouTube does not provide share data directly
                "posted_at": snippet.get("publishedAt", ""),
                "fetched_at": datetime.now(timezone.utc).isoformat()
            })
        log_message(f"Fetched {len(rows)} videos from YouTube for keyword '{keyword}'")
        return pd.DataFrame(rows)
    except requests.exceptions.RequestException as e:
        log_message(f"Error fetching from YouTube: {e}", level='error')
        return pd.DataFrame()

def fetch_twitter(keyword, days=7, max_results=20, retries=3, wait=15):
    """Fetch data from X (Twitter) API"""
    try:
        env_vars = load_env_vars()
        url = "https://api.twitter.com/2/tweets/search/recent"
        headers = {"Authorization": f"Bearer {env_vars['X_BEARER_TOKEN']}"}
        query = f"{keyword} OR #{keyword}"
        start_time = (datetime.now(timezone.utc) - timedelta(days=days)).isoformat()
        
        params = {
            "query": query,
            "max_results": max_results,
            "tweet.fields": "public_metrics,author_id,created_at",
            "start_time": start_time
        }
        
        for attempt in range(retries):
            try:
                r = requests.get(url, headers=headers, params=params)
                r.raise_for_status()
                data = r.json().get("data", [])
                if not data:
                    log_message(f"No Twitter data found for keyword '{keyword}' in last {days} days", level='warning')
                    return pd.DataFrame()
                rows = []
                for item in data:
                    metrics = item.get("public_metrics", {})
                    rows.append({
                        "post_id": item.get("id", ""),
                        "platform": "Twitter",
                        "author_id": item.get("author_id", ""),
                        "content": item.get("text", ""),
                        "like_count": metrics.get("like_count", 0),
                        "comment_count": metrics.get("reply_count", 0),
                        "share_count": metrics.get("retweet_count", 0),
                        "posted_at": item.get("created_at", ""),
                        "fetched_at": datetime.now(timezone.utc).isoformat()
                    })
                log_message(f"Fetched {len(rows)} tweets from Twitter API")
                return pd.DataFrame(rows)
            except requests.exceptions.HTTPError as e:
                if r.status_code == 429:
                    log_message(f"Too Many Requests. Waiting {wait} seconds before retrying...", level='warning')
                    time.sleep(wait)
                else:
                    log_message(f"Twitter Error: {r.text}", level='error')
                    return pd.DataFrame()
        log_message(f"Failed to fetch Twitter data after {retries} retries", level='error')
        return pd.DataFrame()
    except Exception as e:
        log_message(f"Error fetching from Twitter: {e}", level='error')
        return pd.DataFrame()

import pandas as pd
from utils import log_message

def transform_data(yt_df, tw_df):
    """Unify data from YouTube and Twitter"""
    try:
        # Merge data
        all_posts = pd.concat([yt_df, tw_df], ignore_index=True) if not tw_df.empty else yt_df
        if all_posts.empty:
            log_message("No data to transform", level='warning')
            return pd.DataFrame()
        
        # Convert posted_at to datetime
        all_posts["posted_at"] = pd.to_datetime(all_posts["posted_at"], errors="coerce")
        
        # Fill missing values
        all_posts.fillna({"like_count": 0, "comment_count": 0, "share_count": 0}, inplace=True)
        
        # Add engagement_score
        all_posts["engagement_score"] = all_posts["like_count"] + all_posts["comment_count"] + all_posts["share_count"]
        
        # Add date column
        all_posts["date"] = all_posts["posted_at"].dt.date
        
        log_message(f"Transformed {len(all_posts)} posts")
        return all_posts
    except Exception as e:
        log_message(f"Error transforming data: {e}", level='error')
        return pd.DataFrame()

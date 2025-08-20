import pandas as pd
from utils import log_message

def analyze_data(df):
    """Analyze data and calculate metrics"""
    try:
        if df.empty:
            log_message("No data to analyze", level='warning')
            return pd.DataFrame(), pd.DataFrame(), pd.DataFrame()
        
        # Daily metrics
        daily_metrics = df.groupby(["platform", "date"]).agg({
            "post_id": "count",
            "like_count": "sum",
            "comment_count": "sum",
            "share_count": "sum",
            "engagement_score": "sum"
        }).reset_index().rename(columns={"post_id": "post_count"})
        
        # Top 3 posts per platform
        top_per_platform = df.groupby("platform", group_keys=False).apply(
            lambda x: x.sort_values("engagement_score", ascending=False).head(3)
        ).reset_index(drop=True)
        
        # Top 5 posts overall
        top_overall = df.sort_values("engagement_score", ascending=False).head(5)
        
        # Combine top posts
        top_posts = pd.concat([top_overall, top_per_platform]).drop_duplicates("post_id")
        
        # 7-day moving average
        moving_avg = df.groupby(["platform", "date"])["engagement_score"].mean().reset_index()
        moving_avg["moving_avg_7d"] = moving_avg.groupby("platform")["engagement_score"].transform(
            lambda x: x.rolling(window=7, min_periods=1).mean()
        )
        
        log_message("Analysis completed")
        return df, daily_metrics, top_posts, moving_avg
    except Exception as e:
        log_message(f"Error in analysis: {e}", level='error')
        return pd.DataFrame(), pd.DataFrame(), pd.DataFrame(), pd.DataFrame()

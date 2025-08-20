
from transform import transform_data
from analyze import analyze_data
import sqlite3
from utils import log_message
from fetch import fetch_youtube, fetch_twitter


def main(keyword="Python", days=7, max_results=20):
    """Execute the pipeline"""
    try:
        # Fetch data
        yt_df = fetch_youtube(keyword, days, max_results)
        tw_df = fetch_twitter(keyword, days, max_results)
        
        # Transform data
        all_posts = transform_data(yt_df, tw_df)
        if all_posts.empty:
            log_message("No posts to process", level='warning')
            return
        
        # Analyze data
        posts, daily_metrics, top_posts, moving_avg = analyze_data(all_posts)
        
        # Save to SQLite
        conn = sqlite3.connect('social_data.db')
        posts.to_sql('posts', conn, if_exists='replace', index=False)
        conn.close()
        
        # Save metrics to CSV
        daily_metrics.to_csv("daily_metrics.csv", index=False)
        top_posts.to_csv("top_posts.csv", index=False)
        moving_avg.to_csv("moving_averages.csv", index=False)
        
        log_message(f"Pipeline completed! Saved {len(posts)} posts, {len(daily_metrics)} daily metrics, {len(top_posts)} top posts, {len(moving_avg)} moving averages")
        print(f"Pipeline completed! Files saved:")
        print(f"social_data.db -> {len(posts)} posts")
        print(f"daily_metrics.csv -> {len(daily_metrics)} rows")
        print(f"top_posts.csv -> {len(top_posts)} rows")
        print(f"moving_averages.csv -> {len(moving_avg)} rows")
    except Exception as e:
        log_message(f"Pipeline error: {e}", level='error')
        print(f"Pipeline error: {e}")

if __name__ == "__main__":
    main()

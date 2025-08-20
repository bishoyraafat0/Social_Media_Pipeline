import sqlite3
import pandas as pd

# Connect to the database
conn = sqlite3.connect('social_data.db')

# Read the posts table
df = pd.read_sql_query("SELECT * FROM posts", conn)

# Save as CSV
df.to_csv('posts_exported.csv', index=False)

# Display number of rows
print(f"Saved {len(df)} posts to posts_exported.csv")

# Close the connection
conn.close()

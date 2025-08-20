import sqlite3
import pandas as pd

conn = sqlite3.connect('social_data.db')

df = pd.read_sql_query("SELECT * FROM posts", conn)

print(df.head(50))

print(f"Total posts: {len(df)}")

conn.close()
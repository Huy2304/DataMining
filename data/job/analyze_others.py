import pandas as pd
from sqlalchemy import create_engine
import sys
import os

# Connect to DB
DB_URI = "postgresql://user:password@localhost:5432/it_jobs_db"
engine = create_engine(DB_URI)


def analyze_others():
    print("Fetching jobs classified as 'Other'...")
    query = "SELECT job_title, subfield, language FROM it_jobs_analysis WHERE subfield = 'Other'"
    df = pd.read_sql(query, engine)

    if df.empty:
        print("No 'Other' jobs found.")
        return

    print(f"Found {len(df)} jobs classified as 'Other'.")
    print("\n--- Top 20 Job Titles in 'Other' ---")
    print(df["job_title"].value_counts().head(20))

    print("\n--- Random Sample of 20 ---")
    print(df[["job_title", "language"]].sample(20))


if __name__ == "__main__":
    analyze_others()

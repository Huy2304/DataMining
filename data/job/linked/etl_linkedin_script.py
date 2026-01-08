import pandas as pd
from sqlalchemy import create_engine
import uuid
from datetime import datetime
import re
import sys
import os

# Ensure data/job is in sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

try:
    from mappings import get_normalized_subfield, LANGUAGES, TECHNOLOGIES
except ImportError:
    print("Warning: Could not import mappings.py. Using local normalization logic.")

    def get_normalized_subfield(job_title, current_subfield=None):
        return "Other"


DB_URI = "postgresql://user:password@localhost:5432/it_jobs_db"
engine = create_engine(DB_URI)

# CSV File Path
CSV_FILE = "clean_jobs_linkedin.csv"


def clean_and_normalize_linkedin_data(file_path):
    print(f"Reading {file_path}...")
    try:
        df = pd.read_csv(file_path)
    except Exception as e:
        print(f"Error reading CSV: {e}")
        return None

    print(f"Raw rows: {len(df)}")

    # 'job_title' <- 'title'
    df["job_title"] = df["title"]

    # 'company' <- 'company'
    # Keep as is

    # 'date_posted' <- 'date_posted'
    df["date_posted"] = pd.to_datetime(df["date_posted"], errors="coerce")

    # 'id' - Generate UUIDs
    df["id"] = [uuid.uuid4() for _ in range(len(df))]

    df["created_at"] = datetime.now()
    # Add Source
    df["source"] = "LinkedIn"

    # Extract Skills (Language & Technologies) from Description
    try:
        from mappings import LANGUAGES, TECHNOLOGIES
    except ImportError:
        print("Error: Could not import LANGUAGES and TECHNOLOGIES from mappings.py")
        return None

    def extract_keywords(text, keyword_dict):
        if not isinstance(text, str):
            return None
        found = []
        text_lower = text.lower()
        for name, pattern in keyword_dict.items():
            if re.search(pattern, text_lower):
                found.append(name)
        return ", ".join(sorted(found)) if found else None

    print("Extracting skills from descriptions...")
    df["description"] = df["description"].fillna("")

    df["language"] = df["description"].apply(lambda x: extract_keywords(x, LANGUAGES))
    df["technologies"] = df["description"].apply(
        lambda x: extract_keywords(x, TECHNOLOGIES)
    )

    #  Normalize Subfield using Shared Mapping
    print("Normalizing subfields...")
    df["subfield"] = df["job_title"].apply(lambda x: get_normalized_subfield(x, None))

    # --- 4. Select Final Columns ---
    final_df = df[
        [
            "id",
            "language",
            "subfield",
            "technologies",
            "company",
            "date_posted",
            "job_title",
            "created_at",
            "source",
        ]
    ].copy()

    # Filter out rows where date_posted is NaT
    final_df = final_df.dropna(subset=["date_posted"])

    print(f"Processed rows ready for insert: {len(final_df)}")
    return final_df


def insert_to_db(df):
    if df is None or df.empty:
        print("No data to insert.")
        return

    print("Inserting data into database...")
    try:
        df.to_sql("it_jobs_analysis", engine, if_exists="append", index=False)
        print(f"Successfully inserted {len(df)} rows.")
    except Exception as e:
        print(f"Error inserting to DB: {e}")


if __name__ == "__main__":
    processed_df = clean_and_normalize_linkedin_data(CSV_FILE)
    if processed_df is not None:
        insert_to_db(processed_df)

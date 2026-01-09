import pandas as pd
import glob
import os
import logging
from sqlalchemy import create_engine
import uuid

# Setup Logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# DB Connection
DB_URI = "postgresql://user:password@localhost:5432/it_jobs_db"
engine = create_engine(DB_URI)


def load_so_data_to_db():
    csv_files = glob.glob("202*_Q*.csv")
    if not csv_files:
        logger.warning("No CSV files found matching '202*_Q*.csv'")
        return

    logger.info(f"Found {len(csv_files)} files: {csv_files}")

    total_inserted = 0

    for file_path in csv_files:
        try:
            logger.info(f"Reading {file_path}...")
            # Columns in CSV: creation_date, title, tags, view_count, score, answer_count, comment_count
            df = pd.read_csv(file_path)

            # Rename columns to match DB schema
            # DB: id, so_id (maybe missing in CSV?), title, view_count, answer_count, score, date_posted, created_at

            # The query in stackoverflow.ipynb suggests columns:
            # id (so_id?), creation_date, title, tags, view_count, score, answer_count, comment_count

            # Let's verify columns exist
            required_cols = [
                "title",
                "tags",
                "view_count",
                "score",
                "answer_count",
                "creation_date",
            ]
            if not all(col in df.columns for col in required_cols):
                logger.warning(
                    f"Skipping {file_path}: Missing columns. Found: {df.columns.tolist()}"
                )
                continue

            # Prepare DataFrame for Insert
            df_insert = pd.DataFrame()
            df_insert["title"] = df["title"]
            df_insert["view_count"] = df["view_count"].fillna(0).astype(int)
            df_insert["answer_count"] = df["answer_count"].fillna(0).astype(int)
            df_insert["score"] = df["score"].fillna(0).astype(int)
            df_insert["date_posted"] = pd.to_datetime(df["creation_date"]).dt.date
            df_insert["tags"] = df["tags"]

            # SO ID - The CSV might have 'id' column which is the PostId
            if "id" in df.columns:
                df_insert["so_id"] = df["id"]
            else:
                # Generate fake unique ID if missing? Or skip?
                # Ideally we need SO ID to avoid duplicates
                logger.warning(
                    f"File {file_path} missing 'id' column (StackOverflow Post ID). Skipping SO ID mapping."
                )
                df_insert["so_id"] = None

            # Generate Internal UUID
            df_insert["id"] = [uuid.uuid4() for _ in range(len(df_insert))]

            # Clean Tags: Replace '><' with '|' or ','
            # Example: <python><pandas> -> python,pandas
            def clean_tags(tag_str):
                if not isinstance(tag_str, str):
                    return None
                return tag_str.replace("><", ",").replace("<", "").replace(">", "")

            df_insert["tags"] = df_insert["tags"].apply(clean_tags)

            # Insert to DB
            # Use 'append'
            logger.info(f"Inserting {len(df_insert)} rows from {file_path}...")
            df_insert.to_sql(
                "stackoverflow_posts", engine, if_exists="append", index=False
            )

            total_inserted += len(df_insert)

        except Exception as e:
            logger.error(f"Failed to process {file_path}: {e}")

    logger.info(f"✅ Total inserted: {total_inserted} rows.")


if __name__ == "__main__":
    load_so_data_to_db()

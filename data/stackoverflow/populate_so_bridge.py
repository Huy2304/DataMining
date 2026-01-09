import logging
import pandas as pd
from sqlalchemy import create_engine, text
import sys
import os

# Setup Logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# DB Connection
DB_URI = "postgresql://user:password@localhost:5432/it_jobs_db"
engine = create_engine(DB_URI)


def populate_so_bridge():
    """
    Reads tags from stackoverflow_posts, splits them, and populates:
      1. tech_meta (Unified list of tech - Category 'Tag')
      2. stackoverflow_tech_bridge
    """
    logger.info("Fetching StackOverflow posts...")

    # Batch processing is better for large datasets, but let's start simple
    # Assuming tags are like "|python|pandas|dataframe|" or "python,pandas" depending on source
    # The StackOverflow public dataset usually has tags like "python|pandas" or just strings.

    query = "SELECT id, tags FROM stackoverflow_posts WHERE tags IS NOT NULL"

    # Use chunksize for memory efficiency if data is huge
    chunk_size = 10000
    total_processed = 0

    for chunk_df in pd.read_sql(query, engine, chunksize=chunk_size):
        if chunk_df.empty:
            continue

        tech_meta_set = set()
        bridge_rows = []

        for _, row in chunk_df.iterrows():
            tags_raw = row["tags"]
            if not tags_raw:
                continue

            # StackOverflow tags often look like '<python><pandas>' or 'python|pandas'
            # Let's clean it up.
            # If standard SO dump: <tag1><tag2>
            # If CSV import: tag1|tag2

            clean_tags = []
            if "<" in tags_raw:
                clean_tags = (
                    tags_raw.replace("><", "|")
                    .replace("<", "")
                    .replace(">", "")
                    .split("|")
                )
            elif "|" in tags_raw:
                clean_tags = tags_raw.split("|")
            else:
                clean_tags = tags_raw.split(",")  # Fallback

            for tag in clean_tags:
                tag = tag.strip()
                if tag:
                    tech_meta_set.add((tag, "StackOverflow Tag"))
                    bridge_rows.append({"post_id": row["id"], "tech_name": tag})

        if not bridge_rows:
            continue

        # Bulk Insert Logic
        df_tech = pd.DataFrame(list(tech_meta_set), columns=["tech_name", "category"])
        df_bridge = pd.DataFrame(bridge_rows)
        df_bridge.drop_duplicates(inplace=True)

        with engine.begin() as conn:
            # Tech Meta
            df_tech.to_sql("temp_tech_meta_so", conn, if_exists="replace", index=False)
            conn.execute(
                text("""
                INSERT INTO tech_meta (tech_name, category)
                SELECT tech_name, category FROM temp_tech_meta_so
                ON CONFLICT (tech_name) DO NOTHING;
            """)
            )
            conn.execute(text("DROP TABLE temp_tech_meta_so"))

            # Bridge
            df_bridge.to_sql("temp_so_bridge", conn, if_exists="replace", index=False)
            conn.execute(
                text("""
                INSERT INTO stackoverflow_tech_bridge (post_id, tech_name)
                SELECT post_id::UUID, tech_name FROM temp_so_bridge
                ON CONFLICT (post_id, tech_name) DO NOTHING;
            """)
            )
            conn.execute(text("DROP TABLE temp_so_bridge"))

        total_processed += len(chunk_df)
        logger.info(
            f"Processed batch of {len(chunk_df)} posts. Total: {total_processed}"
        )

    logger.info("✅ StackOverflow Bridge populated.")


if __name__ == "__main__":
    populate_so_bridge()

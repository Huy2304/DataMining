import pandas as pd
from sqlalchemy import create_engine, text
import logging
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from mappings import get_normalized_subfield

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Database Connection
DB_URI = "postgresql://user:password@localhost:5432/it_jobs_db"
engine = create_engine(DB_URI)


def normalize_subfields():
    """
    Normalizes the subfield column in it_jobs_analysis table using the shared mappings.
    """

    logger.info("Fetching current subfields and titles...")
    query = "SELECT id, job_title, subfield FROM it_jobs_analysis"
    df = pd.read_sql(query, engine)

    if df.empty:
        logger.warning("No data found in database.")
        return

    logger.info(f"Loaded {len(df)} records.")

    # Apply Logic from mappings.py
    df["new_subfield"] = df.apply(
        lambda row: get_normalized_subfield(row["job_title"], row["subfield"]), axis=1
    )

    logger.info("Preparing to update database...")

    # Calculate changes stats
    changes = df[df["subfield"] != df["new_subfield"]]
    logger.info(f"Identified {len(changes)} rows to update out of {len(df)}.")

    if changes.empty:
        logger.info("No changes needed.")
        return

    logger.info("Sample changes:")
    print(changes[["job_title", "subfield", "new_subfield"]].head(10))

    # Create a temp mapping dataframe
    updates_df = changes[["id", "new_subfield"]].rename(
        columns={"new_subfield": "subfield"}
    )

    with engine.begin() as conn:
        # Create temp table
        conn.execute(
            text("CREATE TEMP TABLE subfield_updates (id UUID, subfield VARCHAR)")
        )

        updates_df.to_sql("subfield_updates", conn, if_exists="append", index=False)

        update_query = """
        UPDATE it_jobs_analysis
        SET subfield = subfield_updates.subfield
        FROM subfield_updates
        WHERE it_jobs_analysis.id = subfield_updates.id
        """
        conn.execute(text(update_query))
        logger.info("Database updated successfully.")

        conn.execute(text("DROP TABLE subfield_updates"))


if __name__ == "__main__":
    normalize_subfields()

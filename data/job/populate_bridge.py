import logging
import pandas as pd
from sqlalchemy import create_engine, text
import sys
import os

# Adjust path to import mappings
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from mappings import LANGUAGES, TECHNOLOGIES

# Setup Logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# DB Connection
DB_URI = "postgresql://user:password@localhost:5432/it_jobs_db"
engine = create_engine(DB_URI)


def populate_bridge_tables():
    """
    Reads the 'language' and 'technologies' columns from it_jobs_analysis,
    parses the CSV strings, and populates the:
      1. tech_meta (Unified list of all tech)
      2. job_tech_bridge (Links Job -> Tech)
    """
    logger.info("Fetching jobs with extracted skills...")

    # Select only necessary columns
    query = "SELECT id, language, technologies FROM it_jobs_analysis"
    df = pd.read_sql(query, engine)

    if df.empty:
        logger.warning("No jobs found in it_jobs_analysis.")
        return

    logger.info(f"Processing {len(df)} jobs...")

    # Data structures to hold new rows
    tech_meta_set = set()  # To store unique (tech_name, category)
    bridge_rows = []  # To store (job_id, tech_name)

    # --- Helper to process comma-separated strings ---
    def process_skills(job_id, skill_str):
        if not skill_str or pd.isna(skill_str):
            return

        # Split by comma and strip whitespace
        skills = [s.strip() for s in skill_str.split(",") if s.strip()]

        for skill in skills:
            # Determine category based on mappings
            # Default to "technology" if not found in LANGUAGES map
            # This is a simple heuristic; you might want more robust logic if mappings overlap
            category = "technology"

            # Check if skill exists in LANGUAGES map keys (case-insensitive check is better but keys are title case)
            # Mappings.py has "Python", "JavaScript" etc.
            # Let's check if the skill matches a key in LANGUAGES
            if skill in LANGUAGES:
                category = "language"

            # Add to Tech Meta (Unique Set)
            tech_meta_set.add((skill, category))

            # Add to Bridge
            bridge_rows.append({"job_id": job_id, "tech_name": skill})

    # --- Iterate through DataFrame ---
    for _, row in df.iterrows():
        # Process Technologies (Unified Column)
        process_skills(row["id"], row["technologies"])

    if not bridge_rows:
        logger.warning("No skills found to process.")
        return

    # --- Convert to DataFrames ---
    # Fix: Explicitly specify columns as a list of strings, distinct from the data
    df_tech_meta = pd.DataFrame(
        data=list(tech_meta_set), columns=["tech_name", "category"]
    )
    df_bridge = pd.DataFrame(bridge_rows)

    # Remove duplicates in bridge (in case a job lists "Python" twice by mistake)
    df_bridge.drop_duplicates(inplace=True)

    logger.info(f"Found {len(df_tech_meta)} unique technologies.")
    logger.info(f"Generated {len(df_bridge)} bridge records.")

    # --- Database Operations ---
    with engine.begin() as conn:
        # 1. Insert Tech Meta (Ignore duplicates)
        # We use INSERT ... ON CONFLICT DO NOTHING
        logger.info("Inserting into tech_meta...")

        # Doing this in a loop or batch is safer than to_sql for "ON CONFLICT"
        # However, to_sql doesn't support ON CONFLICT easily.
        # Strategy: Load to TEMP table -> Insert Ignore into Main

        df_tech_meta.to_sql("temp_tech_meta", conn, if_exists="replace", index=False)

        conn.execute(
            text("""
            INSERT INTO tech_meta (tech_name, category)
            SELECT tech_name, category FROM temp_tech_meta
            ON CONFLICT (tech_name) DO NOTHING;
        """)
        )
        conn.execute(text("DROP TABLE temp_tech_meta"))

        # 2. Insert Bridge Table
        # First, clear existing bridge entries for these jobs?
        # Or just use ON CONFLICT DO NOTHING?
        # Let's assume we want to sync. A clean way is "INSERT ON CONFLICT DO NOTHING"

        logger.info("Inserting into job_tech_bridge...")

        df_bridge.to_sql("temp_job_bridge", conn, if_exists="replace", index=False)

        conn.execute(
            text("""
            INSERT INTO job_tech_bridge (job_id, tech_name)
            SELECT job_id::UUID, tech_name FROM temp_job_bridge
            ON CONFLICT (job_id, tech_name) DO NOTHING;
        """)
        )
        conn.execute(text("DROP TABLE temp_job_bridge"))

    logger.info("✅ Bridge tables populated successfully.")


if __name__ == "__main__":
    populate_bridge_tables()

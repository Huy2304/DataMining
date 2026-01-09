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


def normalize_companies(df):
    """
    Normalizes company names to handle duplicates like 'Viec Oi client' vs 'Việc Ơi IT Client'.
    """
    # Mapping for known company duplicates
    company_map = {
        "Viec Oi client": "Viec Oi Client",
        "Việc Ơi IT Client": "Viec Oi Client",
        "Viec Oi IT Client": "Viec Oi Client",
        # Add more as discovered
    }

    def clean_company(name):
        if not name:
            return None
        name = name.strip()
        return company_map.get(name, name)

    return df["company"].apply(clean_company)


def normalize_subfields():
    """
    Normalizes the subfield column in it_jobs_analysis table using the shared mappings.
    Also splits comma-separated 'language' and 'technologies' into multiple rows if needed,
    or just ensures consistent formatting.
    Also normalizes company names.
    """

    logger.info("Fetching current subfields and titles...")
    query = "SELECT id, job_title, subfield, language, technologies, company FROM it_jobs_analysis"
    df = pd.read_sql(query, engine)

    if df.empty:
        logger.warning("No data found in database.")
        return

    logger.info(f"Loaded {len(df)} records.")

    # Apply Logic from mappings.py
    df["new_subfield"] = df.apply(
        lambda row: get_normalized_subfield(row["job_title"], row["subfield"]), axis=1
    )

    # Normalize Companies
    df["new_company"] = normalize_companies(df)

    # Logic to merge language and technologies
    def merge_techs(row):
        langs = str(row["language"]).split(",") if row["language"] else []
        techs = str(row["technologies"]).split(",") if row["technologies"] else []

        # Clean and strip
        combined = set(
            [l.strip() for l in langs if l and l.strip().lower() != "none"]
            + [t.strip() for t in techs if t and t.strip().lower() != "none"]
        )

        if not combined:
            return None
        return ", ".join(sorted(list(combined)))

    df["merged_technologies"] = df.apply(merge_techs, axis=1)

    logger.info("Preparing to update database...")

    # Calculate changes stats
    subfield_changes = df[df["subfield"] != df["new_subfield"]]
    tech_changes = df[df["technologies"] != df["merged_technologies"]]
    company_changes = df[df["company"] != df["new_company"]]

    logger.info(f"Identified {len(subfield_changes)} subfields to update.")
    logger.info(f"Identified {len(tech_changes)} technologies to update.")
    logger.info(f"Identified {len(company_changes)} companies to update.")

    if subfield_changes.empty and tech_changes.empty and company_changes.empty:
        logger.info("No changes needed.")
        return

    # Prepare update payload
    mask = (
        (df["subfield"] != df["new_subfield"])
        | (df["technologies"] != df["merged_technologies"])
        | (df["company"] != df["new_company"])
    )
    changes_df = df[mask].copy()

    if changes_df.empty:
        logger.info("No changes needed after all.")
        return

    # Create DataFrame for updates
    updates_df = changes_df[
        ["id", "new_subfield", "merged_technologies", "new_company"]
    ].copy()

    # Rename columns to match DB schema
    updates_df.rename(
        columns={
            "new_subfield": "subfield",
            "merged_technologies": "technologies",
            "new_company": "company",
        },
        inplace=True,
    )

    logger.info("Sample updates:")
    print(updates_df.head(5))

    with engine.begin() as conn:
        # Create temp table
        conn.execute(
            text(
                "CREATE TEMP TABLE batch_updates (id UUID, subfield VARCHAR, technologies VARCHAR, company VARCHAR)"
            )
        )

        updates_df.to_sql("batch_updates", conn, if_exists="append", index=False)

        update_query = """
        UPDATE it_jobs_analysis
        SET subfield = batch_updates.subfield,
            technologies = batch_updates.technologies,
            company = batch_updates.company
        FROM batch_updates
        WHERE it_jobs_analysis.id = batch_updates.id
        """
        conn.execute(text(update_query))
        logger.info("Database updated successfully.")

        conn.execute(text("DROP TABLE batch_updates"))


if __name__ == "__main__":
    normalize_subfields()

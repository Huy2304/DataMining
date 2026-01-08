import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sqlalchemy import create_engine
import sys
import os

# robustly find data/job/mappings.py
possible_paths = [
    "../job",  # If running from data/stackoverflow
    "data/job",  # If running from repo root
    "../../data/job",  # Fallback
]

mappings_found = False
for path in possible_paths:
    abs_path = os.path.abspath(path)
    if os.path.exists(os.path.join(abs_path, "mappings.py")):
        sys.path.append(abs_path)
        print(f"Added {abs_path} to sys.path")
        mappings_found = True
        break

try:
    from mappings import PROGRAMMING_LANGUAGES_MAP

    print("✅ Mappings imported successfully.")
except ImportError:
    print(
        "❌ Error: Could not import mappings.py. Please check your directory structure."
    )

# Database Connection
# DB_URI = "postgresql://user:password@localhost:5432/it_jobs_db"
# engine = create_engine(DB_URI)

print("Script completed successfully")


import pandas as pd
import os

# Define paths
so_gpt_path = 'data/outputs/dataset_STACKOVERFLOW_gpt.csv'
gh_path = 'data/outputs/dataset_github_gpt.csv'
so_18_19_path = 'data/outputs/stackoverflow_label_18-19.csv'
so_20_22_path = 'data/outputs/stackoverflow_label_2020-2022.csv'
job_path = 'data/outputs/dataset_job_lable_double_check.csv'

output_path = 'data/outputs/merged_supply_data.csv'

# Helper function to load and standardize
def load_and_standardize(path, mapping=None, source_type_override=None):
    if not os.path.exists(path):
        print(f"Warning: {path} not found. Skipping.")
        return None
    
    try:
        df = pd.read_csv(path)
        
        # Rename columns based on mapping if provided
        if mapping:
            df = df.rename(columns=mapping)
        
        # Override source_type if needed
        if source_type_override:
            df['source_type'] = source_type_override
        
        # Ensure label_gpt exists
        # In case some datasets use 'label', rename it
        if 'label' in df.columns and 'label_gpt' not in df.columns:
             df = df.rename(columns={'label': 'label_gpt'})

        # Keep only analysis columns
        cols_to_keep = ['source_type', 'language', 'event_date', 'label_gpt']
        
        # Filter columns that exist
        available_cols = [c for c in cols_to_keep if c in df.columns]
        df = df[available_cols]
        
        return df
    except Exception as e:
        print(f"Error processing {path}: {e}")
        return None

dfs = []

# Mappings (original_col -> target_col)
# 1. SO GPT (assuming it has tech_keywords)
df_so_gpt = load_and_standardize(so_gpt_path, mapping={'tech_keywords': 'language'})
if df_so_gpt is not None: dfs.append(df_so_gpt)

# 2. GitHub GPT (tech_keywords -> language)
# AND User explicitly requested to normalize date to year for github
df_gh = load_and_standardize(gh_path, mapping={'tech_keywords': 'language'})
if df_gh is not None:
    # Normalize date specifically for GitHub here (or do it globally later, but doing it here is safe)
    # Extract first 4 chars
    df_gh['event_date'] = df_gh['event_date'].astype(str).str[:4]
    dfs.append(df_gh)

# 3. SO 18-19 (User asked: if it has tech_keywords, filter it to language)
# It has 'tech_keywords', so we map it.
df_so_18 = load_and_standardize(so_18_19_path, mapping={'tech_keywords': 'language'})
if df_so_18 is not None: dfs.append(df_so_18)

# 4. SO 20-22
df_so_20 = load_and_standardize(so_20_22_path, mapping={'tech_keywords': 'language'}) # Just in case, though header check might be needed or we assume consistent naming
if df_so_20 is not None: dfs.append(df_so_20)

# 5. Job Data
df_job = load_and_standardize(job_path, mapping={'tech_keywords': 'language'}, source_type_override='job')
if df_job is not None: dfs.append(df_job)

if not dfs:
    print("No data loaded.")
else:
    # Concatenate
    df_supply = pd.concat(dfs, ignore_index=True)

    # Clean strings and convert to lowercase
    # Fill NaNs with empty string to avoid errors during string methods
    df_supply['language'] = df_supply['language'].fillna('').astype(str).str.strip().str.lower()
    df_supply['label_gpt'] = df_supply['label_gpt'].fillna('').astype(str).str.strip().str.lower()
    df_supply['source_type'] = df_supply['source_type'].fillna('').astype(str).str.strip().str.lower()

    
    # Normalize Source Types (optional, but good for consistency)
    # e.g. 'stackoverflow_question' -> 'stackoverflow'
    df_supply.loc[df_supply['source_type'].str.contains('stackoverflow'), 'source_type'] = 'stackoverflow'
    df_supply.loc[df_supply['source_type'].str.contains('github'), 'source_type'] = 'github'

    # Normalize specific labels
    df_supply['label_gpt'] = df_supply['label_gpt'].replace({
        'networking': 'network',
        'frontend': 'web frontend', # just in case
        'backend': 'web backend'
    })

    # Standardize event_date to year only - GLOBAL ENFORCEMENT
    # This ensures even if datasets were missed above, they are fixed here.
    df_supply['event_date'] = df_supply['event_date'].astype(str).str[:4]
    
    # Explode languages (comma separated) to handle multiple tags per row
    df_supply = df_supply.assign(language=df_supply['language'].str.split(',')).explode('language')
    df_supply['language'] = df_supply['language'].str.strip()

    # Remove empty languages
    df_supply = df_supply[df_supply['language'] != '']
    df_supply = df_supply[df_supply['language'] != 'nan']

    # Save
    df_supply.to_csv(output_path, index=False)
    print(f"Successfully merged {len(dfs)} datasets into {output_path} with {len(df_supply)} rows.")
    print("Source types found:", df_supply['source_type'].unique())
    print("Years found:", df_supply['event_date'].unique())

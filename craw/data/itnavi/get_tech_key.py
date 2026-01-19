import sys
import os
import json
sys.path.append('craw')
from tech_domain_extract import extract_raw_keys, save_raw_to_key_map

def process_itnavi_jobs():
    with open(os.path.join(os.path.dirname(__file__), 'itnavi_jobs.json'), 'r', encoding='utf-8') as f:
        jobs = json.load(f)
    for job in jobs:
        job_details = job['job_details']
        data = extract_raw_keys(job_details)
        save_raw_to_key_map(data)

if __name__ == "__main__":
    process_itnavi_jobs()

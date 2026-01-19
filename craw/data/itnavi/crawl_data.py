import json
import requests
from bs4 import BeautifulSoup
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

def get_job_ids_from_page(page):
    url = f"https://itnavi.com.vn/job?page={page}"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    job_items = soup.find_all('div', class_='jsl_item')
    ids = [item['data-id'] for item in job_items if 'data-id' in item.attrs]
    return ids

def get_job_detail(job_id):
    url = f"https://itnavi.com.vn/ajax/get-job-by-id/{job_id}"
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            result = response.json()
            data = result.get('data', {})
            job_name = data.get('job_name', '')
            job_published_date = data.get('job_published_at_show', '')
            job_content = data.get('job_content', '')
            soup = BeautifulSoup(job_content, 'html.parser')
            job_details = soup.get_text(separator='\n').strip()
            return {
                "job_name": job_name,
                "job_published_date": job_published_date,
                "job_details": job_details
            }
    except Exception as e:
        print(f"Failed to get detail for job {job_id}: {e}")
    return None

def crawl_itnavi_jobs():
    all_jobs = []
    with ThreadPoolExecutor(max_workers=5) as executor:
        for page in range(1, 59):  # Pages 1 to 58
            print(f"Processing page {page}")
            job_ids = get_job_ids_from_page(page)
            futures = [executor.submit(get_job_detail, job_id) for job_id in job_ids]
            for future in as_completed(futures):
                detail = future.result()
                if detail:
                    all_jobs.append(detail)
                time.sleep(0.1)  # Small delay between completions

    # Save to JSON
    with open("craw\\data\\itnavi\\itnavi_jobs.json", "w", encoding="utf-8") as f:
        json.dump(all_jobs, f, ensure_ascii=False, indent=4)

    print(f"Crawled {len(all_jobs)} jobs")

if __name__ == "__main__":
    crawl_itnavi_jobs()

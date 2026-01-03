import requests
import json
import csv
import time
import random
from datetime import datetime
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

session = requests.Session()
retries = Retry(total=5, backoff_factor=2, status_forcelist=[500, 502, 503, 504, 429])
session.mount('https://', HTTPAdapter(max_retries=retries))

api_url = "https://careerviet.vn/search-jobs"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 Edg/131.0.0.0",
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "Accept-Language": "vi-VN,vi;q=0.9",
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    "X-Requested-With": "XMLHttpRequest",

}

all_jobs = []
page = 0  # API bắt đầu từ page 0
max_pages = 500  # Thay đổi để lấy hết, test thì giảm xuống

print("Bắt đầu crawl việc làm CNTT từ CareerViet qua API...")

while (page < 10):
    # Payload PHP serialized
    if page == 0:
        payload = 'a:1:{s:8:"INDUSTRY";s:4:"63,1";}'
    else:
        payload = f'a:2:{{s:8:"INDUSTRY";s:4:"63,1";s:4:"PAGE";i:{page};}}'

    print(f"\nĐang lấy trang {page + 1} (PAGE={page})")

    try:
        response = session.post(api_url, data=payload, headers=headers, timeout=60)
        response.raise_for_status()
        data = response.json()
    except Exception as e:
        print(f"Lỗi request trang {page + 1}: {e}")
        time.sleep(10)
        continue

    jobs = data.get("data", [])
    if not jobs:
        print("Không còn job → dừng.")
        break

    print(f"Trang {page + 1}: {len(jobs)} việc làm")
    all_jobs.extend(jobs)

    page += 1
    if page >= max_pages:
        print(f"Đạt giới hạn {max_pages} trang.")
        break

    sleep_time = random.uniform(3, 6)
    print(f"Nghỉ {sleep_time:.1f}s...")
    time.sleep(sleep_time)

print(f"\n=== HOÀN TẤT ===\nTổng: {len(all_jobs)} việc làm")

timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
json_file = f"careerviet_it_jobs_full_{timestamp}.json"
with open(json_file, "w", encoding="utf-8") as f:
    json.dump(all_jobs, f, ensure_ascii=False, indent=2)
print(f"Lưu JSON: {json_file}")

csv_file = f"careerviet_it_jobs_full_{timestamp}.csv"
with open(csv_file, "w", encoding="utf-8-sig", newline="") as f:
    if all_jobs:
        fieldnames = all_jobs[0].keys()
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for job in all_jobs:
            row = job.copy()
            for key in ["LOCATION_NAME_ARR", "BENEFIT_NAME", "BENEFIT_ICON", "TOP_INDUSTRY", "PREMIUM_INDUSTRY"]:
                if key in row and isinstance(row[key], list):
                    row[key] = " | ".join(map(str, row[key]))
            writer.writerow(row)
print(f"Lưu CSV: {csv_file}")
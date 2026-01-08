CREATE EXTENSION IF NOT EXISTS "pgcrypto";

CREATE TABLE IF NOT EXISTS it_jobs_analysis (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    job_title TEXT,
    company VARCHAR(255),
    date_posted DATE,
    subfield VARCHAR(100),
    language VARCHAR(500),
    technologies TEXT,
    source VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_it_jobs_subfield ON it_jobs_analysis(subfield);
CREATE INDEX IF NOT EXISTS idx_it_jobs_date_posted ON it_jobs_analysis(date_posted);

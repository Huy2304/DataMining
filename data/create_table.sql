CREATE EXTENSION IF NOT EXISTS "pgcrypto";

CREATE TABLE IF NOT EXISTS tech_meta (
    tech_name TEXT PRIMARY KEY,          -- 'java,spring boot'
    category TEXT,                       -- 'language', 'framework', 'database', 'tool'
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS it_jobs_analysis (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    job_title TEXT,
    company TEXT,
    language TEXT,
    technologies TEXT,
    date_posted DATE,
    subfield TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS job_tech_bridge (
    job_id UUID REFERENCES it_jobs_analysis(id) ON DELETE CASCADE,
    tech_name TEXT REFERENCES tech_meta(tech_name) ON DELETE CASCADE,
    PRIMARY KEY (job_id, tech_name)
);

CREATE TABLE IF NOT EXISTS stackoverflow_posts (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    so_id BIGINT UNIQUE,                 
    title TEXT,
    view_count INT DEFAULT 0,
    answer_count INT DEFAULT 0,
    score INT DEFAULT 0,
    date_posted DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS stackoverflow_tech_bridge (
    post_id UUID REFERENCES stackoverflow_posts(id) ON DELETE CASCADE,
    tech_name TEXT REFERENCES tech_meta(tech_name) ON DELETE CASCADE,
    PRIMARY KEY (post_id, tech_name)
);



CREATE INDEX IF NOT EXISTS idx_jobs_date ON it_jobs_analysis(date_posted);
CREATE INDEX IF NOT EXISTS idx_jobs_subfield ON it_jobs_analysis(subfield);
CREATE INDEX IF NOT EXISTS idx_so_date ON stackoverflow_posts(date_posted);

CREATE INDEX IF NOT EXISTS idx_job_bridge_tech ON job_tech_bridge(tech_name);
CREATE INDEX IF NOT EXISTS idx_so_bridge_tech ON stackoverflow_tech_bridge(tech_name);

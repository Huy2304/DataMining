CREATE EXTENSION IF NOT EXISTS "pgcrypto";




create table if not EXISTS tech_meta (
    tech_name TEXT primary, -- <java><spring-boot><spring-test><mapstruct>
)

create table if not EXISTS stackoverflow_tech_meta (
    tech_name text,
    stackoverflow_id INT,
)

CREATE TABLE IF NOT EXISTS stackoverflow (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    date_posted DATE,
    view
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_it_jobs_subfield ON it_jobs_analysis(subfield);
CREATE INDEX IF NOT EXISTS idx_it_jobs_date_posted ON it_jobs_analysis(date_posted);

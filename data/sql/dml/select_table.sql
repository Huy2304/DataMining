WITH common_tech AS (
    SELECT DISTINCT LOWER(jtb.tech_name) AS lower_tech
    FROM JOB_TECH_BRIDGE jtb
),
job_tech AS (
    SELECT *
    FROM JOB_TECH_BRIDGE jtb
    INNER JOIN IT_JOBS_ANALYSIS ja
        ON jtb.job_id = ja.id
    WHERE LOWER(jtb.tech_name) IN (SELECT lower_tech FROM common_tech)
),
github_filtered AS (
    SELECT *
    FROM GITHUB_REPO_TECH_BRIDGE gtb
    WHERE LOWER(gtb.tech_name) IN (SELECT lower_tech FROM common_tech)
)
SELECT
	jt.job_id,
	jt.tech_name,
	grm.*
FROM job_tech jt
INNER JOIN github_filtered gf
    ON LOWER(jt.tech_name) = LOWER(gf.tech_name)
INNER JOIN GITHUB_REPO_META grm
	ON grm.repo_meta_id = gf.repo_meta_id;

-- Tech trong từng ngành
SELECT
    ij.subfield,
    ARRAY_AGG(DISTINCT jtb.tech_name ORDER BY jtb.tech_name) AS tech_list,
    COUNT(DISTINCT jtb.job_id) AS job_count,
    COUNT(DISTINCT jtb.tech_name) AS unique_tech_count
FROM it_jobs_analysis ij
INNER JOIN job_tech_bridge jtb
    ON ij.id = jtb.job_id
GROUP BY ij.subfield
ORDER BY job_count DESC, subfield;

-- Tech trong từng ngành
SELECT
    ij.subfield,
    STRING_AGG(DISTINCT jtb.tech_name, ', ') AS technologies,  -- gom tech thành chuỗi
    COUNT(DISTINCT jtb.tech_name) AS tech_count               -- số lượng tech khác nhau
FROM it_jobs_analysis ij
INNER JOIN job_tech_bridge jtb
    ON ij.id = jtb.job_id
GROUP BY ij.subfield
ORDER BY ij.subfield;

-- Số lượng job sử dụng tech trong subfield
SELECT
	ij.subfield,
	jtb.tech_name,
COUNT(*) AS job_count  -- Số lượng job sử dụng tech này trong subfield
FROM it_jobs_analysis ij
INNER JOIN job_tech_bridge jtb
	ON ij.id = jtb.job_id
GROUP BY ij.subfield, jtb.tech_name
ORDER BY ij.subfield, job_count DESC;

-- TOP 1 subfield theo số lượng job
SELECT
    ij.subfield,
    COUNT(DISTINCT ij.id) AS job_count
FROM it_jobs_analysis ij
WHERE ij.subfield IS NOT NULL
GROUP BY ij.subfield
ORDER BY job_count DESC
LIMIT 1;

-- TOP 1 ngôn ngữ theo từng subfield
WITH ranked_tech AS (
    SELECT
        ij.subfield,
        jtb.tech_name,
        COUNT(*) AS job_count,
        ROW_NUMBER() OVER (
            PARTITION BY ij.subfield
            ORDER BY COUNT(*) DESC, jtb.tech_name
        ) AS rank
    FROM it_jobs_analysis ij
    INNER JOIN job_tech_bridge jtb
        ON ij.id = jtb.job_id
    WHERE ij.subfield IS NOT NULL
      AND jtb.tech_name IS NOT NULL
      AND ij.subfield != ''
    GROUP BY ij.subfield, jtb.tech_name
)
SELECT
    subfield,
    tech_name AS top_tech,
    job_count AS number_of_jobs
FROM ranked_tech
WHERE rank = 1
ORDER BY job_count DESC, subfield;

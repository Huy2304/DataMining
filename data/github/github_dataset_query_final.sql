-- Query to generate GitHub dataset with all required columns
-- This query joins all GitHub-related tables to create a comprehensive dataset
-- Run this query in pgAdmin to view the results

WITH repo_languages AS (
    SELECT
        repo_id,
        STRING_AGG(prlang_name, ', ') AS tech_stack,
        COUNT(*) AS total_languages,
        (SELECT prlang_name
         FROM github_repo_prlangs grl2
         WHERE grl2.repo_id = grl.repo_id
         ORDER BY prlang_byte_count DESC
         LIMIT 1) AS primary_language
    FROM github_repo_prlangs grl
    GROUP BY repo_id
),

repo_topics AS (
    SELECT
        repo_id,
        STRING_AGG(topic_name, ', ') AS topics,
        COUNT(*) AS topics_count
    FROM github_repo_topics
    GROUP BY repo_id
),

repo_commits_stats AS (
    SELECT
        repo_id,
        COUNT(*) AS commits_count,
        MAX(commit_author_date) AS last_commit_date
    FROM github_repo_commits
    GROUP BY repo_id
),

repo_tech_bridge AS (
    SELECT
        repo_meta_id,
        STRING_AGG(tech_name, ', ') AS tech_stack_from_bridge,
        COUNT(*) AS tech_count_from_bridge
    FROM github_repo_tech_bridge
    GROUP BY repo_meta_id
)

SELECT
    -- Basic repository information
    grm.repo_id AS Repo_ID,
    grm.repo_id::text AS Repo_Name,
    grm.repo_created_at AS Repo_Created_At,
    grm.repo_updated_at AS Repo_Updated_At,
    grm.repo_pushed_at AS Repo_Pushed_At,
    grm.repo_size_count AS Repo_Size_KB,
    grm.repo_stars_count AS Stars_Count,
    grm.repo_watchers_count AS Watchers_Count,
    grm.repo_forks_count AS Forks_Count,
    grm.repo_open_issues_count AS Open_Issues_Count,

    -- Language information
    rl.primary_language AS Primary_Language,
    rl.total_languages AS Total_Languages,
    rl.tech_stack AS Tech_Stack,

    -- Technology information from bridge table
    rtb.tech_stack_from_bridge,
    rtb.tech_count_from_bridge AS Tech_Count,

    -- License information
    grm.repo_license AS License_Type,
    CASE WHEN grm.repo_license IS NOT NULL THEN TRUE ELSE FALSE END AS Has_License,

    -- Topics information
    rt.topics AS Topics,
    rt.topics_count AS Topics_Count,

    -- Commit information
    rcs.commits_count AS Commits_Count,
    rcs.last_commit_date AS Last_Commit_Date,

    -- Additional information
    grm.repo_default_branch AS Default_Branch,

    -- Calculated fields
    -- Calculate repo age in days (assuming repo_created_at is in ISO format)
    CASE
        WHEN grm.repo_created_at IS NOT NULL THEN
            EXTRACT(DAY FROM (NOW() - grm.repo_created_at::timestamp))
        ELSE NULL
    END AS Repo_Age_Days,

    -- Popularity score (weighted sum of stars, forks, watchers)
    (grm.repo_stars_count * 1.0 + grm.repo_forks_count * 0.5 + grm.repo_watchers_count * 0.3) AS Popularity_Score

FROM github_repo_meta grm
INNER JOIN repo_languages rl ON grm.repo_id = rl.repo_id
INNER JOIN repo_topics rt ON grm.repo_id = rt.repo_id
INNER JOIN repo_commits_stats rcs ON grm.repo_id = rcs.repo_id
INNER JOIN repo_tech_bridge rtb ON grm.repo_meta_id = rtb.repo_meta_id

WHERE grm.repo_id IS NOT NULL
  AND grm.repo_created_at IS NOT NULL
  AND grm.repo_stars_count IS NOT NULL
  AND grm.repo_forks_count IS NOT NULL
  AND grm.repo_watchers_count IS NOT NULL
  AND rl.primary_language IS NOT NULL
  AND rl.total_languages IS NOT NULL
  AND rtb.tech_count_from_bridge IS NOT NULL
  AND grm.repo_license IS NOT NULL
  AND rt.topics_count IS NOT NULL
  AND rcs.commits_count IS NOT NULL
  AND rcs.last_commit_date IS NOT NULL

ORDER BY grm.repo_stars_count DESC, grm.repo_forks_count DESC;

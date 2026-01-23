# Pipeline: IT Subfield Classification + Tech Trend (StackOverflow)

This pipeline builds a classifier to map text to IT job **subfields**, then uses the trained model to label StackOverflow posts and analyze **technology trends** over time.

Key constraints:
- No crawling or new scraping steps (use existing Postgres tables + bridge tables).
- The label `Software Engineer (General)` is deprecated and must **not** appear in training labels or predictions.

---

## Overview

We maintain two different text fields:

- **`text` (classification input):** `title + tags`  
  Used for the ML model (better accuracy because titles contain intent words like “DevOps”, “QA”, “Data Engineer”…)

- **`features` (trend input):** `tags-only`  
  Used to compute market share of technologies; avoids noise from title words.

---

## Notebooks (run in order)

All notebooks are in `DataMining/pipeline_notebooks/`.

### 01 — Extract from DB
**Notebook:** `DataMining/pipeline_notebooks/01_extract_from_db.ipynb`

**What it does**
- Extracts training data (job postings) + inference data (StackOverflow posts) from Postgres.
- Builds:
  - `features` from bridge tables (`tech_name` aggregation)
  - `text = title + features`

**Outputs**
- `DataMining/outputs/job_train_raw.csv`
  - Columns (typical): `job_id`, `label_raw`, `job_title`, `date_posted`, `features`, `text`
  - Meaning: raw training dataset before cleaning/relabeling.

- `DataMining/outputs/so_infer_raw.csv`
  - Columns (typical): `post_id`, `so_id`, `title`, `date_posted`, `features`, `text`
  - Meaning: inference dataset for StackOverflow posts to be classified.

**How to interpret**
- `label_raw` is whatever label exists in DB (may include `Other` and `Software Engineer (General)`).
- `features` is a whitespace-separated list of technologies.

---

### 02 — Relabel Other + Remove “General” (LLM or Rule-Based)
**Notebook:** `DataMining/pipeline_notebooks/02_relabel_llm.ipynb` (Recommended) OR `DataMining/pipeline_notebooks/02_relabel_other.ipynb` (Legacy)

**What it does (LLM Version)**
- Uses Gemini API to classify job postings.
- Focuses on relabeling `Other` and `Software Engineer (General)` to specific subfields.
- Can be configured to relabel all rows for higher accuracy.

**What it does (Rule-Based Version)**
- Uses rule-based keyword matching from `DataMining/data/job/mappings.py`.
- Fast but less accurate for complex titles.

**Outputs**
- `DataMining/outputs/job_train_labeled.csv`
  - Columns: `label_final`, `label_rule` (if available)
  - Meaning: cleaned training dataset for the benchmark step.

**How to interpret**
- Ensure `Software Engineer (General)` is eliminated.
- LLM labels are generally more accurate for ambiguous titles.

---

### 03 — Model Benchmark
**Notebook:** `DataMining/pipeline_notebooks/03_model_benchmark.ipynb`

**What it does**
- Benchmarks multiple TF-IDF configurations and classifiers on the same split.
- Uses **macro-F1** as the primary metric (better for imbalanced classes).

**Train filter**
- Excludes `label_final == 'Other_Unknown'`
- Excludes `label_final == 'Software Engineer (General)'` (extra guard)

**Outputs**
- `DataMining/outputs/benchmark_results.csv`
  - Each row = one (vectorizer, model) combo with metrics:
    - `accuracy`, `macro_f1`, `weighted_f1`, `train_seconds`
  - Meaning: comparison table for selecting the best model.

- `DataMining/outputs/best_config.json`
  - Contains the chosen configuration (best macro-F1).
  - Meaning: single source of truth for training the final model.

**How to interpret**
- Prefer the config with best `macro_f1`.
- `weighted_f1` often looks higher due to majority classes.

---

### 04 — Train Best Model + Serialize
**Notebook:** `DataMining/pipeline_notebooks/04_train_and_serialize.ipynb`

**What it does**
- Trains the best model from `best_config.json` on the full (filtered) labeled dataset.
- Saves a serialized sklearn `Pipeline`.

**Outputs**
- `models/text_subfield_pipeline.joblib`
  - The complete model pipeline (TF-IDF + classifier).
  - Meaning: the artifact used later for prediction.

- `models/label_list.json`
  - List of labels seen during training.
  - Meaning: sanity check for label leakage (ensure no “general”).

**How to interpret**
- If `label_list.json` contains `Software Engineer (General)`, retraining is wrong (should be removed).

---

### 05 — Evaluation
**Notebook:** `DataMining/pipeline_notebooks/05_evaluation.ipynb`

**What it does**
- Loads the serialized pipeline and evaluates it on a fixed stratified split.
- Produces detailed diagnostics (report + confusion breakdown).

**Outputs**
- `DataMining/outputs/eval_metrics.json`
  - Overall metrics (accuracy, macro_f1, weighted_f1).
  - Meaning: headline performance numbers.

- `DataMining/outputs/classification_report.csv`
  - Per-class precision/recall/F1 (+ support).
  - Meaning: shows which subfields are weak/strong.

- `DataMining/outputs/confusion_matrix.csv`
  - Confusion matrix table.
  - Meaning: which labels get mixed up.

- `DataMining/outputs/top_confusions.csv`
  - Top confusing pairs (true_label → predicted_label + counts).
  - Meaning: fastest way to find failure modes.

- `DataMining/outputs/confusion_examples.csv`
  - Example rows of confusing cases (text + true/pred).
  - Meaning: qualitative inspection to improve rules/labels.

---

### 06 — Predict StackOverflow + Trend Analysis
**Notebook:** `DataMining/pipeline_notebooks/06_build_predictions_and_trend.ipynb`

**What it does**
1) Loads StackOverflow inference dataset and predicts subfield using the trained model.
2) Computes tech trend market share using tags-only.

**Outputs**
- `DataMining/predictions.csv`
  - Columns: `date_posted, features, text, predicted_subfield`
  - Meaning:
    - `predicted_subfield` = model’s prediction per StackOverflow post
    - `text` is what the model used to decide
    - `features` is what you later explode for trends

- `DataMining/outputs/market_share_monthly.csv`
  - Columns: `month, tags, count, total, share`
  - Meaning:
    - For each month, each tag’s frequency and market share
    - `share = count / total` where total counts all tags occurrences in that month

**Hard guard (required)**
- If predictions ever produce `Software Engineer (General)`, it is mapped to `Other_Unknown`.
  This protects you from accidentally using an old model artifact.

---

## Run Order

Run notebooks in this exact order:

1. `01_extract_from_db.ipynb`
2. `02_relabel_llm.ipynb` (or `02_relabel_other.ipynb`)
3. `03_model_benchmark.ipynb`
4. `04_train_and_serialize.ipynb`
5. `05_evaluation.ipynb`
6. `06_build_predictions_and_trend.ipynb`

---

## Validation Checklist (must pass)

- `DataMining/outputs/job_train_labeled.csv` has **0** rows where `label_final == 'Software Engineer (General)'`.
- `models/label_list.json` does **not** contain `Software Engineer (General)`.
- `DataMining/predictions.csv` has **0** rows where `predicted_subfield == 'Software Engineer (General)'`.

---

## Practical Notes

- If too many rows become `Other_Unknown`, expand keyword lists in `DataMining/data/job/mappings.py`.
- For 5.5M StackOverflow posts, prediction may take time and memory; consider chunked processing if needed.
- Trend analysis intentionally uses tags-only (`features`) to avoid title-word noise.

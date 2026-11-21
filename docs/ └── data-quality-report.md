# Data Quality Report

## 1. Overview

This report documents the initial data quality assessment of the three public Steam datasets used in GamePulse Analytics.

The assessment covers dataset structure, missing values, duplicate records, relationships between datasets, and the coverage of CCU data.

### Dataset Summary

| Dataset | Records | Columns |
|---|---:|---:|
| games-index.csv | 85,041 | 8 |
| ccu-daily-top2000.csv | 193,981 | 3 |
| health-tiers.csv | 85,020 | 4 |

## 2. Missing Value Assessment

### 2.1 games-index.csv

| Column | Missing Records |
|---|---:|
| app_id | 0 |
| name | 0 |
| slug | 0 |
| release_date | 100 |
| is_free | 0 |
| total_positive | 0 |
| total_negative | 0 |
| health_tier | 21 |

### 2.2 ccu-daily-top2000.csv

No missing values were found in the three columns: `app_id`, `date`, and `max_players`.

### 2.3 health-tiers.csv

| Column | Missing Records |
|---|---:|
| app_id | 0 |
| slug | 0 |
| tier | 0 |
| current_players | 82,123 |

The `current_players` field has a missing rate of approximately 96.59%.

## 3. Duplicate Record Assessment

No duplicate `app_id` values were found in `games-index.csv` or `health-tiers.csv`.

For CCU data, `(app_id, date)` was used as the composite key because each game can have multiple daily records.

No duplicate composite keys were found.

## 4. Dataset Relationship Assessment

The relationship between `games-index.csv` and `health-tiers.csv` was checked using `app_id`.

| Metric | Records |
|---|---:|
| Games index IDs | 85,041 |
| Health tiers IDs | 85,020 |
| Matched IDs | 85,020 |
| Only in games-index | 21 |
| Only in health-tiers | 0 |

The 21 records missing from `health-tiers.csv` exactly match the 21 records with missing `health_tier` values in `games-index.csv`.

This indicates that `health-tiers.csv` covers a subset of the games in `games-index.csv`.

## 5. CCU Data Coverage

| Metric | Result |
|---|---|
| Earliest date | 2026-08-06 |
| Latest date | 2026-11-15 |
| Invalid date records | 0 |
| Duplicate composite keys | 0 |

The CCU dataset contains daily maximum concurrent player counts for sampled games.

It should not be interpreted as a complete historical record of all Steam games, nor should CCU be treated as DAU.

## 6. Missing Value Investigation

### 6.1 current_players

Missing values were investigated by `tier`.

| Tier | Total | Missing | Present | Missing Rate |
|---|---:|---:|---:|---:|
| cooling | 975 | 891 | 84 | 91.38% |
| dormant | 664 | 655 | 9 | 98.64% |
| healthy | 3,371 | 2,488 | 883 | 73.81% |
| quiet | 67,273 | 65,593 | 1,680 | 97.50% |
| thriving | 98 | 0 | 98 | 0.00% |
| unknown | 12,639 | 12,496 | 143 | 98.87% |

Missing values are distributed unevenly across tiers. The thriving group has no missing values, while quiet, dormant, and unknown have particularly high missing rates.

The relationship is descriptive and does not establish causation.

### 6.2 release_date

A total of 100 missing release dates were found.

Distribution by health tier:

| Tier | Records |
|---|---:|
| cooling | 2 |
| dormant | 1 |
| healthy | 2 |
| quiet | 33 |
| unknown | 62 |

Distribution by free status:

| is_free | Records |
|---|---:|
| false | 74 |
| true | 26 |

Only 3 of these 100 games were found in the CCU dataset. The remaining 97 were not covered by the sampled CCU records.

Absence from the CCU dataset does not imply zero players.

## 7. Data Processing Recommendations

Based on the assessment, the following processing rules are recommended:

1. Preserve the original CSV files without modification.
2. Convert empty strings into proper missing values during processing.
3. Keep missing `release_date` values as missing rather than inventing dates.
4. Keep missing `current_players` values as missing rather than replacing them with zero.
5. Preserve the 21 games without health-tier records and handle missing tier information explicitly when joining datasets.
6. Convert date and numeric fields to appropriate data types.
7. Document the CCU sampling scope and observation period in subsequent analysis.

## 8. Conclusion

The three datasets passed the initial checks for duplicate identifiers, duplicate CCU composite keys, and date format validity.

Several missing-value patterns were identified and investigated. These findings will guide the subsequent data preprocessing stage.

The raw datasets will remain unchanged. Processed datasets will be generated separately to ensure reproducibility and traceability.
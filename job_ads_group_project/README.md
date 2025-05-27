# 📊 Job Ads Group Project - dbt

### 🔍 Overview
This dbt project models and transforms job advertisement data from raw sources into a clean, analytical structure.

The data is sourced from the Arbetsförmedlingen via a DLT pipeline and processed through multiple dbt layers: `staging`, `dim`, `fct`, and `mart`.

## 🧱 Project structure

### Sources
All data is loaded from the `staging` schema using the following sources:

- `job_ads` (main raw table)
- `job_ads__driving_license`
- `job_ads__must_have__skills`

### 🛠️ Staging Layer (`src_*`)
Raw data extracted via DLT, lightly cleaned and renamed

Examples:
- `src_job_ads`
- `src_employer`
- `src_occupation`

### 🧮 Refined Layer (`dim_*`, `fct_*`)
Dimensional and fact tables created from the staging data, prepared for analysis.

Examples:
- `dim_job_ads`: Contains job ad details with cleaned and standardized fields.
- `dim_employer`: Contains employer information, linked to job ads.
- `fct_job_ads`: Fact table aggregating job ad data, including counts and metrics.

### 📈 Mart Layer (`mart_*`)
Business-specific and dashboard-ready views used by the Streamlit frontend.

- `mart_full_job_ads`: Full dataset with no filters.
- `mart_hotel_restaurant`: Jobs in *Hotel, restaurant, catering*.
- `mart_installation_maintenance`: Jobs in *Installation, operation, maintenance*.
- `mart_transport_distribution`: Jobs in *Transport, distribution, warehouse*.

## ✅ Testing
We use both built-in dbt tests and custom macros:

### 🔹 Standard tests:
- `unique`
- `not_null`
- `accepted_values`

### 🔸 Custom tests:
- `dim_row_count_match`: Ensures that the number of distinct keys in the fact table matches the row count of the dimension table.
- `mart_row_count_match`: Verifies that mart models contain the expected number of rows compared to their sources.


## 📝 Notes

- Surrogate keys are generated using `dbt_utils.generate_surrogate_key`.
- `coalesce()` is used to ensure no critical values are null in final models.
-  All models are documented using `.yml` files, including:
  - Model descriptions
  - Column-level metadata
  - Associated tests
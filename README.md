# RecoMart Recommendation Data Pipeline

This project implements an end-to-end data management pipeline for a
recommendation system, as part of the DM4ML Assignment-I.

## Business Objective
RecoMart is an e-commerce platform aiming to improve:
- User engagement
- Cross-selling opportunities
- Conversion rate

This pipeline ingests user interaction and product data, validates and
transforms it into features, and trains a recommendation model using
modern data engineering and MLOps practices.

## High-Level Pipeline
1. Data Ingestion (CSV + API)
2. Raw Data Storage (Data Lake)
3. Data Validation & Profiling
4. Data Preparation & EDA
5. Feature Engineering
6. Feature Store
7. Model Training & Evaluation
8. Pipeline Orchestration

## Tech Stack
- Python, Pandas
- Great Expectations (Data Validation)
- MLflow (Experiment Tracking)
- DVC (Data Versioning)
- Airflow / Prefect (Orchestration)

## Repository Structure
    DM4ML-Assignment-1/
    ├── config/ # Configuration files
    ├── data/ # Data lake (raw, validated, processed, features)
    ├── logs/ # Pipeline logs
    ├── reports/ # Assignment reports (PDF)
    ├── scripts/ # Notebooks for EDA and analysis
    ├── src/ # Source code for pipeline stages
    │ ├── ingestion/ # Data ingestion scripts
    │ ├── validation/ # Data validation logic
    │ ├── preparation/ # Data cleaning and preprocessing
    │ ├── transformation/ # Feature engineering
    │ ├── feature_store/ # Feature registry and retrieval
    │ ├── models/ # Model training and evaluation
    │ └── orchestration/ # Pipeline orchestration
    ├── mlruns/ # MLflow artifacts
    ├── demo/ # Demo and walkthrough files
    ├── dvc.yaml # Data versioning configuration
    ├── README.md
    ├── requirements.txt
    └── .gitignore

## How to Run

## Setup
    Install required libraries by running
    
    ```bash
    pip install -r requirements.txt

1. **Problem Formulation**  
   Report is available at: reports/1_problem_formulation.pdf

2. **Data Collection and Ingestion**
    Run the ingestion scripts from the project root:

    ```bash
    python -m src.ingestion.ingest_clickstream
    python -m src.ingestion.ingest_products_api

    Expected Output:
    
    ```bash
    data/raw/clickstream/YYYY/MM/DD/clickstream.csv
    data/raw/products/YYYY/MM/DD/products.json
    logs/ingestion.log

3. **Raw Data Storage**
    Raw data is stored in a date-partitioned local data lake:

    ```bash
    data/raw/

4. **Data Profiling and Validation**
    Run the validation scripts from the project root:

    ```bash
    python -m src.validation.validate_data

    Expected Output:

    ```bash
    reports/4_data_quality_report.pdf
    logs/validation.log

5. **Data Preparation and EDA**
    Run the data preparation and exploratory analysis script from the project root:

    ```bash
    python -m src.preparation.clean_and_prepare
    ```

    This step performs data cleaning, enrichment, encoding, normalization, and
    exploratory data analysis.

    **Expected Output:**

    ```bash
    data/processed/prepared_interactions.csv
    data/processed/eda/interaction_distribution.png
    data/processed/eda/top_products.png
    ```

6. **Feature Engineering and Transformation**
    Run the feature engineering script from the project root:

    ```bash
    python -m src.transformation.feature_engineering
    ```

    This step generates user-level, item-level, and user–item interaction features
    from the prepared dataset and stores them in a PostgreSQL database.

    **Expected Output:**

    ```bash
    PostgreSQL Tables:
    - user_features
    - item_features
    - user_item_features
    ```

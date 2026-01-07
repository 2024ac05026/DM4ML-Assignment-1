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
(brief tree or reference to folders)

## How to Run
1. **Problem Formulation**  
   Report is available at: reports/1_problem_formulation.pdf
   
2. **Data Collection and Ingestion**

Run the ingestion scripts from the project root:

```bash
python -m src.ingestion.ingest_clickstream
python -m src.ingestion.ingest_products_api

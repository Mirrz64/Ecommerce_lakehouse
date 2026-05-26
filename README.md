# End-to-End E-Commerce Medallion Lakehouse Architecture
A production-grade ELT data pipeline simulating an e-commerce lakehouse environment. This project demonstrates modern data engineering principles by utilizing Apache Airflow for workflow orchestration, PostgreSQL as a relational data warehouse, and dbt (Data Build Tool) to implement clean data processing separations across Medallion architecture tiers.

## 🏗️ Architecture Overview
The system processes data sequentially through a structural Medallion data design, completely managed and scheduled automatically by Airflow:

[ Python Data Generator ] 
           │
           ▼
┌────────────────────────────────────────────────────────┐
│  BRONZE TIER (Staging)                                 │
│  - Raw ingestion points & database sources             │
└──────────┬─────────────────────────────────────────────┘
           │
           ▼
┌────────────────────────────────────────────────────────┐
│  SILVER TIER (Intermediate)                            │
│  - Data cleansing, case standardization, filtering     │
└──────────┬─────────────────────────────────────────────┘
           │
           ▼
┌────────────────────────────────────────────────────────┐
│  GOLD TIER (Marts)                                     │
│  - Optimized business analytics dim/fct tables         │
└────────────────────────────────────────────────────────┘

Source Tier: A custom Python generation script introduces active operational relational rows (customers, orders) into isolated landing tables.

Bronze Tier (Staging): Direct raw replication ingestion models mapped via dbt execution layouts.

Silver Tier (Intermediate): Data cleansing layers handling text-case standardization, column casting, and business logic isolation.

Gold Tier (Marts): Production-ready analytical dimension (dim_customers) and fact (fct_orders) tables optimized for downstream reporting engines.

## 🛠️ Technology Stack
Orchestration: Apache Airflow (Dockerized LocalExecutor platform)

Data Transformations: dbt (Data Build Tool Core)

Storage Warehouse: PostgreSQL Engine

Containerization: Docker & Docker Compose network isolation

## 📂 Project Structure
├── dags/
    ├── ecommerce_etl_dag.py
│   └── ecommerce_lakehouse_dag.py     # Airflow DAG definition script
├── dbt_project/
│   ├── models/
│   │   ├── staging/                    # Bronze data tier models
│   │   ├── intermediate/               # Silver cleansing logic transformations
│   │   └── marts/                      # Gold star-schema reporting layer
│   ├── dbt_project.yml                 # dbt project configuration layout
│   └── profiles.yml                    # dbt target adapter credentials config
├── scripts/
│   └── generate_mock_data.py          # Relational operational database engine simulator
├── Dockerfile                          # Customized Airflow container expansion blueprint
└── docker-compose.yml                  # Unified platform multi-container setup map

## 🚀 Getting Started
1. Prerequisites
Ensure you have the following frameworks installed on your local system:

Docker Desktop

Git command line client

2. Environment Configuration
Clone this repository locally and navigate to the project directory:

git clone https://github.com/Mirrz64/Ecommerce_lakehouse.git
cd Ecommerce_lakehouse

Initialize your localized configuration secrets by constructing a root .env file to handle container-level credentials:

POSTGRES_USER=airflow
POSTGRES_PASSWORD=your_secure_password
POSTGRES_DB=postgres_dw
AIRFLOW_SECRET_KEY=your_session_encryption_key

3. Deploy the Infrastructure
Spin up the complete multi-container architecture background network environment using Docker Compose

docker compose up -d --build

This command initializes your PostgreSQL data warehouse layer, builds dependencies, and handles Airflow database migrations automatically.

## 🔄 Automated Orchestration Flow
The execution cycle can be monitored, tested, and triggered natively via the Airflow Webserver UI on http://localhost:8080.

The automated Airflow DAG sequentially chains the complete data lifecycle:

generate_source_data: Spawns procedural mock transactional rows into the relational system.

load_to_bronze_lakehouse: Confirms landing boundaries and structural schema availability.

transform_silver_gold_marts: Commands dbt to run through staging maps and assemble analytical analytics structures.

run_dbt_tests: Runs integrated testing rules (unique, not_null, field constraint sets) to protect warehouse integrity.
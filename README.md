# End-to-End E-Commerce Medallion Lakehouse Architecture

A production-grade ELT data pipeline simulating an e-commerce lakehouse environment. This architecture utilizes **Apache Airflow** for workflow orchestration, **PostgreSQL** as a data warehouse platform, and **dbt (Data Build Tool)** to implement clean data processing separations across Medallion tiers.

## 🏗️ Architecture Overview

- **Source Tier:** Python generation script introducing active relational data into isolated landing tables.
- **Bronze Tier (Staging):** Direct raw replication ingestion points executing safe deduplication protocols.
- **Silver Tier (Intermediate):** Data cleansing layers handling case standardization and invalid state logic isolation.
- **Gold Tier (Marts):** Business-ready analytical aggregations optimized for reporting engines and dashboard lookups.

## 🛠️ Technology Stack
- **Orchestration:** Apache Airflow 2.9.1 (LocalExecutor)
- **Data Transformations:** dbt (Data Build Tool)
- **Storage/Engine:** PostgreSQL 16 Engine
- **Containerization:** Docker Compose network isolation

## 🚀 Getting Started

1. Clone this repository locally.
2. Initialize your localized configuration secrets by constructing a root `.env` file:
   ```text
   POSTGRES_PASSWORD=your_secure_password
   AIRFLOW_SECRET_KEY=your_session_encryption_key

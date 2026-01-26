# Airflow Pipeline Architecture

## Overview
Three Airflow DAGs for automated SEC data processing.

## Pipeline 1: Raw Storage Pipeline
**Purpose**: Load SEC data into RAW tables
**File**: `dags/raw_storage_pipeline.py`

**Tasks**:
1. Download SEC dataset
2. Validate file schema
3. Load to Snowflake RAW tables
4. Verify data integrity

**Schedule**: Quarterly

## Pipeline 2: JSON Transformation Pipeline
**Purpose**: Transform data to JSON format
**File**: `dags/json_pipeline.py`

**Tasks**:
1. Transform to JSON
2. Load to JSON_STORE schema

**Schedule**: Quarterly

## Pipeline 3: Fact Tables Pipeline
**Purpose**: Create denormalized analytics tables
**File**: `dags/fact_tables_pipeline.py`

**Tasks**:
1. Create fact tables
2. Populate from RAW data

**Schedule**: Quarterly

## Configuration
**Job Definition**: `config/job_definition.yaml`

## Status
- ✅ 3 DAG files created
- ✅ Job definition configured
- ✅ Pipeline architecture documented

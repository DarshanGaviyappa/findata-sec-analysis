-- JSON Storage Schema
-- Store as denormalized JSON documents

USE DATABASE FINDATA_DB;
CREATE SCHEMA IF NOT EXISTS JSON_STORE;
USE SCHEMA JSON_STORE;

CREATE TABLE FINANCIAL_STATEMENTS_JSON (
    id VARCHAR(50) PRIMARY KEY,
    cik INTEGER,
    company_name VARCHAR(255),
    filing_date DATE,
    fiscal_year INTEGER,
    fiscal_period VARCHAR(2),
    statement_data VARIANT
);

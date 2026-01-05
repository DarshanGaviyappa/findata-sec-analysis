-- Denormalized Fact Tables Schema
-- Pre-joined tables for analytics

USE DATABASE FINDATA_DB;
CREATE SCHEMA IF NOT EXISTS ANALYTICS;
USE SCHEMA ANALYTICS;

CREATE TABLE FACT_BALANCE_SHEET (
    fact_id VARCHAR(100) PRIMARY KEY,
    cik INTEGER,
    company_name VARCHAR(255),
    period_end_date DATE,
    fiscal_year INTEGER,
    total_assets DECIMAL(20,2),
    total_liabilities DECIMAL(20,2),
    total_equity DECIMAL(20,2)
);

CREATE TABLE FACT_INCOME_STATEMENT (
    fact_id VARCHAR(100) PRIMARY KEY,
    cik INTEGER,
    company_name VARCHAR(255),
    period_end_date DATE,
    fiscal_year INTEGER,
    revenue DECIMAL(20,2),
    net_income DECIMAL(20,2)
);

CREATE TABLE FACT_CASH_FLOW (
    fact_id VARCHAR(100) PRIMARY KEY,
    cik INTEGER,
    company_name VARCHAR(255),
    period_end_date DATE,
    fiscal_year INTEGER,
    operating_cash_flow DECIMAL(20,2),
    free_cash_flow DECIMAL(20,2)
);

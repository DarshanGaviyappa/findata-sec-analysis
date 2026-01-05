-- Raw Staging Schema
-- Store SEC data as-is (SUB, TAG, NUM, PRE)

CREATE DATABASE IF NOT EXISTS FINDATA_DB;
USE DATABASE FINDATA_DB;
CREATE SCHEMA IF NOT EXISTS RAW;
USE SCHEMA RAW;

CREATE TABLE RAW_SUB (
    adsh VARCHAR(20) PRIMARY KEY,
    cik INTEGER,
    name VARCHAR(255),
    form VARCHAR(10),
    period DATE,
    fy INTEGER,
    fp VARCHAR(2)
);

CREATE TABLE RAW_TAG (
    tag VARCHAR(256),
    version VARCHAR(20),
    tlabel VARCHAR(500),
    PRIMARY KEY (tag, version)
);

CREATE TABLE RAW_NUM (
    adsh VARCHAR(20),
    tag VARCHAR(256),
    ddate DATE,
    value DECIMAL(28,4)
);

CREATE TABLE RAW_PRE (
    adsh VARCHAR(20),
    tag VARCHAR(256),
    stmt VARCHAR(2),
    line INTEGER
);

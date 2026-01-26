"""FastAPI Backend for SEC Data"""
from fastapi import FastAPI
import snowflake.connector
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="FinData API", version="1.0")

def get_connection():
    return snowflake.connector.connect(
        user=os.getenv('SNOWFLAKE_USER'),
        password=os.getenv('SNOWFLAKE_PASSWORD'),
        account=os.getenv('SNOWFLAKE_ACCOUNT'),
        role='ACCOUNTADMIN'
    )

@app.get("/")
def root():
    return {"message": "FinData SEC API", "version": "1.0"}

@app.get("/raw/companies")
def get_companies(limit: int = 10):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("USE DATABASE FINDATA_DB")
    cursor.execute("USE SCHEMA RAW")
    cursor.execute(f"SELECT * FROM RAW_SUB LIMIT {limit}")
    
    columns = [desc[0] for desc in cursor.description]
    results = [dict(zip(columns, row)) for row in cursor.fetchall()]
    
    cursor.close()
    conn.close()
    
    return {"count": len(results), "data": results}

@app.get("/json/documents")
def get_json_docs(limit: int = 5):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("USE DATABASE FINDATA_DB")
    cursor.execute("USE SCHEMA JSON_STORE")
    cursor.execute(f"SELECT * FROM FINANCIAL_STATEMENTS_JSON LIMIT {limit}")
    
    columns = [desc[0] for desc in cursor.description]
    results = [dict(zip(columns, row)) for row in cursor.fetchall()]
    
    cursor.close()
    conn.close()
    
    return {"count": len(results), "data": results}

@app.get("/analytics/balance-sheet")
def get_balance_sheet(limit: int = 10):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("USE DATABASE FINDATA_DB")
    cursor.execute("USE SCHEMA ANALYTICS")
    cursor.execute(f"SELECT * FROM FACT_BALANCE_SHEET LIMIT {limit}")
    
    columns = [desc[0] for desc in cursor.description]
    results = [dict(zip(columns, row)) for row in cursor.fetchall()]
    
    cursor.close()
    conn.close()
    
    return {"count": len(results), "data": results}

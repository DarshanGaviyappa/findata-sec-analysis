"""Create denormalized fact tables"""
import snowflake.connector
import os
from dotenv import load_dotenv

load_dotenv()

def get_connection():
    return snowflake.connector.connect(
        user=os.getenv("SNOWFLAKE_USER"),
        password=os.getenv("SNOWFLAKE_PASSWORD"),
        account=os.getenv("SNOWFLAKE_ACCOUNT"),
        role="ACCOUNTADMIN"
    )

def create_fact_tables():
    print("\n" + "="*60)
    print("CREATING FACT TABLES - Storage Approach #3")
    print("="*60 + "\n")
    
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("USE DATABASE FINDATA_DB")
    cursor.execute("USE SCHEMA ANALYTICS")
    cursor.execute("USE WAREHOUSE COMPUTE_WH")
    
    # Create Balance Sheet Fact Table
    print("Creating FACT_BALANCE_SHEET...")
    cursor.execute("""
        CREATE OR REPLACE TABLE FACT_BALANCE_SHEET (
            fact_id VARCHAR(100),
            cik INTEGER,
            company_name VARCHAR(255),
            form_type VARCHAR(10),
            total_assets DECIMAL(20,2),
            total_liabilities DECIMAL(20,2),
            total_equity DECIMAL(20,2)
        )
    """)
    
    # Create Income Statement Fact Table
    print("Creating FACT_INCOME_STATEMENT...")
    cursor.execute("""
        CREATE OR REPLACE TABLE FACT_INCOME_STATEMENT (
            fact_id VARCHAR(100),
            cik INTEGER,
            company_name VARCHAR(255),
            form_type VARCHAR(10),
            revenue DECIMAL(20,2),
            net_income DECIMAL(20,2)
        )
    """)
    
    # Create Cash Flow Fact Table
    print("Creating FACT_CASH_FLOW...")
    cursor.execute("""
        CREATE OR REPLACE TABLE FACT_CASH_FLOW (
            fact_id VARCHAR(100),
            cik INTEGER,
            company_name VARCHAR(255),
            form_type VARCHAR(10),
            operating_cash_flow DECIMAL(20,2),
            free_cash_flow DECIMAL(20,2)
        )
    """)
    
    print("\n✅ All 3 fact tables created!\n")
    
    # Insert sample data (demonstration)
    print("Inserting sample data...")
    
    cursor.execute("USE SCHEMA RAW")
    cursor.execute("SELECT adsh, cik, name, form FROM RAW_SUB LIMIT 10")
    companies = cursor.fetchall()
    
    cursor.execute("USE SCHEMA ANALYTICS")
    
    for adsh, cik, name, form in companies:
        # Sample Balance Sheet
        cursor.execute("""
            INSERT INTO FACT_BALANCE_SHEET VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (adsh, cik, name, form, 1000000.00, 600000.00, 400000.00))
        
        # Sample Income Statement
        cursor.execute("""
            INSERT INTO FACT_INCOME_STATEMENT VALUES (%s, %s, %s, %s, %s, %s)
        """, (adsh, cik, name, form, 500000.00, 50000.00))
        
        # Sample Cash Flow
        cursor.execute("""
            INSERT INTO FACT_CASH_FLOW VALUES (%s, %s, %s, %s, %s, %s)
        """, (adsh, cik, name, form, 75000.00, 60000.00))
    
    conn.commit()
    print(f"✅ Inserted sample data for {len(companies)} companies\n")
    
    # Verify
    cursor.execute("SELECT COUNT(*) FROM FACT_BALANCE_SHEET")
    bs_count = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM FACT_INCOME_STATEMENT")
    is_count = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM FACT_CASH_FLOW")
    cf_count = cursor.fetchone()[0]
    
    print("="*60)
    print("VERIFICATION")
    print("="*60)
    print(f"FACT_BALANCE_SHEET: {bs_count} records")
    print(f"FACT_INCOME_STATEMENT: {is_count} records")
    print(f"FACT_CASH_FLOW: {cf_count} records")
    print("="*60)
    
    print("\n✅ Storage Approach #3 (Fact Tables) - IMPLEMENTED!")
    
    cursor.close()
    conn.close()

if __name__ == "__main__":
    create_fact_tables()

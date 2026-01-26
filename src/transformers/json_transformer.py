"""Transform SEC data into JSON format"""
import snowflake.connector
import os
from dotenv import load_dotenv
import json

load_dotenv()

def get_connection():
    return snowflake.connector.connect(
        user=os.getenv("SNOWFLAKE_USER"),
        password=os.getenv("SNOWFLAKE_PASSWORD"),
        account=os.getenv("SNOWFLAKE_ACCOUNT"),
        role="ACCOUNTADMIN"
    )

def transform_to_json():
    print("\n" + "="*60)
    print("JSON TRANSFORMATION - Storage Approach #2")
    print("="*60 + "\n")
    
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("USE DATABASE FINDATA_DB")
    cursor.execute("USE SCHEMA JSON_STORE")
    cursor.execute("USE WAREHOUSE COMPUTE_WH")
    
    print("Creating table...")
    cursor.execute("""
        CREATE OR REPLACE TABLE FINANCIAL_STATEMENTS_JSON (
            id VARCHAR(50),
            cik INTEGER,
            company_name VARCHAR(255),
            form_type VARCHAR(10),
            statement_data VARIANT
        )
    """)
    print("✅ Table created\n")
    
    cursor.execute("USE SCHEMA RAW")
    cursor.execute("SELECT adsh, cik, name, form FROM RAW_SUB LIMIT 50")
    companies = cursor.fetchall()
    print(f"Found {len(companies)} companies\n")
    
    cursor.execute("USE SCHEMA JSON_STORE")
    
    print("Transforming...")
    for i, (adsh, cik, name, form) in enumerate(companies):
        json_doc = {
            "company": {"cik": cik, "name": name},
            "filing": {"form": form},
            "metadata": {"source": "SEC"}
        }
        
        json_str = json.dumps(json_doc)
        
        cursor.execute(f"""
            INSERT INTO FINANCIAL_STATEMENTS_JSON 
            SELECT %s, %s, %s, %s, PARSE_JSON(%s)
        """, (adsh, cik, name, form, json_str))
        
        if (i+1) % 10 == 0:
            print(f"  {i+1} / {len(companies)} done...")
            conn.commit()
    
    conn.commit()
    print(f"\n✅ Transformed {len(companies)} records\n")
    
    cursor.execute("SELECT COUNT(*) FROM FINANCIAL_STATEMENTS_JSON")
    print(f"✅ Verified: {cursor.fetchone()[0]} documents\n")
    
    print("="*60)
    print("✅ JSON STORAGE COMPLETE!")
    print("="*60)
    
    cursor.close()
    conn.close()

if __name__ == "__main__":
    transform_to_json()

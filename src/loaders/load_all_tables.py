"""Load all SEC tables into Snowflake"""
import pandas as pd
import snowflake.connector
import os
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()

def get_connection():
    return snowflake.connector.connect(
        user=os.getenv("SNOWFLAKE_USER"),
        password=os.getenv("SNOWFLAKE_PASSWORD"),
        account=os.getenv("SNOWFLAKE_ACCOUNT"),
        role="ACCOUNTADMIN"
    )

def main():
    print("\n" + "="*60)
    print("LOADING ALL TABLES")
    print("="*60 + "\n")
    
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("USE DATABASE FINDATA_DB")
    cursor.execute("USE SCHEMA RAW")
    cursor.execute("USE WAREHOUSE COMPUTE_WH")
    
    # Create TAG table
    print("Creating TAG table...")
    cursor.execute("""
        CREATE OR REPLACE TABLE RAW_TAG (
            tag VARCHAR(256),
            version VARCHAR(20),
            tlabel VARCHAR(500)
        )
    """)
    
    # Load TAG
    print("Loading TAG data...")
    data_dir = Path("data/raw/sample/2024q4")
    tag = pd.read_csv(data_dir / "tag.txt", sep="\t", nrows=1000)  # Load first 1000 for testing
    
    for i, row in tag.iterrows():
        cursor.execute(
            "INSERT INTO RAW_TAG (tag, version, tlabel) VALUES (%s, %s, %s)",
            (row["tag"], row["version"], row["tlabel"] if pd.notna(row["tlabel"]) else None)
        )
        if (i+1) % 100 == 0:
            print(f"  Loaded {i+1} records...")
            conn.commit()
    
    conn.commit()
    print(f"✅ TAG loaded: {len(tag)} records\n")
    
    # Verify
    cursor.execute("SELECT COUNT(*) FROM RAW_TAG")
    count = cursor.fetchone()[0]
    print(f"✅ Verified: {count:,} records\n")
    
    print("="*60)
    print("SUCCESS!")
    print("="*60)
    
    cursor.close()
    conn.close()

if __name__ == "__main__":
    main()

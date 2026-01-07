"""Create tables and load data"""
import pandas as pd
import snowflake.connector
import os
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()

def get_connection():
    return snowflake.connector.connect(
        user=os.getenv('SNOWFLAKE_USER'),
        password=os.getenv('SNOWFLAKE_PASSWORD'),
        account=os.getenv('SNOWFLAKE_ACCOUNT'),
        role='ACCOUNTADMIN'
    )

def main():
    print("\n" + "="*60)
    print("SETUP AND LOAD DATA")
    print("="*60 + "\n")
    
    conn = get_connection()
    cursor = conn.cursor()
    
    # Set context
    print("Setting up database context...")
    cursor.execute("USE DATABASE FINDATA_DB")
    cursor.execute("USE SCHEMA RAW")
    cursor.execute("USE WAREHOUSE COMPUTE_WH")
    
    # Create table
    print("Creating RAW_SUB table...")
    cursor.execute("""
        CREATE OR REPLACE TABLE RAW_SUB (
            adsh VARCHAR(20),
            cik INTEGER,
            name VARCHAR(255),
            form VARCHAR(10)
        )
    """)
    print("✅ Table created\n")
    
    # Load data
    print("📊 Loading SUB data...")
    data_dir = Path("data/raw/sample/2024q4")
    sub = pd.read_csv(data_dir / "sub.txt", sep='\t')
    
    count = 0
    for i, row in sub.iterrows():
        cursor.execute(
            "INSERT INTO RAW_SUB (adsh, cik, name, form) VALUES (%s, %s, %s, %s)",
            (row['adsh'], int(row['cik']), row['name'], row['form'])
        )
        count += 1
        if count % 500 == 0:
            print(f"  Loaded {count:,} / {len(sub):,} records...")
            conn.commit()
    
    conn.commit()
    print(f"\n✅ Loaded {count:,} records\n")
    
    # Verify
    cursor.execute("SELECT COUNT(*) FROM RAW_SUB")
    verify_count = cursor.fetchone()[0]
    print(f"✅ Verified: {verify_count:,} records in database\n")
    
    # Show sample
    cursor.execute("SELECT * FROM RAW_SUB LIMIT 5")
    print("Sample data:")
    for row in cursor.fetchall():
        print(f"  {row}")
    
    print("\n" + "="*60)
    print("SUCCESS!")
    print("="*60)
    
    cursor.close()
    conn.close()

if __name__ == "__main__":
    main()

"""Bulk load all tables using direct file reading"""
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
    print("BULK LOADING ALL TABLES")
    print("="*60 + "\n")
    
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("USE DATABASE FINDATA_DB")
    cursor.execute("USE SCHEMA RAW")
    cursor.execute("USE WAREHOUSE COMPUTE_WH")
    
    data_dir = Path("data/raw/sample/2024q4")
    
    # Load TAG (full dataset - ~84K records)
    print("📊 Loading full TAG table...")
    cursor.execute("TRUNCATE TABLE RAW_TAG")
    
    tag = pd.read_csv(data_dir / "tag.txt", sep='\t')
    print(f"  Found {len(tag):,} records")
    
    # Use executemany for better performance
    records = [
        (row['tag'], row['version'], row['tlabel'] if pd.notna(row['tlabel']) else None)
        for _, row in tag.iterrows()
    ]
    
    cursor.executemany(
        "INSERT INTO RAW_TAG (tag, version, tlabel) VALUES (%s, %s, %s)",
        records
    )
    conn.commit()
    print(f"✅ TAG loaded: {len(tag):,} records\n")
    
    # Verify TAG
    cursor.execute("SELECT COUNT(*) FROM RAW_TAG")
    print(f"✅ Verified TAG: {cursor.fetchone()[0]:,} records\n")
    
    # Load PRE (~737K records)
    print("📊 Loading PRE table...")
    cursor.execute("""
        CREATE OR REPLACE TABLE RAW_PRE (
            adsh VARCHAR(20),
            tag VARCHAR(256),
            stmt VARCHAR(2),
            line INTEGER
        )
    """)
    
    pre = pd.read_csv(data_dir / "pre.txt", sep='\t')
    print(f"  Found {len(pre):,} records")
    
    # Load in chunks
    chunk_size = 5000
    for i in range(0, len(pre), chunk_size):
        chunk = pre.iloc[i:i+chunk_size]
        records = [
            (row['adsh'], row['tag'], row['stmt'] if pd.notna(row['stmt']) else None, int(row['line']) if pd.notna(row['line']) else None)
            for _, row in chunk.iterrows()
        ]
        cursor.executemany(
            "INSERT INTO RAW_PRE (adsh, tag, stmt, line) VALUES (%s, %s, %s, %s)",
            records
        )
        conn.commit()
        print(f"  Loaded {min(i+chunk_size, len(pre)):,} / {len(pre):,} records...")
    
    print(f"✅ PRE loaded: {len(pre):,} records\n")
    
    # Verify PRE
    cursor.execute("SELECT COUNT(*) FROM RAW_PRE")
    print(f"✅ Verified PRE: {cursor.fetchone()[0]:,} records\n")
    
    # Summary
    print("="*60)
    print("FINAL SUMMARY")
    print("="*60)
    cursor.execute("SELECT 'RAW_SUB' as table_name, COUNT(*) as count FROM RAW_SUB")
    print(f"RAW_SUB: {cursor.fetchone()[1]:,} records")
    cursor.execute("SELECT COUNT(*) FROM RAW_TAG")
    print(f"RAW_TAG: {cursor.fetchone()[0]:,} records")
    cursor.execute("SELECT COUNT(*) FROM RAW_PRE")
    print(f"RAW_PRE: {cursor.fetchone()[0]:,} records")
    print("="*60)
    
    print("\n✅ 3 out of 4 tables loaded!")
    print("⚠️  NUM table (3.7M records) skipped for now - can add later")
    
    cursor.close()
    conn.close()

if __name__ == "__main__":
    main()

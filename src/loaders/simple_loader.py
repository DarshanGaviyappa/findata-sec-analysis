"""Simple data loader for Snowflake"""
import pandas as pd
import snowflake.connector
import os
from dotenv import load_dotenv
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)

load_dotenv()

def get_connection():
    return snowflake.connector.connect(
        user=os.getenv('SNOWFLAKE_USER'),
        password=os.getenv('SNOWFLAKE_PASSWORD'),
        account=os.getenv('SNOWFLAKE_ACCOUNT'),
        warehouse=os.getenv('SNOWFLAKE_WAREHOUSE'),
        database='FINDATA_DB',
        schema='RAW',
        role='ACCOUNTADMIN'
    )

def load_data():
    data_dir = Path("data/raw/sample/2024q4")
    
    print("\n" + "="*60)
    print("LOADING SEC Q4 2024 DATA INTO SNOWFLAKE")
    print("="*60 + "\n")
    
    conn = get_connection()
    cursor = conn.cursor()
    
    try:
        # Load SUB (small table - 6K rows)
        print("📊 Loading SUB table...")
        sub = pd.read_csv(data_dir / "sub.txt", sep='\t')
        cursor.execute("TRUNCATE TABLE RAW_SUB")
        
        for i, row in sub.iterrows():
            cursor.execute(
                "INSERT INTO RAW_SUB (adsh, cik, name, form) VALUES (%s, %s, %s, %s)",
                (row['adsh'], int(row['cik']), row['name'], row['form'])
            )
            if (i+1) % 500 == 0:
                print(f"  Loaded {i+1:,} / {len(sub):,} records...")
                conn.commit()
        
        conn.commit()
        print(f"✅ SUB table loaded: {len(sub):,} records\n")
        
        # Verify
        cursor.execute("SELECT COUNT(*) FROM RAW_SUB")
        count = cursor.fetchone()[0]
        print(f"✅ Verified: {count:,} records in RAW_SUB\n")
        
        print("="*60)
        print("SUCCESS! Data loaded into Snowflake")
        print("="*60)
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        raise
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    load_data()

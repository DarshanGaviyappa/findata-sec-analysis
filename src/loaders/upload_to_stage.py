"""Upload files to Snowflake stage"""
import snowflake.connector
import os
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()

def upload_files():
    print("\n" + "="*60)
    print("UPLOADING FILES TO SNOWFLAKE STAGE")
    print("="*60 + "\n")
    
    conn = snowflake.connector.connect(
        user=os.getenv('SNOWFLAKE_USER'),
        password=os.getenv('SNOWFLAKE_PASSWORD'),
        account=os.getenv('SNOWFLAKE_ACCOUNT'),
        role='ACCOUNTADMIN'
    )
    
    cursor = conn.cursor()
    
    # Set context
    cursor.execute("USE DATABASE FINDATA_DB")
    cursor.execute("USE SCHEMA RAW")
    cursor.execute("USE WAREHOUSE COMPUTE_WH")
    
    # Create stage if not exists
    cursor.execute("CREATE STAGE IF NOT EXISTS sec_stage")
    print("✅ Stage created\n")
    
    # Upload files
    data_dir = Path("data/raw/sample/2024q4")
    files = ['tag.txt', 'num.txt', 'pre.txt']
    
    for filename in files:
        filepath = data_dir / filename
        print(f"📤 Uploading {filename}...")
        
        # PUT command uploads local file to stage
        cursor.execute(f"PUT file://{filepath.absolute()} @sec_stage AUTO_COMPRESS=FALSE")
        print(f"✅ {filename} uploaded\n")
    
    # List files in stage
    cursor.execute("LIST @sec_stage")
    print("Files in stage:")
    for row in cursor.fetchall():
        print(f"  - {row[0]}")
    
    print("\n" + "="*60)
    print("ALL FILES UPLOADED!")
    print("="*60)
    
    cursor.close()
    conn.close()

if __name__ == "__main__":
    upload_files()

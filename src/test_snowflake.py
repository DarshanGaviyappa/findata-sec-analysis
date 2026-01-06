"""Test Snowflake connection and show what exists"""
import snowflake.connector
import os
from dotenv import load_dotenv

load_dotenv()

print("Testing Snowflake connection...")

try:
    conn = snowflake.connector.connect(
        user=os.getenv('SNOWFLAKE_USER'),
        password=os.getenv('SNOWFLAKE_PASSWORD'),
        account=os.getenv('SNOWFLAKE_ACCOUNT'),
        role='ACCOUNTADMIN'
    )
    
    cursor = conn.cursor()
    
    print(f"✅ Connected to Snowflake!")
    
    # Show all databases
    cursor.execute("SHOW DATABASES")
    databases = cursor.fetchall()
    print(f"\n📊 Found {len(databases)} databases:")
    for db in databases:
        print(f"  - {db[1]}")
    
    # Create FINDATA_DB if it doesn't exist
    print("\n🔧 Creating FINDATA_DB database...")
    cursor.execute("CREATE DATABASE IF NOT EXISTS FINDATA_DB")
    cursor.execute("USE DATABASE FINDATA_DB")
    
    # Create schemas
    print("🔧 Creating schemas...")
    cursor.execute("CREATE SCHEMA IF NOT EXISTS RAW")
    cursor.execute("CREATE SCHEMA IF NOT EXISTS JSON_STORE")
    cursor.execute("CREATE SCHEMA IF NOT EXISTS ANALYTICS")
    
    # Show schemas
    cursor.execute("SHOW SCHEMAS")
    schemas = cursor.fetchall()
    print(f"\n📊 Schemas in FINDATA_DB:")
    for schema in schemas:
        print(f"  - {schema[1]}")
    
    print("\n✅ Database setup complete!")
    print("✅ Ready to create tables and load data!")
    
    cursor.close()
    conn.close()
    
except Exception as e:
    print(f"\n❌ Error: {e}")
    import traceback
    traceback.print_exc()

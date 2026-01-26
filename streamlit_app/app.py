"""Streamlit App - SEC Financial Data Explorer"""
import streamlit as st
import snowflake.connector
import pandas as pd
import os
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(page_title="FinData SEC Explorer", layout="wide")

st.title("🏦 SEC Financial Statement Database")
st.markdown("### Compare 3 Storage Approaches")

# Snowflake connection
@st.cache_resource
def get_connection():
    return snowflake.connector.connect(
        user=os.getenv('SNOWFLAKE_USER'),
        password=os.getenv('SNOWFLAKE_PASSWORD'),
        account=os.getenv('SNOWFLAKE_ACCOUNT'),
        role='ACCOUNTADMIN'
    )

conn = get_connection()

# Sidebar
st.sidebar.header("Storage Approach Comparison")
approach = st.sidebar.selectbox(
    "Select Storage Approach",
    ["Raw RDBMS", "JSON Storage", "Fact Tables"]
)

# Main content
if approach == "Raw RDBMS":
    st.header("📊 Raw Storage (RDBMS)")
    st.write("Data stored as-is in normalized tables")
    
    cursor = conn.cursor()
    cursor.execute("USE DATABASE FINDATA_DB")
    cursor.execute("USE SCHEMA RAW")
    
    cursor.execute("SELECT COUNT(*) FROM RAW_SUB")
    sub_count = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM RAW_TAG")
    tag_count = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM RAW_PRE")
    pre_count = cursor.fetchone()[0]
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Companies", f"{sub_count:,}")
    col2.metric("Tags", f"{tag_count:,}")
    col3.metric("Presentation Records", f"{pre_count:,}")
    
    # Show sample data
    cursor.execute("SELECT * FROM RAW_SUB LIMIT 10")
    df = pd.DataFrame(cursor.fetchall(), columns=[desc[0] for desc in cursor.description])
    st.dataframe(df)
    
elif approach == "JSON Storage":
    st.header("📄 JSON Storage (VARIANT)")
    st.write("Data stored as JSON documents in VARIANT column")
    
    cursor = conn.cursor()
    cursor.execute("USE DATABASE FINDATA_DB")
    cursor.execute("USE SCHEMA JSON_STORE")
    
    cursor.execute("SELECT COUNT(*) FROM FINANCIAL_STATEMENTS_JSON")
    count = cursor.fetchone()[0]
    st.metric("JSON Documents", count)
    
    cursor.execute("SELECT company_name, statement_data FROM FINANCIAL_STATEMENTS_JSON LIMIT 5")
    for row in cursor.fetchall():
        st.subheader(row[0])
        st.json(str(row[1]))
        
else:
    st.header("📈 Fact Tables (Denormalized)")
    st.write("Pre-joined tables optimized for analytics")
    
    cursor = conn.cursor()
    cursor.execute("USE DATABASE FINDATA_DB")
    cursor.execute("USE SCHEMA ANALYTICS")
    
    cursor.execute("SELECT * FROM FACT_BALANCE_SHEET LIMIT 10")
    df = pd.DataFrame(cursor.fetchall(), columns=[desc[0] for desc in cursor.description])
    st.dataframe(df)

st.sidebar.markdown("---")
st.sidebar.info("Built for Assignment 2 - FinData Inc.")

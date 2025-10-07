import streamlit as st
import requests
import base64
import json

st.set_page_config(page_title="Snowflake AI Evaluation", layout="centered")

st.title("💬 Snowflake AI Evaluation (POC)")

usecase_name = st.text_input("Enter Use Case Name:")
run_btn = st.button("Run AI Evaluation")

ACCOUNT = "your-account-id"      # e.g., qdzxiy-aob89714
USER = "RITHISH"
PASSWORD = "your_password"
WAREHOUSE = "TRIAL_WH"
DATABASE = "TRIAL_DB"
SCHEMA = "INGESTION"
ROLE = "ACCOUNTADMIN"

def call_snowflake(usecase_name):
    statement = f"CALL EVALUATE_USECASE_QUALITY('{usecase_name}');"
    auth = base64.b64encode(f"{USER}:{PASSWORD}".encode()).decode()
    body = {
        "statement": statement,
        "warehouse": WAREHOUSE,
        "database": DATABASE,
        "schema": SCHEMA,
        "role": ROLE
    }
    url = f"https://{ACCOUNT}.snowflakecomputing.com/api/v2/statements"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Basic {auth}"
    }
    r = requests.post(url, headers=headers, data=json.dumps(body))
    return r.json() if r.status_code == 200 else {"error": r.text}

if run_btn and usecase_name:
    st.info("Running evaluation...")
    st.json(call_snowflake(usecase_name))

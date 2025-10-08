import streamlit as st, requests, base64, json

st.set_page_config(page_title="Cortex Chat", layout="centered")
st.title("💬 Snowflake Cortex (Web-only POC)")

usecase = st.text_input("Use case name", placeholder="e.g., Sales Forecasting")
if st.button("Run Cortex"):
    if not usecase:
        st.warning("Enter a use case first.")
        st.stop()

    # Read secrets from Streamlit Cloud (set in step 3)
    ACCOUNT = st.secrets["snowflake"]["account"]      # e.g. qdzxiy-aob89714
    USER     = st.secrets["snowflake"]["user"]
    PASSWORD = st.secrets["snowflake"]["password"]
    WAREHOUSE= st.secrets["snowflake"]["warehouse"]   # TRIAL_WH
    DATABASE = st.secrets["snowflake"]["database"]    # TRIAL_DB
    SCHEMA   = st.secrets["snowflake"]["schema"]      # INGESTION
    ROLE     = st.secrets["snowflake"]["role"]        # ACCOUNTADMIN

    auth = base64.b64encode(f"{USER}:{PASSWORD}".encode()).decode()
    body = {
        "statement": f"CALL EVALUATE_USECASE_QUALITY('{usecase}');",
        "warehouse": WAREHOUSE,
        "database": DATABASE,
        "schema": SCHEMA,
        "role": ROLE
    }
    url = f"https://{ACCOUNT}.snowflakecomputing.com/api/v2/statements"
    headers = {"Content-Type":"application/json", "Authorization":f"Basic {auth}"}

    with st.spinner("Calling Cortex…"):
        r = requests.post(url, headers=headers, data=json.dumps(body))
    if r.status_code != 200:
        st.error(f"Error {r.status_code}: {r.text}")
    else:
        data = r.json()
        st.success("Done ✅")
        st.subheader("Raw Response")
        st.json(data)

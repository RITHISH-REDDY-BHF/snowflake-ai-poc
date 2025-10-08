import streamlit as st
import snowflake.connector as sf

st.title("💬 Snowflake Cortex (Web) POC")

use_case = st.text_input("Use case name", "sales")
if st.button("Run Cortex"):
    try:
        cfg = st.secrets["snowflake"]   # must exist as shown above
        con = sf.connect(
            account=cfg["account"],
            user=cfg["user"],
            password=cfg["password"],
            warehouse=cfg["warehouse"],
            database=cfg["database"],
            schema=cfg["schema"],
            role=cfg["role"],
        )
        cur = con.cursor()

        # Example 1: Call your view that uses SNOWFLAKE.CORTEX.COMPLETE
        cur.execute("SELECT NAME, RATING, AI_SUMMARY FROM V_USECASE_QUALITY_WITH_AI LIMIT 5")
        rows = cur.fetchall()
        st.write("Top rows with AI summary:")
        st.dataframe(rows)

        # Example 2: Call your stored proc (if you have one)
        # cur.execute("CALL EVALUATE_USECASE_QUALITY(%s)", (use_case,))

        cur.close()
        con.close()
    except KeyError as e:
        st.error(f"Missing secret key: {e}. Check Settings → Secrets.")
    except Exception as e:
        st.error(str(e))

# TTLens - TTL Analyzer Tool for Apache Cassandra
# Project Catalyst | Author: [Your Name]

import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider
import re
import io

st.set_page_config(page_title="TTLens - TTL Analyzer", layout="wide")
st.sidebar.title("TTLens Input Mode")
mode = st.sidebar.radio("Choose mode:", ["📂 Upload File", "🌐 Connect to Cluster"])

st.title("🕒 TTLens – Cassandra TTL Expiry Analyzer")

def parse_schema_file(uploaded_file):
    content = uploaded_file.read().decode("utf-8")
    tables = []
    for match in re.finditer(r"CREATE TABLE (\w+)\.(\w+).*?WITH.*?default_time_to_live\s*=\s*(\d+)", content, re.DOTALL):
        keyspace, table, ttl = match.groups()
        tables.append({
            "Keyspace": keyspace,
            "Table": table,
            "TTL (sec)": int(ttl),
            "Source": "default_time_to_live"
        })
    return pd.DataFrame(tables)

if mode == "📂 Upload File":
    uploaded_file = st.file_uploader("Upload a schema.cql", type=["cql"])
    if uploaded_file:
        st.success(f"File `{uploaded_file.name}` uploaded successfully.")
        ttl_table_data = parse_schema_file(uploaded_file)
        if not ttl_table_data.empty:
            st.subheader("🧾 TTL-Enabled Tables")
            st.dataframe(ttl_table_data, use_container_width=True)
        else:
            st.warning("No default_time_to_live settings found in uploaded schema.")

elif mode == "🌐 Connect to Cluster":
    st.subheader("Cluster Connection")
    host = st.text_input("Host")
    port = st.number_input("Port", value=9042)
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    connect = st.button("Connect")

    if connect:
        try:
            auth_provider = PlainTextAuthProvider(username=username, password=password)
            cluster = Cluster([host], port=port, auth_provider=auth_provider)
            session = cluster.connect()
            st.session_state["cluster"] = cluster
            st.session_state["session"] = session
            st.session_state["connected"] = True
            st.success(f"Connected to {host}:{port}")
        except Exception as e:
            st.error(f"Connection failed: {str(e)}")

    if st.session_state.get("connected"):
        with st.expander("🧪 Multi-Column TTL Scanner"):
            keyspace = st.text_input("Keyspace")
            table = st.text_input("Table")
            partition_key_column = st.text_input("Partition Key Column")
            partition_key_value = st.text_input("Partition Key Value")
            columns_to_check = st.text_input("Comma-separated column names to scan for TTL")

            if st.button("Scan TTLs for All Columns"):
                try:
                    session = st.session_state["session"]
                    cols = [col.strip() for col in columns_to_check.split(",")]
                    select_clause = ", ".join([f"ttl({col})" for col in cols])
                    query = f"SELECT {select_clause} FROM {keyspace}.{table} WHERE {partition_key_column} = '{partition_key_value}' LIMIT 1;"
                    result = session.execute(query)
                    row = result.one()

                    if row:
                        ttl_data = []
                        for i, col in enumerate(cols):
                            ttl_val = row[i]
                            ttl_data.append({
                                "Column": col,
                                "TTL Remaining (sec)": ttl_val if ttl_val is not None else "∞ / No TTL",
                                "Expiring": ttl_val is not None
                            })
                        df = pd.DataFrame(ttl_data)
                        st.session_state["last_ttl_df"] = df
                        st.dataframe(df)

                        csv_buffer = io.StringIO()
                        df.to_csv(csv_buffer, index=False)
                        st.download_button(
                            label="📥 Download TTL Results as CSV",
                            data=csv_buffer.getvalue(),
                            file_name=f"ttl_scan_{table}.csv",
                            mime="text/csv"
                        )
                    else:
                        st.info("No row found for the provided partition key value.")
                except Exception as err:
                    st.error(f"Query error: {err}")
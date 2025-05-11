# TTLens - TTL Analyzer Tool for Apache Cassandra
# Project Catalyst | Author: [Your Name]

# This is the entry point for TTLens using Streamlit (MVP Version)

import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta
from io import StringIO
import re

# For cluster connection
from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider
from cassandra.metadata import TableMetadata

# ---------------------------
# Sidebar - Mode Selection
# ---------------------------
st.set_page_config(page_title="TTLens - TTL Analyzer", layout="wide")
st.sidebar.title("TTLens Input Mode")
mode = st.sidebar.radio("Choose mode:", ["📂 Upload File", "🌐 Connect to Cluster"])

st.title("🕒 TTLens – Cassandra TTL Expiry Analyzer")

# ---------------------------
# File Parsers
# ---------------------------
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

def parse_histogram_file(uploaded_file):
    content = uploaded_file.read().decode("utf-8")
    lines = content.splitlines()
    data_start = False
    rows = []
    for line in lines:
        if 'Percentile' in line and 'Partition Size' in line:
            data_start = True
            continue
        if data_start and line.strip():
            parts = re.split(r"\s{2,}", line.strip())
            if len(parts) >= 5:
                rows.append({
                    "Percentile": parts[0],
                    "Write Latency (μs)": int(parts[2]),
                    "Read Latency (μs)": int(parts[3]),
                    "Partition Size (bytes)": int(parts[4]),
                    "Cell Count": int(parts[5]) if len(parts) > 5 else None
                })
    return pd.DataFrame(rows)

def simulate_ttl_decay_chart(title):
    expiry_hours = ["1h", "6h", "12h", "24h", "3d", "7d"]
    expiring_data = [5000, 30000, 70000, 100000, 400000, 700000]
    df = pd.DataFrame({"Time Bucket": expiry_hours, "Records Expiring": expiring_data})
    fig = px.bar(df, x="Time Bucket", y="Records Expiring", title=title)
    st.plotly_chart(fig, use_container_width=True)

# ---------------------------
# 📂 Upload File Mode
# ---------------------------
if mode == "📂 Upload File":
    uploaded_file = st.file_uploader("Upload a schema.cql or tablehistograms.txt", type=["cql", "txt"])
    if uploaded_file:
        st.success(f"File `{uploaded_file.name}` uploaded successfully.")

        if uploaded_file.name.endswith(".cql"):
            ttl_table_data = parse_schema_file(uploaded_file)
            if not ttl_table_data.empty:
                st.subheader("🧾 TTL-Enabled Tables")
                st.dataframe(ttl_table_data, use_container_width=True)
                st.subheader("📊 TTL Expiry Timeline (Simulated)")
                simulate_ttl_decay_chart("Projected Record Expiry")
            else:
                st.warning("No default_time_to_live settings found in uploaded schema.")

        elif uploaded_file.name.endswith(".txt"):
            histogram_df = parse_histogram_file(uploaded_file)
            if not histogram_df.empty:
                st.subheader("📈 Table Histogram Metrics")
                st.dataframe(histogram_df, use_container_width=True)
                fig = px.bar(histogram_df, x="Percentile", y="Partition Size (bytes)",
                             title="Partition Size by Percentile")
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.warning("Could not parse histogram data. Please check the format.")

# ---------------------------
# 🌐 Connect to Cluster Mode
# ---------------------------
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

            query = """
            SELECT keyspace_name, table_name, default_time_to_live 
            FROM system_schema.tables 
            WHERE default_time_to_live > 0 ALLOW FILTERING;
            """
            rows = session.execute(query)
            data = [{
                "Keyspace": row.keyspace_name,
                "Table": row.table_name,
                "TTL (sec)": row.default_time_to_live,
                "Source": "default_time_to_live"
            } for row in rows]

            ttl_table_data = pd.DataFrame(data)

            st.success(f"Connected to {host}:{port} – Fetched TTL tables")
            st.subheader("🧾 TTL-Enabled Tables (Live Cluster)")
            st.dataframe(ttl_table_data, use_container_width=True)

            st.subheader("📊 TTL Expiry Projection (Simulated)")
            simulate_ttl_decay_chart("Live TTL Expiry Projection")

        except Exception as e:
            st.error(f"Connection failed: {str(e)}")

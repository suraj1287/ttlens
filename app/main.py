import streamlit as st
import pandas as pd
import plotly.express as px

# Set page config
st.set_page_config(page_title="TTLens - TTL Analyzer", layout="wide")
st.sidebar.title("TTLens Input Mode")
mode = st.sidebar.radio("Choose mode:", ["📂 Upload File", "🌐 Connect to Cluster"])

st.title("🕒 TTLens – Cassandra TTL Expiry Analyzer")

# Simulated TTL Table parser
def parse_schema_file(uploaded_file):
    return pd.DataFrame({
        "Keyspace": ["events_ks", "logs_ks"],
        "Table": ["events_by_user", "logs_by_host"],
        "TTL (sec)": [86400, 604800],
        "Source": ["default_time_to_live", "column-level"]
    })

# Simulated chart
def simulate_ttl_decay_chart(title):
    expiry_hours = ["1h", "6h", "12h", "24h", "3d", "7d"]
    expiring_data = [5000, 30000, 70000, 100000, 400000, 700000]
    df = pd.DataFrame({"Time Bucket": expiry_hours, "Records Expiring": expiring_data})
    fig = px.bar(df, x="Time Bucket", y="Records Expiring", title=title)
    st.plotly_chart(fig, use_container_width=True)

# Upload Mode
if mode == "📂 Upload File":
    uploaded_file = st.file_uploader("Upload schema.cql or tablehistograms.txt", type=["cql", "txt"])
    if uploaded_file:
        st.success(f"File `{uploaded_file.name}` uploaded successfully.")
        ttl_table_data = parse_schema_file(uploaded_file)
        st.subheader("🧾 TTL-Enabled Tables")
        st.dataframe(ttl_table_data, use_container_width=True)
        st.subheader("📊 TTL Expiry Timeline")
        simulate_ttl_decay_chart("Simulated Expiry")

# Connect Mode
elif mode == "🌐 Connect to Cluster":
    st.subheader("Cluster Connection")
    host = st.text_input("Host")
    port = st.number_input("Port", value=9042)
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    connect = st.button("Connect")

    if connect:
        st.success(f"Connected to cluster at {host}:{port} (simulated)")
        ttl_table_data = pd.DataFrame({
            "Keyspace": ["live_ks"],
            "Table": ["metrics_by_device"],
            "TTL (sec)": [432000],
            "Source": ["default_time_to_live"]
        })
        st.subheader("🧾 TTL-Enabled Tables (Live)")
        st.dataframe(ttl_table_data, use_container_width=True)
        st.subheader("📊 TTL Expiry Projection")
        simulate_ttl_decay_chart("Simulated Live TTL Expiry")

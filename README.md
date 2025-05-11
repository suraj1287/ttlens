# 🕒 TTLens – TTL Analyzer for Apache Cassandra

**TTLens** is a lightweight, diagnostic tool built with Streamlit to analyze and visualize TTL (Time-To-Live) behavior in Apache Cassandra and DataStax Enterprise.

It helps support engineers and database administrators:
- Upload `.cql` or `tablehistograms.txt` files to inspect TTL-enabled tables
- Detect `default_time_to_live` settings from schema files
- Visualize projected row expirations over time
- (Coming Soon) Connect directly to Cassandra clusters to analyze TTLs at row-level

---

## 🔧 Features

- 📂 Upload `.cql` files and extract TTL settings
- 📊 View TTL expiry timeline in hours/days
- 🌐 (Planned) Connect to live Cassandra clusters
- 🧪 (Planned) Analyze row-level TTL decay using live TTL queries
- 📈 (Planned) Parse `nodetool tablehistograms` for tombstone trends

---

## 📦 Sample Upload Files

This repo includes:
- `sample_schema.cql`: Demonstrates tables with and without TTL
- `tablehistograms.txt`: Simulated nodetool output for testing

---

## 🚀 Getting Started

### 1. Clone the repo

```bash
git clone https://github.com/suraj1287/ttlens.git
cd ttlens

python3 -m venv venv
source venv/bin/activate

pip install -r requirements.txt

streamlit run app/main.py


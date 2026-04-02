# Snowpark Connect for Spark — PySpark Hello World

A minimal example showing how to run **PySpark DataFrame** workloads on
**Snowflake's compute engine** using
[Snowpark Connect for Apache Spark](https://docs.snowflake.com/en/developer-guide/snowpark-connect/snowpark-connect-overview).

No Spark cluster to manage — Snowflake handles all the compute.

---

## What is Snowpark Connect for Spark?

Snowpark Connect leverages the decoupled client-server architecture introduced
in Apache Spark 3.4 (Spark Connect). Your PySpark code runs locally as a
thin client while Snowflake executes the actual workload on its warehouse,
giving you Snowflake governance, security, and scalability with familiar
PySpark APIs.

---

## Prerequisites

| Requirement | Details |
|---|---|
| **Python** | 3.10 – 3.12 |
| **Java** | Same architecture as Python (e.g. both arm64) |
| **Snowflake account** | With a warehouse, database, and schema |

---

## Quick Start

### 1. Create & activate a virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 2. Install dependencies

```bash
pip install --upgrade --force-reinstall 'snowpark-connect[jdk]'
```

Or use the provided file:

```bash
pip install -r requirements.txt
```

### 3. Configure Snowflake connection

Copy the template and fill in your credentials:

```bash
mkdir -p ~/.snowflake
cp connections.toml.template ~/.snowflake/connections.toml
chmod 0600 ~/.snowflake/connections.toml
```

Edit `~/.snowflake/connections.toml`:

```toml
[spark-connect]
host = "<your_account>.snowflakecomputing.com"
account = "<your_account>"
user = "<your_user>"
password = "<your_password>"
warehouse = "<your_warehouse>"
database = "<your_database>"
schema = "public"
```

### 4. Run the example

**As a script:**

```bash
python snowpark_connect_hello_world.py
```

**As a Jupyter notebook:**

```bash
pip install jupyter
jupyter notebook snowpark_connect_hello_world.ipynb
```

---

## Files

| File | Description |
|---|---|
| `snowpark_connect_hello_world.ipynb` | Jupyter notebook — step-by-step walkthrough |
| `snowpark_connect_hello_world.py` | Standalone Python script — same logic |
| `connections.toml.template` | Template for Snowflake connection config |
| `requirements.txt` | Python dependencies |

---

## What the Example Covers

1. **Session init** — `snowflake.snowpark_connect.server.init_spark_session()`
2. **DataFrame creation** — `spark.createDataFrame()`
3. **Filtering** — `df.filter()`
4. **Sorting** — `df.orderBy()`
5. **Aggregations** — `df.groupBy().agg()`
6. **Column transforms** — `df.withColumn()`
7. **Spark SQL** — `spark.sql()`
8. **(Optional) Reading a Snowflake table** — `spark.read.table()`

---

## Reference

- [Snowpark Connect for Spark Overview](https://docs.snowflake.com/en/developer-guide/snowpark-connect/snowpark-connect-overview)
- [Run Spark workloads from VS Code / Jupyter / Terminal](https://docs.snowflake.com/en/developer-guide/snowpark-connect/snowpark-connect-workloads-jupyter)
- [Intro to Snowpark Connect for Spark (Guide)](https://www.snowflake.com/en/developers/guides/intro-to-snowpark-connect-for-apache-spark/)

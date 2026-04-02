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
| **Snowflake account** | With a warehouse, database, and schema |

> **Note:** Java is required by PySpark, but the `snowpark-connect[jdk]` package
> bundles a compatible JDK automatically — no separate Java install needed.

---

## Quick Start

### 1. Create & activate a virtual environment

```bash
python3 -m venv snowpark_connect_pyspark_env
source snowpark_connect_pyspark_env/bin/activate
```

### 2. Install dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

> **Important:** Do NOT install `pyspark` separately. The `snowpark-connect[jdk]`
> package in `requirements.txt` pulls the correct compatible versions of `pyspark`,
> `protobuf`, `zstandard`, and all other transitive dependencies automatically.
> Installing `pyspark` independently can cause protobuf version conflicts.

### 3. Configure Snowflake connection

Copy the template and fill in your credentials:

```bash
mkdir -p ~/.snowflake
cp connections.toml.template ~/.snowflake/connections.toml
chmod 0600 ~/.snowflake/connections.toml
```

If you already have a `~/.snowflake/connections.toml`, add the `[spark-connect]`
section from the template to your existing file instead of overwriting it.

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

### 5. Deactivate the virtual environment (when done)

```bash
deactivate
```

---

## How the Connection Works

There is no explicit connection string or credential passing in the Python code.
The connection is established via **convention-based configuration**:

1. `init_spark_session()` automatically reads `~/.snowflake/connections.toml`
2. It looks for the `[spark-connect]` section by name
3. It authenticates with Snowflake using the credentials in that section
4. It starts a Spark Connect server on Snowflake's infrastructure
5. It returns a standard PySpark `SparkSession` connected to the remote server

```
~/.snowflake/connections.toml         snowpark_connect_hello_world.py
┌──────────────────────────┐          ┌───────────────────────────────┐
│ [spark-connect]          │          │                               │
│ host = "acme.snow..."    │◄─────────│ init_spark_session()          │
│ account = "acme"         │  reads   │   (auto-discovers the TOML)  │
│ user = "bob"             │  auto-   │                               │
│ password = "***"         │  mati-   │ Returns: SparkSession ───────►│
│ warehouse = "WH1"        │  cally   │                               │
│ database = "DB1"         │          │ spark.sql(), df.filter(), ... │
└──────────────────────────┘          └───────────────────────────────┘
```

The environment variable `SPARK_CONNECT_MODE_ENABLED=1` (set in the script)
tells PySpark to route all operations through the Spark Connect protocol
to Snowflake rather than running them locally.

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

## Files

| File | Description |
|---|---|
| `snowpark_connect_hello_world.py` | Standalone Python script |
| `snowpark_connect_hello_world.ipynb` | Jupyter notebook — step-by-step walkthrough |
| `connections.toml.template` | Template for Snowflake connection config |
| `requirements.txt` | Python dependencies |
| `commands.txt` | Step-by-step setup instructions (plain text) |

---

## Troubleshooting

| Problem | Solution |
|---|---|
| `protobuf` version conflict | Do not install `pyspark` separately — let `snowpark-connect[jdk]` manage it. If already broken, delete the venv and recreate it. |
| `zstandard` not found | Should be installed automatically. If missing: `pip install zstandard` |
| `ModuleNotFoundError: No module named 'snowflake'` | Ensure the venv is activated: `source snowpark_connect_pyspark_env/bin/activate` |
| Connection error at runtime | Verify `~/.snowflake/connections.toml` has a `[spark-connect]` section with valid credentials |

---

## Useful Commands

```bash
# Check installed snowpark-connect version
pip show snowpark-connect

# Check all installed packages
pip list

# Verify Python version
python3 --version
```

---

## Reference

- [Snowpark Connect for Spark Overview](https://docs.snowflake.com/en/developer-guide/snowpark-connect/snowpark-connect-overview)
- [Run Spark workloads from VS Code / Jupyter / Terminal](https://docs.snowflake.com/en/developer-guide/snowpark-connect/snowpark-connect-workloads-jupyter)
- [Intro to Snowpark Connect for Spark (Guide)](https://www.snowflake.com/en/developers/guides/intro-to-snowpark-connect-for-apache-spark/)

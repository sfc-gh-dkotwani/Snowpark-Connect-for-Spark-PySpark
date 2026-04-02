"""
Snowpark Connect for Spark — PySpark Hello World

Demonstrates running PySpark DataFrame operations on Snowflake's compute engine
via Snowpark Connect for Apache Spark. No Spark cluster required.

Prerequisites:
  - Python 3.10+ (< 3.13), Java (same arch as Python)
  - pip install --upgrade --force-reinstall 'snowpark-connect[jdk]'
  - A [spark-connect] connection in ~/.snowflake/connections.toml
"""

import os

from snowflake import snowpark_connect
import pyspark
import pyspark.sql.functions as F
import snowflake
from snowflake.snowpark_connect.resources_initializer import wait_for_resource_initialization
from pyspark.sql import Row

os.environ["SPARK_CONNECT_MODE_ENABLED"] = "1"


def main():
    # ------------------------------------------------------------------ #
    # 1. Initialize Spark Session via Snowpark Connect
    # ------------------------------------------------------------------ #
    spark = snowflake.snowpark_connect.server.init_spark_session()
    print(f"Spark version : {spark.version}")
    print("Snowpark Connect session initialized successfully!\n")

    # ------------------------------------------------------------------ #
    # 2. Create a DataFrame from in-memory data
    # ------------------------------------------------------------------ #
    df = spark.createDataFrame([
        Row(id=1, name="Alice",   department="Engineering", salary=95000),
        Row(id=2, name="Bob",     department="Marketing",   salary=72000),
        Row(id=3, name="Charlie", department="Engineering", salary=105000),
        Row(id=4, name="Diana",   department="Sales",       salary=68000),
        Row(id=5, name="Eve",     department="Engineering", salary=110000),
    ])

    print("--- Schema ---")
    df.printSchema()

    print("--- All Rows ---")
    df.show()

    # ------------------------------------------------------------------ #
    # 3. Basic DataFrame operations
    # ------------------------------------------------------------------ #
    print(f"Total row count: {df.count()}\n")

    print("--- Engineering department only ---")
    df.filter(F.col("department") == "Engineering").show()

    print("--- Sorted by salary (desc) ---")
    df.orderBy(F.col("salary").desc()).show()

    # ------------------------------------------------------------------ #
    # 4. Aggregations
    # ------------------------------------------------------------------ #
    print("--- Average salary by department ---")
    df.groupBy("department").agg(
        F.avg("salary").alias("avg_salary"),
        F.count("*").alias("headcount"),
    ).orderBy("department").show()

    # ------------------------------------------------------------------ #
    # 5. Column transformations
    # ------------------------------------------------------------------ #
    print("--- With 10% bonus column ---")
    df.withColumn("bonus", F.col("salary") * 0.10).show()

    # ------------------------------------------------------------------ #
    # 6. Spark SQL
    # ------------------------------------------------------------------ #
    df.createOrReplaceTempView("employees")

    print("--- Spark SQL aggregation ---")
    spark.sql("""
        SELECT department,
               COUNT(*)       AS headcount,
               SUM(salary)    AS total_salary,
               MAX(salary)    AS max_salary
        FROM employees
        GROUP BY department
        ORDER BY total_salary DESC
    """).show()

    # ------------------------------------------------------------------ #
    # 7. (Optional) Read a Snowflake table
    # ------------------------------------------------------------------ #
    # Uncomment and update the table name to try reading from Snowflake:
    #
    # sales_table = "my_database.public.my_table"
    # sales = spark.read.table(sales_table)
    # sales.show()
    # sales.filter(sales["col1"] != "somevalue").show()

    # ------------------------------------------------------------------ #
    # 8. Stop the Spark session
    # ------------------------------------------------------------------ #
    spark.stop()
    print("Spark session stopped.")


if __name__ == "__main__":
    main()

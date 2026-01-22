from pyspark.sql import SparkSession
from trino.dbapi import connect
import pandas as pd
import os

import boto3

# Global Spark Session
spark = None

def init_s3_bucket():
    """Ensure the 'warehouse' bucket exists in Ozone."""
    try:
        s3 = boto3.client(
            "s3",
            endpoint_url=os.getenv("OZONE_S3_ENDPOINT", "http://ozone-om:9862"),
            aws_access_key_id="any",
            aws_secret_access_key="any",
            region_name="us-east-1"
        )
        s3.create_bucket(Bucket="warehouse")
        print("S3 Bucket 'warehouse' created or verified.")
    except Exception as e:
        print(f"Warning: Could not create S3 bucket: {e}")

def init_spark():
    global spark
    if spark is None:
        print("Initializing S3...")
        init_s3_bucket()
        
        print("Starting Spark Session...")
        # Note: We need to ensure the Spark Driver connects to the Master
        # and has necessary Iceberg/S3 packages.
        spark = SparkSession.builder \
            .appName("LakeEngineAPI") \
            .master(os.getenv("SPARK_MASTER", "local[*]")) \
            .config("spark.jars.packages", "org.apache.iceberg:iceberg-spark-runtime-3.5_2.12:1.4.2,org.apache.hadoop:hadoop-aws:3.3.4") \
            .config("spark.sql.extensions", "org.apache.iceberg.spark.extensions.IcebergSparkSessionExtensions") \
            .config("spark.sql.catalog.iceberg", "org.apache.iceberg.spark.SparkCatalog") \
            .config("spark.sql.catalog.iceberg.type", "hive") \
            .config("spark.sql.catalog.iceberg.uri", "thrift://hive-metastore:9083") \
            .config("spark.sql.catalog.iceberg.s3.endpoint", os.getenv("OZONE_S3_ENDPOINT", "http://ozone-om:9862")) \
            .config("spark.sql.catalog.iceberg.warehouse", "s3a://warehouse/") \
            .config("spark.hadoop.fs.s3a.endpoint", os.getenv("OZONE_S3_ENDPOINT", "http://ozone-om:9862")) \
            .config("spark.hadoop.fs.s3a.access.key", "any") \
            .config("spark.hadoop.fs.s3a.secret.key", "any") \
            .config("spark.hadoop.fs.s3a.path.style.access", "true") \
            .config("spark.hadoop.fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem") \
            .config("spark.sql.defaultCatalog", "iceberg") \
            .getOrCreate()
        print("Spark Session Created.")

def ingest_file(table_name: str, file_path: str, file_name: str):
    global spark
    if not spark: init_spark()

    # Determine format
    fmt = "csv"
    if file_name.endswith(".json"): fmt = "json"
    elif file_name.endswith(".parquet"): fmt = "parquet"

    print(f"Reading {fmt} from {file_path}")
    df = spark.read.format(fmt).option("header", "true").option("inferSchema", "true").load(file_path)
    
    # Write to Iceberg
    full_table_name = f"iceberg.default.{table_name}"
    
    # Check if table exists
    try:
        # Create table if not exists (simple strategy)
        df.writeTo(full_table_name).createOrReplace()
        action = "Created/Replaced"
    except Exception as e:
        # Append
        df.writeTo(full_table_name).append()
        action = "Appended"
    
    return f"Successfully {action} data into {full_table_name}"

def run_trino_query(sql: str):
    conn = connect(
        host=os.getenv("TRINO_HOST", "trino"),
        port=8080,
        user="python",
        catalog="iceberg",
        schema="default"
    )
    cur = conn.cursor()
    cur.execute(sql)
    rows = cur.fetchall()
    columns = [desc[0] for desc in cur.description]
    return [dict(zip(columns, row)) for row in rows]

def perform_upsert(table_name: str, records: list, primary_key: str):
    global spark
    if not spark: init_spark()
    
    full_table_name = f"iceberg.default.{table_name}"
    
    # Create a DataFrame from the incoming records
    updates_df = spark.createDataFrame(pd.DataFrame(records))
    updates_df.createOrReplaceTempView("updates")
    
    # Perform Merge
    merge_sql = f"""
    MERGE INTO {full_table_name} t
    USING updates s
    ON t.{primary_key} = s.{primary_key}
    WHEN MATCHED THEN UPDATE SET *
    WHEN NOT MATCHED THEN INSERT *
    """
    
    spark.sql(merge_sql)
    return len(records)

def list_snapshots(table_name: str):
    global spark
    if not spark: init_spark()
    full_table_name = f"iceberg.default.{table_name}"
    # Iceberg metadata table
    # history: made_current_at, snapshot_id, parent_id, is_current_ancestor
    df = spark.read.format("iceberg").load(f"{full_table_name}.history")
    return [row.asDict() for row in df.collect()]

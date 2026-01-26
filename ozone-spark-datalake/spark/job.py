from pyspark.sql import SparkSession
import os

def main():
    # Initialize Spark Session
    spark = SparkSession.builder \
        .appName("OzoneBatchProcess") \
        .getOrCreate()

    print(">>> Spark Session Created")

    # Access parameters
    # Note: We use specific hostname 'ozone-om' as defined in docker-compose
    ozone_om_address = "ozone-om:9862"
    bucket_path = f"ofs://{ozone_om_address}/datalake"

    # Define paths
    input_path = f"{bucket_path}/raw/input.csv"
    output_path = f"{bucket_path}/processed/summary"

    print(f">>> Reading data from: {input_path}")
    
    # Read CSV
    df = spark.read.csv(input_path, header=True, inferSchema=True)
    
    print(">>> Input Schema:")
    df.printSchema()
    df.show()

    # Transformation: Calculate total amount per category
    print(">>> Performing Transformation: Group By Category")
    processed_df = df.groupBy("category").sum("amount").withColumnRenamed("sum(amount)", "total_amount")

    print(">>> Output Preview:")
    processed_df.show()

    # Write Output
    print(f">>> Writing data to: {output_path}")
    processed_df.write.mode("overwrite").csv(output_path, header=True)

    print(">>> Job Completed Successfully")
    spark.stop()

if __name__ == "__main__":
    main()

# Understanding the Architecture

## What problem are we solving?
We are building a "Data Lakehouse" prototype. Traditional Data Lakes (just dumping files in S3) are messy, unreliable, and hard to query. Traditional Databases (like Postgres) are expensive to scale for massive analytical workloads. We are solving the "Middle Ground" problem: How do we get the cheap, massive storage of a Data Lake with the reliability and usability (ACID, SQL, CRUD) of a Database? This prototype demonstrates that architecture locally.

## Why not PostgreSQL?
PostgreSQL is amazing, but it's primarily a "Scale-Up" Mono-lithic architecture optimized for Transactions (OLTP) - inserting single rows very fast.
1.  **Storage Coupling**: In Postgres, storage and compute are tied together on the same machine (mostly). In our Lake, Storage (Ozone) and Compute (Spark/Trino) are separate. We can scale them independently.
2.  **Analytics Performance**: Postgres is Row-Oriented. Analytical queries want Column-Oriented data (like Parquet/Iceberg) to scan millions of records fast.
3.  **Cost**: Storing terabytes in Block Storage (disk) is expensive. Object Storage (Ozone/S3) is cheap.

## Why Iceberg?
Before Iceberg, Data Lakes were just folders of files. If you were writing a file while someone was reading, they might crash or see partial data.
Iceberg acts as a **Table Layer** over those files.
1.  **ACID Transactions**: It guarantees that you either see the whole update or none of it. No partial reads.
2.  **Time Travel**: You can query "What did this table look like yesterday?".
3.  **Schema Evolution**: You can add/rename columns without rewriting all the data (which you can't easily do in raw CSV/Parquet).

## Why Spark writes, Trino reads?
It's about "Best Tool for the Job":
*   **Spark (The Heavy Lifter)**: Spark is designed for massive, complex batch processing (ETL). Implementing complex logic for merging updates (MERGE INTO) and rewriting data files is what Spark is best at. Writing data is efficient but "Startup time" is slow.
*   **Trino (The Speedster)**: Trino (formerly PrestoSQL) is designed purely for **Querying**. It's useless for complex ETL logic, but it's incredibly fast at reading. It keeps workers hot and ready to return SQL results in milliseconds/seconds, whereas Spark might take seconds just to start the job.

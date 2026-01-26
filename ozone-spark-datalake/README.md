# Ozone-Spark Data Lake (Simple)

A production-ready, minimal example of using Apache Ozone as a storage backend for Apache Spark batch processing.

## Structure

*   **`docker-compose.yml`**: Defines the `ozone` (Storage) and `spark` (Compute) services.
*   **`data/`**: Configuration and raw data.
*   **`spark/`**: Spark Python job (`job.py`).
*   **`scripts/`**: Helper scripts for ingestion and execution.

## Prerequisites

*   Docker && Docker Compose
*   (On Windows) PowerShell or Git Bash to run scripts.

## Quick Start

### 1. Start the Environment
Run Docker Compose in detached mode:
```bash
docker-compose up -d
```
*Wait about 30 seconds for Ozone to fully initialize and exit safe mode.*

### 2. Ingest Data
This script creates the `datalake` volume, `raw` and `processed` buckets, and uploads the sample CSV.
```bash
cd scripts
bash ingest.sh
```

### 3. Run Spark Job
This script submits the Spark job to the spark container. It automatically locates the required Ozone filesystem JAR.
```bash
bash run_spark.sh
```

### 4. Verify Outcome
The `run_spark.sh` script will list the output files at the end. You should see `_SUCCESS` and part files in `ofs://ozone/datalake/processed/summary`.

## How It Works

1.  **Shared libs**: We use a Docker Volume (`ozone_libs`) to share the `ozone-filesystem-hadoop3.jar` from the Ozone container to the Spark container.
2.  **OFS Protocol**: Spark connects using the `ofs://` protocol (Ozone File System).
3.  **Networking**: Both containers share a Docker network `lake_net` so Spark can talk to Ozone Manager on port `9862`.

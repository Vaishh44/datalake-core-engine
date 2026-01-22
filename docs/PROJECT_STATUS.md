# Project Status & Deployment Guide

## 1. What have we done so far?
We have built a **fully functional "Mini-Data Lake"**. It is not just a diagram; it is running code.
*   **The Foundation**: We set up Apache Ozone (Storage), Hive Metastore (Catalog), Postgres, Spark, and Trino using Docker.
*   **The Brain (API)**: We built a custom Python API (`api/`) that abstracts away the complexity. You don't need to run complex Spark commands manually; you just hit an endpoint.
*   **The Logic**:
    *   **Ingestion**: Takes a CSV/JSON, spins up a Spark job, and writes it as an **Iceberg** table.
    *   **Querying**: Connects to Trino to let you run fast SQL queries on those files.
    *   **Upserts (ACID)**: Implemented the "Hard Part" — updating a single row in a massive dataset using Spark's `MERGE INTO` command.
    *   **Time Travel**: Exposed Iceberg's history feature so you can see previous versions of data.

## 2. What is Pending?
In terms of the original scope (Protoype), **nothing technical is pending**. The code is complete.
However, for a *Production* or *Remote Server* Usage:
*   **Security**: Currently, there is NO authentication. Anyone with the IP can query/delete data.
*   **Persistence**: The `docker-compose.yml` uses named volumes. If you delete them (`docker-compose down -v`), you lose data. In production, you'd map these to real host directories.
*   **Resource Tuning**: We are using default configs. On a heavy load, Spark might crash with "Out of Memory".

## 3. Running on Ubuntu (Termius) - What to Understand
Since you are moving this to a remote Ubuntu server, here are the critical things to know:

### Resource Requirements (CRITICAL)
This stack is **Heavy**. It runs multiple Java Virtual Machines (JVMs).
*   **Minimum RAM**: 8GB (It might struggle).
*   **Recommended RAM**: 16GB+.
*   **CPU**: 4+ Cores recommended.
*   If your server is small (e.g., AWS t2.micro), **it will not work**. The containers will get killed by the OOM Killer.

### Deployment Steps
1.  **Copy Files**: Upload the entire `datalake_core_engine` folder to your Ubuntu server (e.g., using SFTP in Termius).
2.  **Install Docker**: Ensure `docker` and `docker-compose` are installed on Ubuntu.
3.  **Run**:
    ```bash
    cd datalake_core_engine
    sudo docker-compose up --build -d
    ```
4.  **Wait**: It takes ~2 minutes for everything to start. Use `docker logs -f spark-master` or `docker logs -f lake-api` to check progress.

### Connectivity
*   If you run `test_flow.py` **ON the server**: It works out of the box (uses `localhost`).
*   If you run `test_flow.py` **FROM your laptop**:
    *   You need to change the API URL:
        ```bash
        export API_URL="http://<YOUR_UBUNTU_IP>:8000"
        python test_flow.py
        ```
    *   **Important**: You must ensure port `8000` (API) is open in your server's firewall (AWS Security Group / UFW).

### Troubleshooting
*   **"Connection Refused"**: The API hasn't started yet. Wait longer.
*   **"Exit Code 137"**: This means "Out of Memory". Your server uses too much RAM. You might need to add Swap space or get a bigger server.

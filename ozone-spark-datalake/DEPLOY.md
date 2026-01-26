# Deployment Instructions (Git Workflow)

These steps describe how to deploy the `ozone-spark-datalake` project to your Ubuntu server using Git.

## 1. Connect to Server
Log in to your Ubuntu server using Termius or SSH.

## 2. Clone the Repository
Clone the repository to your server.
*Note: Replace `<repo-url>` with your actual repository URL.*

```bash
# 1. Clone the repo
git clone https://github.com/Vaishh44/datalake-core-engine.git

# 2. Navigate to the project folder
cd datalake-core-engine/ozone-spark-datalake
```

## 3. Run the Project
Now follow the standard start-up procedure.

```bash
# 1. Ensure scripts are executable (and fix potential line-ending issues)
chmod +x scripts/*.sh
sed -i 's/\r$//' scripts/*.sh

# 2. Start Docker Containers
docker compose up -d

# 3. Wait 30s for Ozone to initialize...
echo "Waiting 30s for services..."
sleep 30

# 4. Ingest Data (Creates volume/bucket & uploads CSV)
./scripts/ingest.sh

# 5. Run Spark Job
./scripts/run_spark.sh
```

## 4. Troubleshooting
*   **"Ozone filesystem JAR not found"**: Ensure the `ozone` container is running and healthy. The volume should populate automatically.
*   **"Connection refused"**: If `run_spark.sh` fails to connect to Ozone, check if `ozone` container is healthy: `docker ps`.
*   **"bad interpreter: No such file or directory"**: This usually means Windows line endings (`\r\n`) got into the scripts. Run the `sed -i 's/\r$//' scripts/*.sh` command again.

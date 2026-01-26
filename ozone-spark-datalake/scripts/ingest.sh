#!/bin/bash
set -e

echo "=========================================="
echo " Ingesting Data into Apache Ozone Lake    "
echo " (Distributed SCM/OM/DN Setup)            "
echo "=========================================="

# 1. Initialize Ozone services (SCM & OM)
# We use '|| true' because they might fail if already initialized
echo "[INFO] Initializing SCM..."
docker exec ozone-scm ozone scm --init || true

echo "[INFO] Initializing OM..."
docker exec ozone-om ozone om --init || true

# 2. Restart services to apply initialization if needed
# (Optional, but good practice if init was fresh. Using compose restart can be heavy, 
#  so we rely on the fact that usually these commands work on running containers or we accept a manual restart if needed.
#  However, for this script, we assume they are running. 
#  If init happened, the process inside might need a kick, but typically 'ozone scm' entrypoint handles it.
#  A more robust way is to just proceed and wait.)

# 3. Wait for Readiness
echo "[INFO] Waiting for OM Safe Mode exit..."
# Retry loop
until docker exec ozone-om ozone admin safemode status | grep -q "out of safe mode"; do
  echo "  Waiting for Safe Mode exit..."
  sleep 5
done

# 4. Create Volume (if not exists)
echo "[INFO] Creating Volume 'datalake'..."
docker exec ozone-om ozone sh volume create /datalake || true

# 5. Create Buckets
echo "[INFO] Creating Bucket 'raw'..."
docker exec ozone-om ozone sh bucket create /datalake/raw || true

echo "[INFO] Creating Bucket 'processed'..."
docker exec ozone-om ozone sh bucket create /datalake/processed || true

# 6. Upload Data
echo "[INFO] Uploading input.csv..."
# Copy to OM container tmp
docker cp ../data/input.csv ozone-om:/tmp/input.csv

# Put into Ozone FS
docker exec ozone-om ozone fs -put -f /tmp/input.csv ofs://ozone-om/datalake/raw/input.csv

echo "[SUCCESS] Data Ingestion Complete."
echo "Verified File List:"
docker exec ozone-om ozone fs -ls ofs://ozone-om/datalake/raw/

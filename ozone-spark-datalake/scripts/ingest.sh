#!/bin/bash
set -e

echo "======================================="
echo " Ingesting Data into Apache Ozone Lake "
echo "======================================="

# 1. Wait for Ozone to be ready
echo "[INFO] Waiting for Ozone Manager..."
until docker exec ozone ozone admin safemode status | grep -q "out of safe mode"; do
  echo "  Waiting for Safe Mode exit..."
  sleep 5
done

# 2. Create Volume and Buckets
echo "[INFO] Creating Volume 'datalake'..."
# Ignore error if exists
docker exec ozone ozone sh volume create /datalake || true

echo "[INFO] Creating Bucket 'raw'..."
docker exec ozone ozone sh bucket create /datalake/raw || true

echo "[INFO] Creating Bucket 'processed'..."
docker exec ozone ozone sh bucket create /datalake/processed || true

# 3. Upload Data
echo "[INFO] Uploading input.csv..."
# Copy from host to container tmp
docker cp ../data/input.csv ozone:/tmp/input.csv

# Put into Ozone FS
docker exec ozone ozone fs -put -f /tmp/input.csv ofs://ozone/datalake/raw/input.csv

echo "[SUCCESS] Data Ingestion Complete."
echo "Verified File List:"
docker exec ozone ozone fs -ls ofs://ozone/datalake/raw/

#!/bin/bash
set -e

echo "=========================================="
echo " Running Spark Job on Ozone (Distributed) "
echo "=========================================="

# 1. Check Spark container
if ! docker ps | grep -q spark; then
  echo "[ERROR] Spark container is not running."
  echo "        Run: docker compose up -d"
  exit 1
fi

# 2. Locate Ozone filesystem JAR inside Spark container
# The path might differ slightly in apache/ozone vs others, but we mapped it to /opt/ozone-libs
echo "[INFO] Locating Ozone filesystem JAR..."

JAR_PATH=$(docker exec spark find /opt/ozone-libs -type f -name "*ozone-filesystem*jar" | head -n 1)

if [ -z "$JAR_PATH" ]; then
  echo "[ERROR] Ozone filesystem JAR not found in /opt/ozone-libs."
  echo "        Ensure Ozone containers are running and volume is mounted."
  exit 1
fi

echo "[INFO] Found Ozone JAR: $JAR_PATH"

# 3. Submit Spark Job
echo "[INFO] Submitting Spark job..."

docker exec spark /opt/spark/bin/spark-submit \
  --master local[*] \
  --jars "$JAR_PATH" \
  --conf spark.hadoop.fs.ofs.impl=org.apache.hadoop.fs.ozone.OzoneFileSystem \
  --conf spark.hadoop.fs.AbstractFileSystem.ofs.impl=org.apache.hadoop.fs.ozone.OzoneFS \
  --conf spark.hadoop.fs.defaultFS=ofs://ozone-om/ \
  --conf spark.hadoop.ozone.om.address=ozone-om:9862 \
  /app/job.py

echo "=========================================="
echo " Spark Job Completed Successfully         "
echo "=========================================="

# 4. Verify Output
echo "[INFO] Verifying processed data in Ozone..."
docker exec ozone-om ozone fs -ls -R ofs://ozone-om/datalake/processed/

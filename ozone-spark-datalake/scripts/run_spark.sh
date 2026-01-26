#!/bin/bash
set -e

echo "=========================================="
echo " Running Spark Job on Apache Ozone Lake   "
echo "=========================================="

# 1. Check Spark container
if ! docker ps | grep -q spark; then
  echo "[ERROR] Spark container is not running."
  echo "        Run: docker compose up -d"
  exit 1
fi

# 2. Locate Ozone filesystem JAR inside Spark container
echo "[INFO] Locating Ozone filesystem JAR..."

JAR_PATH=$(docker exec spark find /opt/ozone-libs -type f -name "*ozone-filesystem*jar" | head -n 1)

if [ -z "$JAR_PATH" ]; then
  echo "[ERROR] Ozone filesystem JAR not found."
  echo "        Expected under /opt/ozone-libs"
  exit 1
fi

echo "[INFO] Found Ozone JAR: $JAR_PATH"

# 3. Submit Spark job
echo "[INFO] Submitting Spark job..."

docker exec spark spark-submit \
  --master local[*] \
  --jars "$JAR_PATH" \
  --conf spark.hadoop.fs.ofs.impl=org.apache.hadoop.fs.ozone.OzoneFileSystem \
  --conf spark.hadoop.fs.AbstractFileSystem.ofs.impl=org.apache.hadoop.fs.ozone.OzoneFS \
  --conf spark.hadoop.fs.defaultFS=ofs://ozone/ \
  --conf spark.hadoop.ozone.om.address=ozone:9862 \
  /app/job.py

echo "=========================================="
echo " Spark Job Completed Successfully         "
echo "=========================================="

# 4. Verify output
echo "[INFO] Verifying processed data in Ozone..."
docker exec ozone ozone fs -ls -R ofs://ozone/datalake/processed/

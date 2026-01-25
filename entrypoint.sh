#!/bin/bash
set -e

echo "======================================"
echo " Starting Apache Ozone All-In-One "
echo "======================================"

# 1. Initialize SCM
if [ ! -f "/data/metadata/scm/current/VERSION" ]; then
    echo "[INIT] Initializing SCM..."
    ozone scm --init
else
    echo "[INIT] SCM already initialized."
fi

# 2. Initialize OM
if [ ! -f "/data/metadata/om/current/VERSION" ]; then
    echo "[INIT] Initializing OM..."
    ozone om --init
else
    echo "[INIT] OM already initialized."
fi

# 3. Start SCM
echo "[START] Starting SCM..."
ozone scm --daemon start

# 4. Start OM
echo "[START] Starting OM..."
ozone om --daemon start

# 5. Start Datanode
echo "[START] Starting Datanode..."
ozone datanode --daemon start

# 6. Wait for SCM Safe Mode Exit
echo "[WAIT] Waiting for SCM to exit safe mode..."
until ozone admin safemode status | grep -q "out of safe mode"; do
    echo "   SCM still in safe mode..."
    sleep 5
done
echo "[READY] SCM is out of safe mode."

# 7. Wait for Pipeline Creation
echo "[WAIT] Waiting for pipeline creation..."
until ozone admin pipeline list | grep -q "RATIS"; do
    echo "   No pipeline yet..."
    sleep 5
done
echo "[READY] Pipeline is created."

# 8. Start S3 Gateway
echo "[START] Starting S3 Gateway..."
ozone s3g --daemon start

# 9. Keep Container Alive
echo "[DONE] Ozone All-In-One is READY."
tail -f /dev/null

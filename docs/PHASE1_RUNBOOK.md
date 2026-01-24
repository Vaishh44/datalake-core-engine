# Phase 1 – Apache Ozone Verification

This runbook details the process to verify the Phase 1 Single-Container Ozone setup.
We use a **Unified Docker Container** that automatically initializes SCM, OM, Datanode, and S3 Gateway.

> **⚠️ WARNING**: Do **NOT** run manual `ozone scm --init` or `ozone om --init` commands inside the container. The entrypoint script handles this automatically. Manual intervention will break the state.

## 🚀 Steps to Run

Run these exact commands in order:

### 1. Start Ozone
```bash
docker-compose -f docker-compose.ozone.yml down
docker-compose -f docker-compose.ozone.yml up -d
```
*Wait ~30-60 seconds for the container to initialize and auto-create buckets.*

### 2. Prepare Python Environment
```bash
# If not already active
source venv/bin/activate  
pip install boto3
```

### 3. Run Verification
```bash
python verify_ozone.py
```

---

## ✅ Success Criteria
You must see the following success message:
> **✅ PHASE 1 COMPLETE: Ozone is working, S3 Gateway verified**

## 🌐 Connectivity
*   **Ozone UI**: [`http://localhost:9874`](http://localhost:9874)
*   **S3 Gateway**: [`http://localhost:9862`](http://localhost:9862)

If running on a remote server (Termius), ensure your SSH tunnel maps these ports correctly.

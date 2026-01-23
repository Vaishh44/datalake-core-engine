# Phase 1 – Apache Ozone Verification

This runbook details the process to verify the Phase 1 Single-Container Ozone setup.
We use a **Unified Docker Container** that automatically initializes SCM, OM, Datanode, and S3 Gateway.

## 🚀 Steps to Run

Run these exact commands in order:

### 1. Start Ozone
```bash
docker-compose -f docker-compose.ozone.yml up -d
```
*Wait ~30-60 seconds for the container to initialize and auto-create buckets.*

### 2. Prepare Python Environment
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install boto3
```

### 3. Run Verification
```bash
python verify_ozone.py
```

---

## ✅ Success Criteria
You must see the following success message:
> **✅ PHASE 1 COMPLETE: Ozone is working**

## 🌐 Connectivity
*   **Ozone UI**: `http://localhost:9874`
*   **S3 Gateway**: `http://localhost:9862`

If running on a remote server (Termius), use **SSH Tunneling** to map `localhost:9862` (local) to `localhost:9862` (remote) to run the script from your laptop.

# PHASE 1: OZONE RUNBOOK (STRICT)

This document describes how to start and verify **Apache Ozone** (standalone) on an Ubuntu server.
Scope: Ozone Only. No Spark/Trino/API.

## 1. Prerequisites
Ensure you have `docker`, `docker-compose`, and `python3` installed.

## 2. Setup Python Environment
Ubuntu enforces PEP-668, so we MUST use a virtual environment.

```bash
# 1. Install venv if missing
sudo apt-get update && sudo apt-get install -y python3-venv

# 2. Create virtual environment
python3 -m venv venv

# 3. Activate environment
source venv/bin/activate

# 4. Install dependency
pip install boto3
```

## 3. Start Apache Ozone
Run the Ozone-specific compose file.

```bash
# Start in background
docker-compose -f docker-compose.ozone.yml up -d

# Wait 60 seconds for initialization
sleep 60
```

**Verify Containers are Running:**
```bash
docker ps
```
You should see: `ozone-s3g`, `ozone-om`, `ozone-scm`, `ozone-datanode`.

- S3 Gateway: `localhost:9862`
- Ozone UI: `localhost:9878`

## 4. Run Verification
Execute the python script **from within your virtual environment**.

```bash
python verify_ozone.py
```

## 5. Success Criteria
You MUST see the following line at the bottom of the output:

> **✅ PHASE 1 COMPLETE: Ozone is working**

If you see `❌ FAILURE`, check logs:
```bash
docker logs ozone-s3g
docker logs ozone-om
```

## 6. Shutdown
When finished:
```bash
docker-compose -f docker-compose.ozone.yml down
```

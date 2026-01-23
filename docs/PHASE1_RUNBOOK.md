# Phase 1 – Apache Ozone Verification

This runbook details the **STRICT** process to verify Apache Ozone setup.
We use `ozone-runner` to run all services in a single container.

## Steps

### 1. Start Ozone
Start the single-node stack:
```bash
docker-compose -f docker-compose.ozone.yml up -d
```

### 2. Wait 60 seconds
Allow services to fully initialize.
```bash
sleep 60
```
*Check logs if needed:* `docker logs ozone`

### 3. Initialize Ozone (MANDATORY)
**You MUST perform this step manually.** 
Ozone S3 Gateway requires a volume layout mapping (s3v) to likely exist.

```bash
# Enter the container
docker exec -it ozone bash

# Create the specific volume for S3
ozone sh volume create s3v

# Create the bucket (Ozone side)
ozone sh bucket create s3v/phase1-test

# Exit the container
exit
```

### 4. Create Python venv
Ensure you are in a clean environment.

```bash
# Create and activate venv
python3 -m venv venv
source venv/bin/activate

# Install boto3
pip install boto3
```

### 5. Run Verification
Run the script which uses `UNSIGNED` authentication.

```bash
python verify_ozone.py
```

## Success Criteria
You must see the following success message at the end:

> **✅ PHASE 1 COMPLETE: Ozone is working**

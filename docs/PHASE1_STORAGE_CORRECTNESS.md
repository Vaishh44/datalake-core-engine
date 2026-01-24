# Phase 1: Ozone Storage Correctness Verification

This document checks if the Apache Ozone core storage (SCM, OM, Datanode) is functioning correctly **without** relying on S3, APIs, or external drivers.

## 1. Reset & Start Environment

Since we are enforcing strict replication, we must start with clean data.

```bash
# Stop existing containers
docker-compose -f docker-compose.ozone.yml down

# ⚠️ DELETE OLD DATA (CRITICAL)
# Run this from your project root (d:\datalake_core_engine or ~/projects/datalake-core-engine)
sudo rm -rf ozone-data

# Start the Native Ozone Container
docker-compose -f docker-compose.ozone.yml up -d
```

> **Wait 45 seconds** for the startup script to finish initializing services.

## 2. Verify Processes

Enter the container and check `jps`.

```bash
docker exec -it ozone-all-in-one bash

# Inside container:
jps
```
**Expected Output:**
- `StorageContainerManagerStarter`
- `OzoneManagerStarter`
- `HddsDatanodeService`
- `Jps`

*(Note: Gateway/S3G should NOT be present)*

## 3. Run Storage Validation (Ozone Shell)

Run these commands strictly inside the container:

### A. Create Volume
```bash
ozone sh volume create /vol1
```
*Expected: No error output.*

### B. Create Bucket
```bash
ozone sh bucket create /vol1/bucket1
```
*Expected: No error output.*

### C. Put Key (Upload)
Create a test file and upload it.
```bash
echo "Ozone Native Test Data" > /tmp/testfile.txt

ozone sh key put /vol1/bucket1/testkey /tmp/testfile.txt
```
*Expected: No error output.*

### D. List Keys
```bash
ozone sh key list /vol1/bucket1
```
*Expected: JSON output showing `testkey`.*

### E. Get Key (Download) & Verify
Download the key back to a new file and compare content.
```bash
ozone sh key get /vol1/bucket1/testkey /tmp/downloaded.txt

cat /tmp/downloaded.txt
```
**Expected Output:**
> Ozone Native Test Data

---
## ✅ Success Criteria
If you see "Ozone Native Test Data" printed at the end, Phase 1 is **COMPLETE**.
The core storage pipeline is working reliably.

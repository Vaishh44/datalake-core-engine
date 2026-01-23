# Phase 1 – Apache Ozone Verification

This runbook details the **STRICT** process to verify Apache Ozone setup.
We use a multi-container setup (SCM, OM, Datanode, S3G) to ensure all services run correctly.

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
*Check logs if needed:* `docker logs ozone-om`

### 3. Initialize Ozone (MANDATORY)
**You MUST perform this step manually.** 
Ozone S3 Gateway requires a volume layout mapping (s3v) to likely exist.

```bash
# Enter the OM container
docker exec -it ozone-om bash

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

---

## 🌐 Troubleshooting: "Localhost" Not Working?

If you are running this on a **Remote Server** (e.g., via Termius, AWS, VPS), clicking `http://localhost:9878` will NOT work because "localhost" refers to **your laptop**, not the server.

### Option A: Use Server API (If Ports Open)
Replace `localhost` with your server's public IP.
*   Example: `http://123.45.67.89:9878`
*   *Note: This requires port 9878 to be allowed in the firewall/security group.*

### Option B: Use SSH Tunneling (Recommended)
This maps the server's port to your local laptop safely.

**In Termius:**
1.  Go to **Ports** (or Tunnels).
2.  Add a **Local Rule**.
3.  Set **Source** (Local): `9878`
4.  Set **Destination** (Remote): `localhost:9878`
5.  Connect.

Now, opening `http://localhost:9878` on your laptop **WILL** show the Ozone UI.

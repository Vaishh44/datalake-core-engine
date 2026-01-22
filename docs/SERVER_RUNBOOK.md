# Server Deployment Runbook for Termius (Ubuntu)

Follow these exact steps on your Ubuntu server to deploy and verify the Data Lake Engine.

## Phase 1: Setup & Start

### 1. File Transfer
*   **Action**: Use Termius SFTP or `scp` to copy the `datalake_core_engine` folder from your Windows machine to the Ubuntu server (e.g., inside `/home/ubuntu/`).

### 2. Connect to Server
*   Open your Termius terminal/SSH session.

### 3. Install Docker (If not already installed)
Copy and paste this block to install Docker and Docker Compose:
```bash
sudo apt-get update
sudo apt-get install -y docker.io docker-compose
sudo usermod -aG docker $USER
# NOTE: You might need to logout and login again for the group change to take effect.
```

### 4. Start the Engine (Phase 1: Ozone Only)
Navigate to the folder and start the ozone services:

```bash
cd datalake_core_engine
make up-ozone
# OR manually: sudo docker-compose -f docker-compose.ozone.yml up -d
```

### 5. Check Status
Run this to see if all containers are "Up":
```bash
sudo docker-compose -f docker-compose.ozone.yml ps
```
**Expected Output**:
You should see `ozone-scm`, `ozone-om`, and `ozone-datanode` with State `Up`.

### 6. Wait for Initialization
Wait ~1 minute. You can check logs:
```bash
make logs-ozone
```

---

## Phase 2: Verification (Ozone Only)

### 1. Install Python Dependencies
```bash
sudo apt-get install -y python3-pip make
pip3 install boto3 requests
```

### 2. Run the Verification Script
```bash
make test-ozone
# OR: python3 verify_ozone.py
```

### 3. Expected Output
You should see:
```text
--- Phase 1: Ozone Verification ---
...
[4] Uploading 'ozone_test.txt' to Ozone...
    Success.
...
✅ PHASE 1 COMPLETE: Ozone is working...
```

## Phase 3: Full Stack (Do not run yet)
Only proceed here after Phase 1 is green.
```bash
# sudo docker-compose up --build -d
# python3 test_flow.py
```

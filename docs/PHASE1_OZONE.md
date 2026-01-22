# Phase 1: Apache Ozone Verification

This phase focuses STRICTLY on ensuring the storage layer (Apache Ozone) is running and accessible via the S3 Gateway.
No Spark, No Trino, No API.

## 1. Start Ozone Only
We use a special compose file that only starts Ozone services.

```bash
# Stop any existing containers
docker-compose down

# Start only Ozone
docker-compose -f docker-compose.ozone.yml up -d
```

**Wait ~30-60 seconds** for Ozone to initialize.

## 2. Install Dependencies (Python)
You need `boto3` to talk to the S3 Gateway.

```bash
pip install boto3
```

## 3. Run Verification
Run the verification script. It will:
1.  Connect to Ozone (S3 Sataway port 9862).
2.  Create a bucket named `phase1-test`.
3.  Upload a file.
4.  Download it back.
5.  Verify the content matches.

```bash
python verify_ozone.py
```

## 4. Expected Output

```text
--- Phase 1: Ozone Verification ---
Target: http://localhost:9862
[1] Connecting to S3 Gateway...
[2] Creating bucket 'phase1-test'...
    Success.
[3] Creating local test file 'ozone_test.txt'...
[4] Uploading 'ozone_test.txt' to Ozone...
    Success.
[5] Verifying file exists in bucket...
    Success: Found 'ozone_test.txt' in remote bucket.
[6] Downloading file back to 'downloaded_ozone_test.txt'...
    Success.
[7] Verifying content...
    Success: Content matches exactly.

✅ PHASE 1 COMPLETE: Ozone is working, S3 Gateway is active, Read/Write is confirmed.
```

## 5. Troubleshooting (Remote Server)
If running on Ubuntu/Termius:
1.  Ensure you opened port `9862` (S3 Gateway) if running script from laptop.
2.  Or run the script **on the server** (Recommended).

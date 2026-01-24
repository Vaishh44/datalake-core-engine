import boto3
import sys
import time
from botocore.config import Config
from botocore import UNSIGNED

# Configuration
OZONE_ENDPOINT = "http://localhost:9878"
BUCKET_NAME = "phase1-test"
FILE_NAME = "ozone_test.txt"
DOWNLOAD_FILE_NAME = "downloaded_ozone_test.txt"

def main():
    print("--------------------------------------------------")
    print("   PHASE 1: OZONE STORAGE VERIFICATION START      ")
    print("--------------------------------------------------")

    # 1. Initialize S3 Client
    print(f"[INIT] Connecting to Ozone S3 Gateway at {OZONE_ENDPOINT}...")
    try:
        s3 = boto3.client(
            "s3",
            endpoint_url=OZONE_ENDPOINT,
            aws_access_key_id="ozone",
            aws_secret_access_key="ozone",
            config=Config(signature_version=UNSIGNED), 
            region_name="us-east-1"
        )
    except Exception as e:
        print(f"❌ FAILURE: Connection setup failed. Error: {e}")
        sys.exit(1)

    # 2. Check/Create Bucket with Retry Logic
    print(f"[ACTION] Checking/Creating bucket '{BUCKET_NAME}'...")
    retries = 10
    bucket_ready = False
    
    for i in range(retries):
        try:
            s3.create_bucket(Bucket=BUCKET_NAME)
            print("   ✅ Bucket created via S3 API.")
            bucket_ready = True
            break
        except Exception as e:
            # If connection failed, we retry. If bucket exists, we proceed.
            msg = str(e)
            if "Connection refused" in msg or "EndpointConnectionError" in msg or "ClientError" not in msg:
                 # Assume these are transient startup issues
                 print(f"   ⏳ Attempt {i+1}/{retries}: Connection failing or retrying... ({msg})")
                 time.sleep(5)
            else:
                 # Likely "BucketAlreadyExists" or similar
                 print(f"   ℹ️ Bucket may already exist: {msg}")
                 bucket_ready = True
                 break

    if not bucket_ready:
        print(f"❌ FAILURE: Bucket '{BUCKET_NAME}' could not be created/verified.")
        sys.exit(1)

    # 3. Create Local File
    print(f"[ACTION] Creating local test file '{FILE_NAME}'...")
    try:
        with open(FILE_NAME, "w") as f:
            f.write("Apache Ozone Phase 1 Single-Container Verification Successful!")
        print("   ✅ Local file created.")
    except Exception as e:
        print(f"❌ FAILURE: Local file creation failed. Error: {e}")
        sys.exit(1)

    # 4. Upload File
    print(f"[ACTION] Uploading '{FILE_NAME}' to Ozone...")
    try:
        s3.upload_file(FILE_NAME, BUCKET_NAME, FILE_NAME)
        print("   ✅ File uploaded successfully.")
    except Exception as e:
        print(f"❌ FAILURE: Upload failed. Error: {e}")
        sys.exit(1)

    # 5. Download File
    print(f"[ACTION] Downloading file to '{DOWNLOAD_FILE_NAME}'...")
    try:
        s3.download_file(BUCKET_NAME, FILE_NAME, DOWNLOAD_FILE_NAME)
        print("   ✅ File downloaded successfully.")
    except Exception as e:
        print(f"❌ FAILURE: Download failed. Error: {e}")
        sys.exit(1)

    # 6. Verify Content
    print(f"[ACTION] Verifying content match...")
    try:
        with open(DOWNLOAD_FILE_NAME, "r") as f:
            content = f.read()
            expected = "Apache Ozone Phase 1 Single-Container Verification Successful!"
            if content == expected:
                print(f"   ✅ Content verified: '{content}'")
            else:
                print(f"❌ FAILURE: Content mismatch!")
                sys.exit(1)
    except Exception as e:
        print(f"❌ FAILURE: Verification failed. Error: {e}")
        sys.exit(1)

    # Cleanup
    try:
        import os
        if os.path.exists(FILE_NAME): os.remove(FILE_NAME)
        if os.path.exists(DOWNLOAD_FILE_NAME): os.remove(DOWNLOAD_FILE_NAME)
    except:
        pass

    print("\n✅ PHASE 1 COMPLETE: Ozone is working, S3 Gateway verified")

if __name__ == "__main__":
    main()

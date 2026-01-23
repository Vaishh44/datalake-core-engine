import boto3
import os
import sys
from botocore.config import Config

# Configuration
OZONE_ENDPOINT = "http://localhost:9862"
ACCESS_KEY = "ozone"  # Default test credentials as requested
SECRET_KEY = "ozone"
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
            aws_access_key_id=ACCESS_KEY,
            aws_secret_access_key=SECRET_KEY,
            config=Config(signature_version='s3v4'),
            region_name="us-east-1"
        )
    except Exception as e:
        print(f"❌ FAILURE: Connection setup failed. Error: {e}")
        sys.exit(1)

    # 2. Create Bucket
    print(f"[ACTION] Creating bucket '{BUCKET_NAME}'...")
    try:
        s3.create_bucket(Bucket=BUCKET_NAME)
        print("   ✅ Bucket created (or already exists).")
    except Exception as e:
        if "BucketAlreadyOwner" in str(e):
             print("   ⚠️ Bucket already exists.")
        else:
             print(f"❌ FAILURE: Create bucket failed. Error: {e}")
             sys.exit(1)

    # 3. Create Local File
    print(f"[ACTION] Creating local test file '{FILE_NAME}'...")
    try:
        with open(FILE_NAME, "w") as f:
            f.write("Apache Ozone Phase 1 Verification Successful!")
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
        if os.path.exists(DOWNLOAD_FILE_NAME):
            os.remove(DOWNLOAD_FILE_NAME)
        
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
            expected = "Apache Ozone Phase 1 Verification Successful!"
            if content == expected:
                print(f"   ✅ Content verified: '{content}'")
            else:
                print(f"❌ FAILURE: Content mismatch!")
                print(f"      Expected: '{expected}'")
                print(f"      Got:      '{content}'")
                sys.exit(1)
    except Exception as e:
        print(f"❌ FAILURE: Verification failed. Error: {e}")
        sys.exit(1)

    # Cleanup
    try:
        if os.path.exists(FILE_NAME): os.remove(FILE_NAME)
        if os.path.exists(DOWNLOAD_FILE_NAME): os.remove(DOWNLOAD_FILE_NAME)
    except:
        pass

    print("\n✅ PHASE 1 COMPLETE: Ozone is working")

if __name__ == "__main__":
    main()

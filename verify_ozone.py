import boto3
import os
import sys

# Configuration
# Note: When running locally, localhost:9862 is the S3 Gateway
# When running inside Docker Network, it would be ozone-om:9862
OZONE_ENDPOINT = os.getenv("OZONE_ENDPOINT", "http://localhost:9862")
ACCESS_KEY = "any"
SECRET_KEY = "any"
BUCKET_NAME = "phase1-test"
FILE_NAME = "ozone_test.txt"

def main():
    print(f"--- Phase 1: Ozone Verification ---")
    print(f"Target: {OZONE_ENDPOINT}")

    # 1. Connect
    print(f"[1] Connecting to S3 Gateway...")
    try:
        s3 = boto3.client(
            "s3",
            endpoint_url=OZONE_ENDPOINT,
            aws_access_key_id=ACCESS_KEY,
            aws_secret_access_key=SECRET_KEY,
            region_name="us-east-1"
        )
    except Exception as e:
        print(f"FAIL: Could not create boto3 client. {e}")
        sys.exit(1)

    # 2. Create Bucket
    print(f"[2] Creating bucket '{BUCKET_NAME}'...")
    try:
        s3.create_bucket(Bucket=BUCKET_NAME)
        print("    Success.")
    except Exception as e:
        if "BucketAlreadyOwner" in str(e):
            print("    Bucket already exists (OK).")
        else:
            print(f"FAIL: {e}")
            sys.exit(1)

    # 3. Create Test File
    print(f"[3] Creating local test file '{FILE_NAME}'...")
    with open(FILE_NAME, "w") as f:
        f.write("Hello Apache Ozone! This is Phase 1.")
    
    # 4. Upload File
    print(f"[4] Uploading '{FILE_NAME}' to Ozone...")
    try:
        s3.upload_file(FILE_NAME, BUCKET_NAME, FILE_NAME)
        print("    Success.")
    except Exception as e:
        print(f"FAIL: Upload failed. {e}")
        sys.exit(1)

    # 5. List Objects to Verify
    print(f"[5] Verifying file exists in bucket...")
    try:
        response = s3.list_objects_v2(Bucket=BUCKET_NAME)
        objects = [obj['Key'] for obj in response.get('Contents', [])]
        if FILE_NAME in objects:
            print(f"    Success: Found '{FILE_NAME}' in remote bucket.")
        else:
            print(f"FAIL: File not listed in bucket. Found: {objects}")
            sys.exit(1)
    except Exception as e:
        print(f"FAIL: List objects failed. {e}")
        sys.exit(1)

    # 6. Download File
    print(f"[6] Downloading file back to 'downloaded_{FILE_NAME}'...")
    try:
        s3.download_file(BUCKET_NAME, FILE_NAME, f"downloaded_{FILE_NAME}")
        print("    Success.")
    except Exception as e:
        print(f"FAIL: Download failed. {e}")
        sys.exit(1)

    # 7. Verify Content
    print(f"[7] Verifying content...")
    with open(f"downloaded_{FILE_NAME}", "r") as f:
        content = f.read()
        if content == "Hello Apache Ozone! This is Phase 1.":
            print("    Success: Content matches exactly.")
        else:
            print(f"FAIL: Content mismatch. Got: '{content}'")
            sys.exit(1)

    print("\n✅ PHASE 1 COMPLETE: Ozone is working, S3 Gateway is active, Read/Write is confirmed.")
    
    # Cleanup (Optional)
    # os.remove(FILE_NAME)
    # os.remove(f"downloaded_{FILE_NAME}")

if __name__ == "__main__":
    main()

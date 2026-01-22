import requests
import json
import time

import os

# Allow usage on remote server by setting API_URL env var
# e.g. export API_URL=http://your-server-ip:8000
API_URL = os.getenv("API_URL", "http://localhost:8000")

def wait_for_api():
    print("Waiting for API to come online...")
    for _ in range(30):
        try:
            r = requests.get(f"{API_URL}/")
            if r.status_code == 200:
                print("API is Online!")
                return
        except:
            pass
        time.sleep(2)
    print("API failed to start.")
    exit(1)

def main():
    wait_for_api()

    # 1. Ingest Data
    print("\n--- 1. Ingesting Data ---")
    csv_content = "id,name,score\n1,Alice,85\n2,Bob,90\n3,Charlie,78"
    files = {'file': ('students.csv', csv_content, 'text/csv')}
    r = requests.post(f"{API_URL}/ingest/students", files=files)
    print(r.json())
    
    # 2. Query Data (Trino)
    print("\n--- 2. Querying Data (Trino) ---")
    query = {"sql": "SELECT * FROM iceberg.default.students ORDER BY id"}
    r = requests.post(f"{API_URL}/query", json=query)
    print("Result:", r.json())

    # 3. Upsert (Update Bob's score)
    print("\n--- 3. Performing Upsert (Update Bob -> 95) ---")
    updates = [
        {"id": 2, "name": "Bob", "score": 95}, # Update
        {"id": 4, "name": "David", "score": 88} # Insert
    ]
    r = requests.post(f"{API_URL}/crud/upsert/students?primary_key=id", json=updates)
    print(r.json())

    # 4. Verify Update
    print("\n--- 4. Verifying Update (Trino) ---")
    r = requests.post(f"{API_URL}/query", json=query)
    data = r.json()['data']
    print("Result:", data)
    
    # Check Bob's score
    bob = next(row for row in data if row['id'] == 2)
    assert bob['score'] == 95, f"Bob's score should be 95, got {bob['score']}"
    print("Verification Successful: Bob's score updated.")

    # 5. Check Snapshots (Time Travel)
    print("\n--- 5. checking Snapshots (Time Travel) ---")
    r = requests.get(f"{API_URL}/snapshots/students")
    history = r.json()['history']
    print("Snapshots:", len(history))
    for h in history:
        print(f" - {h['made_current_at']} (ID: {h['snapshot_id']})")

if __name__ == "__main__":
    main()

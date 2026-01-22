from fastapi import FastAPI, UploadFile, File, HTTPException
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import engine
import os

app = FastAPI(title="Antigravity Data Lake Engine")

# Data Models
class QueryRequest(BaseModel):
    sql: str

class Record(BaseModel):
    data: Dict[str, Any]

@app.on_event("startup")
async def startup_event():
    print("Initializing Data Lake Engine...")
    engine.init_spark()

@app.get("/")
def health_check():
    return {"status": "online", "system": "Antigravity Lake Engine"}

@app.post("/ingest/{table_name}")
async def ingest_data(table_name: str, file: UploadFile = File(...)):
    """
    Ingest a CSV/JSON file into an Iceberg table.
    """
    try:
        # Save temp file
        file_location = f"/tmp/{file.filename}"
        with open(file_location, "wb") as f:
            f.write(await file.read())
        
        # Trigger Spark Job
        result = engine.ingest_file(table_name, file_location, file.filename)
        return {"status": "success", "details": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if os.path.exists(file_location):
            os.remove(file_location)

@app.post("/query")
def run_query(query: QueryRequest):
    """
    Run a SQL query via Trino (Fast Read).
    """
    try:
        data = engine.run_trino_query(query.sql)
        return {"data": data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/crud/upsert/{table_name}")
def upsert_record(table_name: str, records: List[Dict[str, Any]], primary_key: str):
    """
    Perform a MERGE operation (Upsert) via Spark.
    """
    try:
        count = engine.perform_upsert(table_name, records, primary_key)
        return {"status": "merged", "rows_affected": count}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/snapshots/{table_name}")
def get_snapshots(table_name: str):
    """
    List table history/snapshots (Time Travel).
    """
    try:
        history = engine.list_snapshots(table_name)
        return {"history": history}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

import pandas as pd
import json
import io
from azure.storage.blob import BlobServiceClient

AZURE_CONN = "<YOUR CONNECTION STRING>"

def main(blob: bytes):
    # Load raw CSV
    df = pd.read_csv(io.BytesIO(blob))

    # ---- DATA CLEANING ----
    df = df.dropna()
    df["Diet_type"] = df["Diet_type"].str.strip().str.lower()

    # Save cleaned data
    cleaned_csv = df.to_csv(index=False)

    blob_service = BlobServiceClient.from_connection_string(AZURE_CONN)

    cleaned_blob = blob_service.get_blob_client(
        container="data",
        blob="Cleaned_Diets.csv"
    )
    cleaned_blob.upload_blob(cleaned_csv, overwrite=True)

    # ---- RESULT CALCULATION ----
    results = {
        "diet_counts": df["Diet_type"].value_counts().to_dict(),
        "avg_calories": round(df["Calories"].mean(), 2),
        "total_recipes": len(df)
    }

    result_blob = blob_service.get_blob_client(
        container="cache",
        blob="results.json"
    )
    result_blob.upload_blob(json.dumps(results), overwrite=True)

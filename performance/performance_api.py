from flask import Flask, request, jsonify
import pandas as pd
import json
import io
from azure.storage.blob import BlobServiceClient

app = Flask(__name__)
AZURE_CONN = "DefaultEndpointsProtocol=https;AccountName=hashaccount;AccountKey=ZHW+Pgh3i7A8kgulaMviIjJpOiuYm7O2em9SfZTekfBfwED6WboU+MFsSo+ER6SX4hDMaH2tQizP+AStNI5k3g==;EndpointSuffix=core.windows.net"

def load_cleaned_data():
    blob = BlobServiceClient.from_connection_string(AZURE_CONN)\
        .get_blob_client("data", "Cleaned_Diets.csv")

    data = blob.download_blob().readall()
    return pd.read_csv(io.BytesIO(data))

def load_cached_results():
    blob = BlobServiceClient.from_connection_string(AZURE_CONN)\
        .get_blob_client("cache", "results.json")

    return json.loads(blob.download_blob().readall())

@app.route("/api/summary")
def summary():
    return jsonify(load_cached_results())

@app.route("/api/recipes")
def recipes():
    df = load_cleaned_data()

    diet = request.args.get("diet")
    search = request.args.get("search")
    page = int(request.args.get("page", 1))
    page_size = 10

    if diet:
        df = df[df["Diet_type"] == diet.lower()]

    if search:
        df = df[df["Recipe_name"].str.contains(search, case=False)]

    start = (page - 1) * page_size
    end = start + page_size

    return jsonify({
        "recipes": df.iloc[start:end].to_dict(orient="records"),
        "total": len(df),
        "page": page
    })

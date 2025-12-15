from flask import Flask, render_template, request, redirect, url_for, session
import pandas as pd
import bcrypt
from azure.storage.blob import BlobServiceClient
import io

def load_users():
    blob_service_client = BlobServiceClient.from_connection_string(
        "DefaultEndpointsProtocol=https;AccountName=hashaccount;AccountKey=ZHW+Pgh3i7A8kgulaMviIjJpOiuYm7O2em9SfZTekfBfwED6WboU+MFsSo+ER6SX4hDMaH2tQizP+AStNI5k3g==;EndpointSuffix=core.windows.net"
    )
    #Yes i know i misspelled accounts but i dont want to change it in azure 
    blob_client = blob_service_client.get_blob_client(
        container="acounts",
        blob="users.csv"
    )

    data = blob_client.download_blob().readall()
    return pd.read_csv(io.BytesIO(data))


def save_users(df):
    blob_service_client = BlobServiceClient.from_connection_string(
        "DefaultEndpointsProtocol=https;AccountName=hashaccount;AccountKey=ZHW+Pgh3i7A8kgulaMviIjJpOiuYm7O2em9SfZTekfBfwED6WboU+MFsSo+ER6SX4hDMaH2tQizP+AStNI5k3g==;EndpointSuffix=core.windows.net"
    )

    blob_client = blob_service_client.get_blob_client(
        container="acounts",
        blob="users.csv"
    )

    csv_data = df.to_csv(index=False)
    blob_client.upload_blob(csv_data, overwrite=True)
app = Flask(__name__)

app.secret_key = "925449f1e7c49251e1e6aa8d041981e30b966a0b345dc3a0af9178949364bd82"

@app.route('/home')
def home():
    if "user" not in session:
        return redirect(url_for("login_page"))
    return render_template('index.html', title='Home', username=session["user"])


@app.route("/login", methods=["GET"])
def login_page():
    return render_template("login/login.html")


#I used the post method because in our software security course its bad practice to use GET for it
#It would leave us vulnerable to XSS attacks 

@app.route("/login", methods=["POST"])
def login():
    username = request.json["username"]
    password = request.json["password"].encode("utf-8")

    users = load_users()

    user = users[users["username"] == username]

    if user.empty:
        return {"success": False}, 401

    stored_hash = user.iloc[0]["password_hash"].encode("utf-8")

    if bcrypt.checkpw(password, stored_hash):
        session["user"] = username
        return {"success": True, "redirect": url_for("home")}

    return {"success": False}, 401


@app.route('/register')
def register_page():
    return render_template('register/register.html')


@app.route("/register", methods=["POST"])
def register():
    username = request.json["username"]
    password = request.json["password"].encode("utf-8")

    users = load_users()

    if username in users["username"].values:
        return {"success": False, "error": "Username already exists"}, 400

    password_hash = bcrypt.hashpw(password, bcrypt.gensalt()).decode("utf-8")

    new_row = {
        "username": username,
        "password_hash": password_hash
    }

    users = users._append(new_row, ignore_index=True)

    save_users(users)

    #auto-login
    session["user"] = username

    return {"success": True, "redirect": url_for("home")}



if __name__ == '__main__':
    app.run(debug=True)







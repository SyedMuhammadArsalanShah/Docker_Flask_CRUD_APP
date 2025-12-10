from flask import Flask, jsonify
import psycopg2
import os
import time
from urllib.parse import urlparse

app = Flask(__name__)

# Get DATABASE_URL from environment (Railway sets this automatically)
DATABASE_URL = os.environ.get("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable not set!")

# Parse DATABASE_URL for psycopg2
result = urlparse(DATABASE_URL)
db_name = result.path[1:]  # remove leading '/'
db_user = result.username
db_password = result.password
db_host = result.hostname
db_port = result.port or 5432

# Retry DB connection until it succeeds
while True:
    try:
        conn = psycopg2.connect(
            host=db_host,
            database=db_name,
            user=db_user,
            password=db_password,
            port=db_port
        )
        print("Connected to PostgreSQL successfully!")
        break
    except Exception as e:
        print(f"Waiting for DB to start... ({e})")
        time.sleep(2)

@app.route("/")
def home():
    cur = conn.cursor()
    cur.execute("SELECT version();")
    db_version = cur.fetchone()
    cur.close()
    return jsonify({
        "message": "Hello, Docker with Python!",
        "postgres_version": db_version[0]
    })

if __name__ == "__main__":
    # Use Railway dynamic PORT
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

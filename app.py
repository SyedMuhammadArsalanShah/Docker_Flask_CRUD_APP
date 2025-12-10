from flask import Flask, jsonify
import psycopg2
import os
import time

app = Flask(__name__)

# Retry DB connection until it succeeds (useful when DB starts slowly)
while True:
    try:
        conn = psycopg2.connect(
            host=os.environ.get("DB_HOST", "db"),
            database=os.environ.get("DB_NAME", "mydb"),
            user=os.environ.get("DB_USER", "myuser"),
            password=os.environ.get("DB_PASSWORD", "mypassword")
        )
        break
    except Exception as e:
        print("Waiting for DB to start...")
        time.sleep(2)

@app.route("/")
def home():
    cur = conn.cursor()
    cur.execute("SELECT version();")
    db_version = cur.fetchone()
    return jsonify({
        "message": "Hello, Docker with Python!",
        "postgres_version": db_version[0]
    })

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))  # Railway ka dynamic PORT
    app.run(host="0.0.0.0", port=port)


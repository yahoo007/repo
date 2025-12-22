from flask import Flask, send_from_directory
import os
import psycopg2

# 1. On définit l'application AVANT les routes
app = Flask(__name__)

@app.route('/')
def index():
    return send_from_directory('../static', 'index.html')

@app.route('/db-check')
def db_check():
    try:
        # On utilise les noms standards PostgreSQL
        conn = psycopg2.connect(
            host=os.getenv("DB_HOST", "db"),
            database=os.getenv("POSTGRES_DB", "postgres"),
            user=os.getenv("POSTGRES_USER", "postgres"),
            password=os.getenv("POSTGRES_PASSWORD") # Changé pour correspondre à la DB
        )
        return {"status": "success", "message": "Connexion à PostgreSQL réussie !"}
    except Exception as e:
        return {"status": "error", "message": str(e)}, 500

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
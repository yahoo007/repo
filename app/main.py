from flask import Flask, send_from_directory
import os
import psycopg2

# 1. DÉCLARER APP EN PREMIER
app = Flask(__name__)

@app.route('/')
def index():
    # Affiche votre fichier HTML
    return send_from_directory('../static', 'index.html')

@app.route('/db-check')
def db_check():
    try:
        # Tente de se connecter
        conn = psycopg2.connect(
            host=os.getenv("DB_HOST", "db"),
            database=os.getenv("POSTGRES_DB", "postgres"),
            user=os.getenv("POSTGRES_USER", "postgres"),
            password=os.getenv("DB_PASSWORD")
        )
        cur = conn.cursor()
        cur.close()
        conn.close()
        return {"status": "success", "message": "Connexion à PostgreSQL réussie !"}
    except Exception as e:
        return {"status": "error", "message": str(e)}, 500

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
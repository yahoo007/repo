from flask import Flask, send_from_directory
import os
import psycopg2

app = Flask(__name__)

@app.route('/')
def index():
    # Affiche votre fichier HTML
    return send_from_directory('../static', 'index.html')

@app.route('/db-check')
def db_check():
    try:
        # Tente de se connecter à la base de données définie dans docker-compose
        conn = psycopg2.connect(
            host="db",
            database="dev_db",
            user="admin",
            password=os.getenv("DB_PASSWORD")
        )
        return {"status": "success", "message": "Connexion à PostgreSQL réussie !"}
    except Exception as e:
        return {"status": "error", "message": str(e)}, 500

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
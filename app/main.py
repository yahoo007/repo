@app.route('/db-check')
def db_check():
    try:
        # On utilise os.getenv avec des valeurs par défaut pour plus de sécurité
        conn = psycopg2.connect(
            host=os.getenv("DB_HOST", "db"),
            database=os.getenv("POSTGRES_DB", "postgres"),
            user=os.getenv("POSTGRES_USER", "postgres"),
            password=os.getenv("POSTGRES_PASSWORD") # Jenkins injecte POSTGRES_PASSWORD depuis le .env
        )
        cur = conn.cursor()
        cur.close()
        conn.close()
        return {"status": "success", "message": "Connexion à PostgreSQL réussie !"}
    except Exception as e:
        return {"status": "error", "message": str(e)}, 500
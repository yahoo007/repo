from flask import Flask, render_template, request, redirect
import psycopg2
import os

app = Flask(__name__)

def get_db_connection():
    return psycopg2.connect(
        host='db',
        database=os.environ.get('POSTGRES_DB'),
        user=os.environ.get('POSTGRES_USER'),
        password=os.environ.get('POSTGRES_PASSWORD')
    )

@app.route('/')
def index():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT contenu FROM demandes ORDER BY date_creation DESC;')
    demandes = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('index.html', demandes=demandes)

@app.route('/ajouter', methods=['POST'])
def ajouter():
    contenu = request.form['demande']
    if contenu:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('INSERT INTO demandes (contenu) VALUES (%s)', (contenu,))
        conn.commit()
        cur.close()
        conn.close()
    return redirect('/')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
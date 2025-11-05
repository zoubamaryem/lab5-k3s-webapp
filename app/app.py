from flask import Flask, render_template, request, redirect, url_for
import psycopg2
import os
import time

app = Flask(__name__)

# Récupérer les variables d'environnement pour la connexion DB
DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_PORT = os.getenv('DB_PORT', '5432')
DB_NAME = os.getenv('DB_NAME', 'webapp_db')
DB_USER = os.getenv('DB_USER', 'webapp_user')
DB_PASSWORD = os.getenv('DB_PASSWORD', 'webapp_password')

def get_db_connection():
    """Établir une connexion à la base de données PostgreSQL"""
    max_retries = 5
    retry_delay = 2
    
    for attempt in range(max_retries):
        try:
            conn = psycopg2.connect(
                host=DB_HOST,
                port=DB_PORT,
                database=DB_NAME,
                user=DB_USER,
                password=DB_PASSWORD,
                connect_timeout=5
            )
            return conn
        except psycopg2.OperationalError as e:
            if attempt < max_retries - 1:
                print(f"Tentative {attempt + 1}/{max_retries} - Erreur de connexion: {e}")
                time.sleep(retry_delay)
            else:
                print(f"Échec de connexion après {max_retries} tentatives")
                return None
        except Exception as e:
            print(f"Erreur inattendue de connexion à la DB: {e}")
            return None

def init_db():
    """Initialiser la base de données et créer la table si elle n'existe pas"""
    conn = get_db_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id SERIAL PRIMARY KEY,
                    name VARCHAR(100) NOT NULL,
                    email VARCHAR(100) NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            conn.commit()
            cursor.close()
            conn.close()
            print("✅ Base de données initialisée avec succès")
        except Exception as e:
            print(f"❌ Erreur lors de l'initialisation de la DB: {e}")

@app.route('/')
def index():
    """Page d'accueil avec formulaire et liste des utilisateurs"""
    conn = get_db_connection()
    users = []
    db_status = "Déconnecté"
    
    if conn:
        db_status = "Connecté"
        try:
            cursor = conn.cursor()
            cursor.execute('SELECT id, name, email, created_at FROM users ORDER BY created_at DESC')
            users = cursor.fetchall()
            cursor.close()
            conn.close()
        except Exception as e:
            print(f"Erreur lors de la récupération des données: {e}")
    
    return render_template('index.html', users=users, db_status=db_status)

@app.route('/add', methods=['POST'])
def add_user():
    """Ajouter un nouvel utilisateur"""
    name = request.form.get('name')
    email = request.form.get('email')
    
    if name and email:
        conn = get_db_connection()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute(
                    'INSERT INTO users (name, email) VALUES (%s, %s)',
                    (name, email)
                )
                conn.commit()
                cursor.close()
                conn.close()
                print(f"✅ Utilisateur ajouté: {name} ({email})")
            except Exception as e:
                print(f"❌ Erreur lors de l'insertion: {e}")
    
    return redirect(url_for('index'))

@app.route('/health')
def health():
    """Endpoint de santé pour Kubernetes"""
    conn = get_db_connection()
    if conn:
        conn.close()
        return {'status': 'healthy', 'database': 'connected'}, 200
    return {'status': 'unhealthy', 'database': 'disconnected'}, 503

@app.route('/info')
def info():
    """Informations sur l'environnement"""
    return {
        'app': 'K3s Web Application - Lab 5',
        'db_host': DB_HOST,
        'db_port': DB_PORT,
        'db_name': DB_NAME,
        'db_user': DB_USER
    }

if __name__ == '__main__':
    print("🚀 Démarrage de l'application Flask...")
    print(f"📊 Configuration DB: {DB_USER}@{DB_HOST}:{DB_PORT}/{DB_NAME}")
    
    # Attendre que la DB soit prête
    time.sleep(5)
    
    # Initialiser la DB au démarrage
    init_db()
    
    # Démarrer l'application
    print("✅ Application prête sur le port 5000")
    app.run(host='0.0.0.0', port=5000, debug=False)

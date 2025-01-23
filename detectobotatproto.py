from atproto import Client
import configparser
import sqlite3
import hashlib

# Fonction pour calculer le MD5 d'un texte
def calculate_md5(text):
    return hashlib.md5(text.encode('utf-8')).hexdigest()

# Se connecter ou créer une base de données SQLite
def connect_to_database(db_name="botmessage.db"):
    return sqlite3.connect(db_name)

# Créer une table si elle n'existe pas déjà
def create_table(conn):
    with conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS text_table (
                id TEXT PRIMARY KEY, -- MD5 hash
                text_content TEXT NOT NULL
            )
        ''')

# Insérer un texte dans la table
def insert_unique_text(conn, text):
    md5_hash = calculate_md5(text)
    try:
        with conn:
            conn.execute('''
                INSERT INTO text_table (id, text_content)
                VALUES (?, ?)
            ''', (md5_hash, text))
        print(f"Texte inséré : {text}")
    except sqlite3.IntegrityError:
        print(f"Doublon détecté : {text} (MD5 : {md5_hash})")

# Ajouter toutes les lignes d'un log à la base de données
def insert_log_file_to_db(conn, log_file_path):
    try:
        with open(log_file_path, "r", encoding="utf-8") as file:
            for line in file:
                line = line.strip()  # Supprime les espaces inutiles
                if line:  # Ignorer les lignes vides
                    insert_unique_text(conn, line)
    except FileNotFoundError:
        print(f"Erreur : Le fichier '{log_file_path}' est introuvable.")
    except Exception as e:
        print(f"Une erreur s'est produite : {e}")

# Écrire les textes dans un fichier ligne par ligne
def write_posts_to_file(posts, filename):
    with open(filename, 'w', encoding='utf-8') as file:
        for post in posts:
            file.write(post.record.text + '\n')

def Insert_post_target_to_db(target, conn, client):
    print(f'\nProfile Posts of {target}:\n\n')
    cursor = None
    while True:
        # Récupérer une page de posts
        response = client.get_author_feed(actor=target,cursor=cursor,limit=5)
        for text in response.feed:
            insert_unique_text(conn, text)

        # Vérifier si un curseur est disponible pour la page suivante
        cursor = response.cursor
        
        # Si aucun curseur n'est disponible, on a tout récupéré
        if not cursor:
            break

if __name__ == '__main__':
    config = configparser.ConfigParser()
    config.read('settings.ini')
    app_login = config['client']['app_login']
    app_passwd = config['client']['app_passwd']
    target = config['targets']['target']

    # Connexion à la base de données
    conn = connect_to_database()

    # Création de la table
    create_table(conn)

    # enregistrement du sample
    log_file_path = "gemmatroup124.log"
    insert_log_file_to_db(conn, log_file_path)


    # Connexion à bsky
    client = Client()
    profile = client.login(app_login, app_passwd)
    print('Welcome,', profile.display_name)
    
    # Récupération des posts de target
    # Insert_post_target_to_db(target, conn, client)

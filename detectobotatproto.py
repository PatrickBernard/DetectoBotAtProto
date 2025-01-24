from atproto import Client
import configparser
import sqlite3
import hashlib

# Calculer le MD5 d'un texte
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

def find_accounts_with_message(message):
    try:
        # Rechercher les posts contenant le message
        response = client.app.bsky.feed.search_posts(params={"q": message})
        accounts = []
        for post in response.posts:  # Parcours des objets PostView
            if hasattr(post.record, 'text') and post.record.text == message:  # Accéder directement à l'attribut 'text'
                accounts.append(post.author.handle)  # Accéder au handle de l'auteur
        return accounts
    except Exception as e:
        print(f"Erreur lors de la recherche des comptes pour le message '{message}' : {e}")
        return []

# Fonction pour imprimer la liste des comptes
def print_accounts_list(accounts):
    if not accounts:
        print("Aucun compte n'a été trouvé.")
        return

    print("Liste des comptes trouvés :")
    for i, account in enumerate(accounts, start=1):
        print(f"{i}. {account}")

# Fonction pour créer ou récupérer une liste de modération
def create_or_get_moderation_list(actor,list_name):
    global moderation_list_id

    # Récupérer les listes existantes
    try:
        lists = client.app.bsky.graph.get_lists(params={"actor": actor})
        for lst in lists['lists']:
            print(lst['name']) 
            if lst['name'] == list_name:
                moderation_list_id = lst['uri']
                print(f"Liste de modération trouvée avec l'ID : {moderation_list_id}")
                return moderation_list_id
    except Exception as e:
        print(f"Erreur lors de la récupération des listes : {e}")

    # Si la liste n'existe pas, la créer
    # try:
    #     # Ici, on simule la création d'une liste avec un appel correct pour l'API
    #     response = client.app.bsky.graph.list.create()
    #     (
    #         params={
    #             "name": list_name,
    #             "description": "Liste de modération automatique"
    #         }
    #     )
    #     moderation_list_id = response['uri']
    #     print(f"Liste de modération créée avec l'ID : {moderation_list_id}")
    #     return moderation_list_id
    # except Exception as e:
    #     print(f"Erreur lors de la création de la liste : {e}")


if __name__ == '__main__':
    config = configparser.ConfigParser()
    config.read('settings.ini')
    app_login = config['client']['app_login']
    app_passwd = config['client']['app_passwd']
    target = config['targets']['target']
    list_name = config['lists']['moderation_list_name']

    # Connexion à la base de données
    conn = connect_to_database()

    # Création de la table
    create_table(conn)
    
    # Connexion à bsky
    client = Client()
    profile = client.login(app_login, app_passwd)
    print('Welcome,', profile.display_name)
    create_or_get_moderation_list(app_login,list_name)
    print(f"ID de la liste de modération : {moderation_list_id}")
    
    message="En soutenant inconditionnellement l'Ukraine, Macron a négligé les problèmes internes de la France. C'est inacceptable."
    responses=find_accounts_with_message(message)
    print_accounts_list(responses)
    
    
    # Récupération des posts de target,
    # avec le md5 associer cela nous sert également de déduplication
    #Insert_post_target_to_db(target, conn, client)
    
    # récupère les messages de la bdd
    #cursor = conn.cursor()
    #cursor.execute("SELECT text_content FROM text_table")
    #messages = cursor.fetchall()
    
    #for message in messages:
    #    accounts = find_accounts_with_message(message)
    #    for account in accounts:
    #        add_account_to_moderation_list(moderation_list_id,account)
    
    # enregistrement du sample
    # log_file_path = "gemmatroup124.log"
    # insert_log_file_to_db(conn, log_file_path)
from atproto import Client
import configparser

# Écrire les textes dans un fichier ligne par ligne
def write_posts_to_file(posts, filename):
    with open(filename, 'w', encoding='utf-8') as file:
        for post in posts:
            file.write(post.record.text + '\n')

def main():
    config = configparser.ConfigParser()
    config.read('settings.ini')
    app_login = config['client']['app_login']
    app_passwd = config['client']['app_passwd']
    
    client = Client()
    profile = client.login(app_login, app_passwd)
    print('Welcome,', profile.display_name)
    
    handle = 'gemmatroup124.bsky.social'
    
    print(f'\nProfile Posts of {handle}:\n\n')

    cursor = None
    
    while True:
        # Récupérer une page de posts
        response = client.get_author_feed(actor=handle,cursor=cursor,limit=5)
        
        with open("toto.log", 'a', encoding='utf-8') as file:
            for view in response.feed:
                file.write(view.post.record.text + '\n')

        # Vérifier si un curseur est disponible pour la page suivante
        cursor = response.cursor
        
        # Si aucun curseur n'est disponible, on a tout récupéré
        if not cursor:
            break


if __name__ == '__main__':
    main()

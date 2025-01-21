from atproto import Client, client_utils
import configparser

def main():
    config = configparser.ConfigParser()
    config.read('settings.ini')
    app_login = config['client']['app_login']
    app_passwd = config['client']['app_passwd']
    
    client = Client()
    profile = client.login(app_login, app_passwd)
    print('Welcome,', profile.display_name)
    
    handle = 'norton2546.bsky.social'
    
    print(f'\nProfile Posts of {handle}:\n\n')

    # Get profile's posts. Use pagination (cursor + limit) to fetch all
    profile_feed = client.get_author_feed(actor=handle, limit=5)
    for feed_view in profile_feed.feed:
        print('-', feed_view.post.record.text)

    #text = client_utils.TextBuilder().text('TEST : Hello World from detectobot ').link('Python SDK', 'https://atproto.blue')
    #post = client.send_post(text)
    #client.like(post.uri, post.cid)

if __name__ == '__main__':
    main()

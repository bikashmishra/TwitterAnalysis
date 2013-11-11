from twitter import *
import os.path 
import urllib
import json

def auth_search():
    CONSUMER_CREDENTIALS = os.path.expanduser('~/My Documents/data_science_bm1__consumertoken')
    consumer_key, consumer_secret = read_token_file(CONSUMER_CREDENTIALS)

    MY_TWITTER_CREDS = os.path.expanduser('~/My Documents/.data_science_bm1__credentials')  
    if not os.path.exists(MY_TWITTER_CREDS):
        oauth_dance("data_science_bm1", consumer_key, consumer_secret, MY_TWITTER_CREDS)
    
    oauth_token, oauth_secret = read_token_file(MY_TWITTER_CREDS)
    
    twitter = Twitter(auth=OAuth(oauth_token, oauth_secret, consumer_key, consumer_secret))
    searchres = twitter.search.tweets(q="#GOP")
    for status in searchres['statuses']:
        print status['text']
    
def main():
    auth_search()
    
if __name__=="__main__":
    main()
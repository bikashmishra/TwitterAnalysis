""" Uses Python Twitter Tools from sixohsix/Twitter  """
from twitter import *
import os.path 
import urllib
import json
from Stream import * 

def tweepy_stream():
    CONSUMER_CREDENTIALS = os.path.expanduser('~/My Documents/data_science_bm1__consumertoken')
    consumer_key, consumer_secret = read_token_file(CONSUMER_CREDENTIALS)

    MY_TWITTER_CREDS = os.path.expanduser('~/My Documents/.data_science_bm1__credentials')
    key, secret = read_token_file(MY_TWITTER_CREDS)
    
    s = Stream(consumer_key, consumer_secret, key, secret, 'teststream')
    sthread = s.run()
    print type(sthread)
    
def auth_search():
    CONSUMER_CREDENTIALS = os.path.expanduser('~/My Documents/data_science_bm1__consumertoken')
    consumer_key, consumer_secret = read_token_file(CONSUMER_CREDENTIALS)

    MY_TWITTER_CREDS = os.path.expanduser('~/My Documents/.data_science_bm1__credentials')
     
    if not os.path.exists(MY_TWITTER_CREDS):
        oauth_dance("data_science_bm1", consumer_key, consumer_secret, MY_TWITTER_CREDS)
    
    oauth_token, oauth_secret = read_token_file(MY_TWITTER_CREDS)
    
    twit = Twitter(auth=OAuth(oauth_token, oauth_secret, consumer_key, consumer_secret))
    searchres = twit.search.tweets(q="#GOP")
    for status in searchres['statuses']:
        i=0
        if i<1:
            for k,v in status.iteritems():
                print k
                print v
#         print status['text']
    
def auth_status():
    CONSUMER_CREDENTIALS = os.path.expanduser('~/My Documents/data_science_bm1__consumertoken')
    consumer_key, consumer_secret = read_token_file(CONSUMER_CREDENTIALS)

    MY_TWITTER_CREDS = os.path.expanduser('~/My Documents/.data_science_bm1__credentials')  
    if not os.path.exists(MY_TWITTER_CREDS):
        oauth_dance("data_science_bm1", consumer_key, consumer_secret, MY_TWITTER_CREDS)
    
    oauth_token, oauth_secret = read_token_file(MY_TWITTER_CREDS)
    twit = Twitter(auth=OAuth(oauth_token, oauth_secret, consumer_key, consumer_secret))
    
    print twit.statuses.home_timeline()
    # does not work
#    print twit.statuses.friends_timeline(id="itzarun")
    
def auth_stream():
    CONSUMER_CREDENTIALS = os.path.expanduser('~/My Documents/data_science_bm1__consumertoken')
    consumer_key, consumer_secret = read_token_file(CONSUMER_CREDENTIALS)

    MY_TWITTER_CREDS = os.path.expanduser('~/My Documents/.data_science_bm1__credentials')  
    if not os.path.exists(MY_TWITTER_CREDS):
        oauth_dance("data_science_bm1", consumer_key, consumer_secret, MY_TWITTER_CREDS)
    
    oauth_token, oauth_secret = read_token_file(MY_TWITTER_CREDS)
    twit_stream = TwitterStream(auth=OAuth(oauth_token, oauth_secret, consumer_key, consumer_secret))
    iterator = twit_stream.statuses.sample(q='#GOP')
    for tweet in iterator:
        print tweet
     
def main():
    tweepy_stream()
    
if __name__=="__main__":
    main()
import configparser
import tweepy

#read config
config = configparser.ConfigParser()
config.read('../config/config.ini')

#read the config
api_key = config['twitter']['api_key']
api_key_secret = config['twitter']['api_key_secret']
access_token = config['twitter']['access_token']
access_token_secret = config['twitter']['access_token_secret']

# Authenticate
auth = tweepy.OAuthHandler(api_key, api_key_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)


def getTweetsBYHashtag(hashtag):
    pass

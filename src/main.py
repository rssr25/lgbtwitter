import re
import tweepy
import configparser
import numpy as np
import pandas as pd
from wordcloud import WordCloud

import sys
from preprocess import PreprocessTweets

def getApiObject():
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

    return api


if __name__ == "__main__":

    api = getApiObject()
    tweets, location = PreprocessTweets.getTweetsByKeyword("lgbtq", api)
    print(tweets)
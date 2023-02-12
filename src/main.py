import re
import tweepy
import configparser
import numpy as np
import pandas as pd
from wordcloud import WordCloud
from better_profanity import profanity
import sys



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


def clean_tweet(tweet):
    if type(tweet) == np.float32:
        return ""
    r = tweet.lower()
    r = profanity.censor(r)
    r = re.sub("'", "", r) # This is to avoid removing contractions in english
    r = re.sub("@[A-Za-z0-9_]+","", r)
    r = re.sub("#[A-Za-z0-9_]+","", r)
    r = re.sub(r'http\S+', '', r)
    r = re.sub('[()!?]', ' ', r)
    r = re.sub('\[.*?\]',' ', r)
    r = re.sub("[^a-z0-9]"," ", r)
    r = r.split()
    #stopwords = ["for", "on", "an", "a", "of", "and", "in", "the", "to", "from"]
    #r = [w for w in r if not w in stopwords]
    r = " ".join(word for word in r)
    return r

def getTweetsByKeyword(query, api, country=None):

    filtered = query + "-filter:retweets"

    if country is not None:
        searchCountry = country
        places = api.search_geo(query=searchCountry, granularity="country")
        place_id = places[0].id
        print(place_id)
        filtered = (filtered) and ("place:%s" % place_id)
        print(filtered)

    else:
        country = ""

    
    tweets = tweepy.Cursor(api.search_tweets, 
                            q=filtered,
                            lang="en").items(10)
    

    list1 = [[tweet.text, tweet.user.screen_name, tweet.user.location] for tweet in tweets]
    df = pd.DataFrame(data=list1, columns=['tweets','user', "location"])
    tweet_list = df.tweets.to_list()
    locations = df.location.to_list()
    cleaned = [clean_tweet(tw) for tw in tweet_list]
    return (cleaned, locations)



if __name__ == "__main__":

    api = getApiObject()
    tweets, location = getTweetsByKeyword("lgbtq", api)
    print(tweets)
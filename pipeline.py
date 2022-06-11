import os
import tweepy
from tyl import extract_liked_tweets, save_liked_tweets


TWITTER_BEARER_TOKEN = os.getenv("TWITTER_BEARER_TOKEN")
TWITTER_USER_ID = os.getenv("TWITTER_USER_ID")


client = tweepy.Client(bearer_token=TWITTER_BEARER_TOKEN)
liked_tweets = extract_liked_tweets(client, TWITTER_USER_ID)
save_liked_tweets(liked_tweets, "liked_tweets.pkl")

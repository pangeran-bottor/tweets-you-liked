import os
from tyl import get_client, extract_liked_tweets, save_liked_tweets


TWITTER_USER_ID = os.getenv("TWITTER_USER_ID")


client = get_client()
liked_tweets = extract_liked_tweets(client, TWITTER_USER_ID)
save_liked_tweets(liked_tweets, "liked_tweets.pkl")

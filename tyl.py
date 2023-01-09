import collections
import os
import pickle
from typing import List

import pandas as pd
import tweepy


def fields_to_str(target_fields):
    return ",".join(target_fields)


# See https://developer.twitter.com/en/docs/twitter-api/data-dictionary/object-model/tweet
tweet_target_fields = ["id", "text", "author_id", "created_at", "public_metrics"]

# See https://developer.twitter.com/en/docs/twitter-api/data-dictionary/object-model/user
user_target_fields = [
    "id",
    "name",
    "username",
    "url",
    "public_metrics",
    "profile_image_url",
]

TweetYouLiked = collections.namedtuple("TweetYouLiked", ["tweet", "user"])


def get_client():
    TWITTER_BEARER_TOKEN = os.getenv("TWITTER_BEARER_TOKEN")
    client = tweepy.Client(bearer_token=TWITTER_BEARER_TOKEN)
    return client


def get_twitter_id_by_username(client: tweepy.Client, username: str):
    resp = client.get_user(username=username)
    twitter_id = resp.data.id
    return twitter_id


def extract_liked_tweets(client, twitter_id):
    liked_tweets = []

    resp = client.get_liked_tweets(
        twitter_id,
        tweet_fields=fields_to_str(tweet_target_fields),
        user_fields=fields_to_str(user_target_fields),
        expansions="author_id",
    )

    page_limit = 1

    while resp.data and page_limit <= 3:
        page_limit += 1

        author_dict = {}
        for user in resp.includes["users"]:
            author_dict[user.id] = user.data

        for tweet in resp.data:
            tyl = TweetYouLiked(tweet.data, author_dict[tweet.author_id])
            liked_tweets.append(tyl)

        next_token = resp.meta.get("next_token", "")
        if next_token != "":
            resp = client.get_liked_tweets(
                twitter_id,
                tweet_fields=fields_to_str(tweet_target_fields),
                user_fields=fields_to_str(user_target_fields),
                expansions="author_id",
                pagination_token=next_token,
            )
        else:
            break
    return liked_tweets


def save_liked_tweets(liked_tweets, filename):
    with open(filename, "wb") as f:
        pickle.dump(liked_tweets, f)


def load_liked_tweets(filename):
    with open(filename, "rb") as f:
        liked_tweets = pickle.load(f)
    return liked_tweets


def liked_tweets_to_dataframe(liked_tweets: List[TweetYouLiked]) -> pd.DataFrame:
    raw_data = []
    for liked_tweet in liked_tweets:
        data = dict(
            tweet_id=liked_tweet.tweet["id"],
            text=liked_tweet.tweet["text"],
            author_id=liked_tweet.user["id"],
            author_username=liked_tweet.user["username"],
        )

        raw_data.append(data)

    df = pd.DataFrame.from_records(raw_data)
    return df

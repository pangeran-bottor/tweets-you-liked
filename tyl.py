import collections
import pickle


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


def extract_liked_tweets(client, user_id):
    liked_tweets = []

    resp = client.get_liked_tweets(
        user_id,
        tweet_fields=fields_to_str(tweet_target_fields),
        user_fields=fields_to_str(user_target_fields),
        expansions="author_id",
    )

    while resp.data:
        author_dict = {}
        for user in resp.includes["users"]:
            author_dict[user.id] = user.data

        for tweet in resp.data:
            tyl = TweetYouLiked(tweet.data, author_dict[tweet.author_id])
            liked_tweets.append(tyl)

        next_token = resp.meta.get("next_token", "")
        if next_token != "":
            resp = client.get_liked_tweets(
                user_id,
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

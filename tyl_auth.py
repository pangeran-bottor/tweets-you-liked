import tweepy


REDIRECT_URI = "https://pangeran-bottor-tweets-you-liked-tyl-app-2elaze.streamlitapp.com/"
CLIENT_ID = ""
CLIENT_SECRET = ""
SCOPES = ["follows.read", "like.read", "tweet.read", "users.read"]

oauth2_user_handler = tweepy.OAuth2UserHandler(
    client_id=CLIENT_ID,
    redirect_uri="https://pangeran-bottor-tweets-you-liked-tyl-app-2elaze.streamlitapp.com/",
    scope=["like.read", "follows.read", "tweet.read", "users.read"],
    # Client Secret is only necessary if using a confidential client
    client_secret=CLIENT_SECRET
)

authorization_url = oauth2_user_handler.get_authorization_url()

# user authorize app, then get the url (code)
token_resp = oauth2_user_handler.fetch_token("the URL")
client = token_resp["access_token"]
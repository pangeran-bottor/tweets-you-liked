from tyl import *
import streamlit as st


st. set_page_config(layout="wide")
if "liked_tweets_map" not in st.session_state:
    st.session_state["liked_tweets_map"] = {}


def extract_button_callback():
    # TODO: validate inputted twitter id
    current_twitter_username = st.session_state.twitter_username
    twitter_id = get_twitter_id_by_username(client, current_twitter_username)

    extracted_liked_tweets = extract_liked_tweets(
        client, twitter_id
    )
    extracted_liked_tweets_df = liked_tweets_to_dataframe(extracted_liked_tweets)

    st.session_state.liked_tweets_map[
        current_twitter_username
    ] = extracted_liked_tweets_df


client = get_client()
liked_tweets = []


st.title("Tweets You Liked")


twitter_username_text_input = st.text_input(label="Insert Twitter Username", key="twitter_username")
extract_button = st.button(
    label="Get Tweets You Liked!", on_click=extract_button_callback
)

if extract_button:
    st.write(
        "Tweets You Liked: ",
        len(st.session_state.liked_tweets_map.get(st.session_state.twitter_username, [])),
    )
    st.dataframe(
        data=st.session_state.liked_tweets_map.get(st.session_state.twitter_username, []),
        width=5000
    )

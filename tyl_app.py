from io import BytesIO
from tyl import *
import streamlit as st


st.set_page_config(layout="wide")
if "liked_tweets_map" not in st.session_state:
    st.session_state["liked_tweets_map"] = {}


def extract_button_callback():
    # TODO: validate inputted twitter id
    current_twitter_username = st.session_state.twitter_username
    twitter_id = get_twitter_id_by_username(client, current_twitter_username)

    extracted_liked_tweets = extract_liked_tweets(client, twitter_id)
    extracted_liked_tweets_df = liked_tweets_to_dataframe(extracted_liked_tweets)

    st.session_state.liked_tweets_map[
        current_twitter_username
    ] = extracted_liked_tweets_df


def get_current_dataframe():
    current_twitter_username = st.session_state.twitter_username
    df = st.session_state.liked_tweets_map.get(current_twitter_username, pd.DataFrame())
    return df


def to_excel(df):
    output = BytesIO()
    writer = pd.ExcelWriter(output, engine="xlsxwriter")
    df.to_excel(writer, index=False, sheet_name="Sheet1")
    workbook = writer.book
    worksheet = writer.sheets["Sheet1"]
    format1 = workbook.add_format({"num_format": "0.00"})
    worksheet.set_column("A:A", None, format1)
    writer.save()
    processed_data = output.getvalue()
    return processed_data


client = get_client()
liked_tweets = []


st.title("Tweets You Liked")


twitter_username_text_input = st.text_input(
    label="Insert Twitter Username", key="twitter_username"
)
extract_button = st.button(
    label="Get Tweets You Liked!", on_click=extract_button_callback
)

if extract_button:
    current_twitter_username = st.session_state.twitter_username
    current_df = get_current_dataframe()
    st.write(
        "Tweets You Liked: ",
        len(current_df),
    )
    st.dataframe(data=current_df, width=5000)

    df_xlsx = to_excel(current_df)
    st.download_button("Download your data", df_xlsx, f"TweetsYouLiked_{current_twitter_username}.xlsx")

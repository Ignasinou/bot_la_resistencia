from CONF import API_key
from CONF import API_key_secret
from CONF import bearer_token
from CONF import access_token
from CONF import access_token_secret
import tweepy

def sendTweet():
    # Authenticate to Twitter
    # client = tweepy.Client(bearer_token,API_key,API_key_secret,access_token,access_token_secret)
    client = tweepy.Client(
        consumer_key=API_key, consumer_secret=API_key_secret,
        access_token=access_token, access_token_secret=access_token_secret
    )
    response = client.create_tweet(
        text="Fechas disponibles."
    )
sendTweet()
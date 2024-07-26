import os
import tweepy
import yfinance as yf
import pandas as pd
from datetime import date, timedelta
  

# ----- POST TO TWITTER ----- #

# TOKENS AND SECRETS
CLIENT_ID = os.environ["CLIENT_ID"]
CLIENT_ID_SECRET = os.environ["CLIENT_ID_SECRET"]
ACCESS_TOKEN = os.environ["ACCESS_TOKEN"]
ACCESS_TOKEN_SECRET = os.environ["ACCESS_TOKEN_SECRET"]
API_KEY = os.environ["API_KEY"]
API_KEY_SECRET = os.environ["API_KEY_SECRET"]
BEARER_TOKEN = os.environ["BEARER_TOKEN"]

# AUTHENTICATION - WILL RESULT IN A 401 ERROR
"""
auth = tweepy.OAuthHandler(API_KEY, API_KEY_SECRET)
auth.set_access_token(
    ACCESS_TOKEN,
    ACCESS_TOKEN_SECRET,
)
"""

# INITIALIZE
api = tweepy.Client(
    access_token=ACCESS_TOKEN,
    access_token_secret=ACCESS_TOKEN_SECRET,
    consumer_key=API_KEY,
    consumer_secret=API_KEY_SECRET,
)

# POST TO TWITTER
tweet = result
post_result = api.create_tweet(text="pls work!")

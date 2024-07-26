import os
import tweepy
import yfinance as yf
import pandas as pd
from datetime import date, timedelta

# ----- GET S&P500 STOCK UPDATES ----- #

# GET STOCK TICKERS (S&P 500)
sp500 = pd.read_html('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')[0]
sp500_tickers = sp500.Symbol.to_list()

# GET YESTERDAY AND BEFORE YESTERDAY DATE
yesterday = date.today() - timedelta(days = 1)
byesterday = date.today() - timedelta(days = 2)

# GET BEFORE YESTERDAY PRICE DATA
data = yf.download(sp500_tickers, byesterday, auto_adjust=True)
data = data["Close"]
data = data.transpose()

# DROP NULL VALUES
data.dropna(inplace = True) 

# CONVERT TO DICT
data_dict = data.to_dict()

# GET VALUES THEN CONVERT TO DATAFRAME
new_data = data_dict.values()
new = pd.DataFrame.from_dict(new_data)

# TRANSPOSE THEN RENAME COLUMN
new_t = new.transpose()
new_t.rename(columns={0:"byesterday", 1:"yesterday"}, inplace=True)

new_t['price increase'] = new_t.apply(lambda x: x['yesterday'] - x['byesterday'], axis=1)
new_t['percent'] = new_t.apply(lambda x: ((x['yesterday'] - x['byesterday']) / x['byesterday']) * 100, axis=1)

# SORT BY PERCENT
new_t.sort_values("percent", axis=0, ascending=False, inplace=True)
 
# FORMAT VALUES
new_t["price increase"] = new_t["price increase"].map("${:.2f}".format)
new_t["percent"] = new_t["percent"].map("{:.2f}%".format)

# GET TOP 5
top5 = new_t.drop(columns=['byesterday', 'yesterday']).head()

# CONVERT NAME, PRICE AND PERCENT TO LIST
top5_names = list(top5['price increase'].to_dict().keys())
top5_price = list(top5['price increase'].to_dict().values())
top5_percent = list(top5['percent'].to_dict().values())

long_name = []

# GET WEBSITE AND SUMMARY, THEN PUT TO LIST
for name in top5_names:
  k = yf.Ticker(name)
  long_name.append(k.info['longName'].replace("Inc.", "").replace(",", "").strip())

# SHOW DETAILS
result = f"""Daily Top Stock ({yesterday.strftime("%B %d, %Y")}):
"""
for i in range(5):
  result += f"""
{long_name[i]} ({top5_names[i]}) - {top5_percent[i]} - {top5_price[i]}"""
  

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
    bearer_token=BEARER_TOKEN,
    access_token=ACCESS_TOKEN,
    access_token_secret=ACCESS_TOKEN_SECRET,
    consumer_key=API_KEY,
    consumer_secret=API_KEY_SECRET,
)

# POST TO TWITTER
tweet = result
post_result = api.create_tweet(text="pls work!")

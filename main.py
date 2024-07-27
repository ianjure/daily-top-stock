import os
import tweepy
import yfinance as yf
import pandas as pd
from datetime import date, timedelta

def getDailyTopStocks():

  """
  Returns a string of the daily top performing stocks in S&P 500.
  """

  # GET STOCK TICKERS (S&P 500)
  sp500 = pd.read_html('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')[0]
  sp500_tickers = sp500.Symbol.to_list()

  # GET YESTERDAY AND BEFORE YESTERDAY DATE
  yesterday = date.today() - timedelta(days = 1)
  before_yesterday = date.today() - timedelta(days = 2)

  # GET BEFORE YESTERDAY PRICE DATA
  data = yf.download(sp500_tickers, before_yesterday, auto_adjust=True)
  data = data["Close"]
  data = data.transpose()

  # DROP NULL VALUES
  data.dropna(inplace = True) 

  # CONVERT TO DICT
  data_dict = data.to_dict()

  # GET VALUES THEN CONVERT TO DATAFRAME
  new_data = data_dict.values()
  new_data = pd.DataFrame.from_dict(new_data)

  # TRANSPOSE THEN RENAME COLUMN
  new_data = new_data.transpose()
  new_data.rename(columns={0:"byesterday", 1:"yesterday"}, inplace=True)

  new_data['price increase'] = new_data.apply(lambda x: x['yesterday'] - x['byesterday'], axis=1)
  new_data['percent'] = new_data.apply(lambda x: ((x['yesterday'] - x['byesterday']) / x['byesterday']) * 100, axis=1)

  # SORT BY PERCENT
  new_data.sort_values("percent", axis=0, ascending=False, inplace=True)
  
  # FORMAT VALUES
  new_data["price increase"] = new_data["price increase"].map("${:.2f}".format)
  new_data["percent"] = new_data["percent"].map("{:.2f}%".format)

  # GET TOP 5
  top5 = new_data.drop(columns=['byesterday', 'yesterday']).head()

  # CONVERT NAME, PRICE AND PERCENT TO LIST
  top5_names = list(top5['price increase'].to_dict().keys())
  top5_price = list(top5['price increase'].to_dict().values())
  top5_percent = list(top5['percent'].to_dict().values())

  long_name = []

  # GET THE COMPANY NAMES, THEN PUT TO LIST
  for name in top5_names:
    k = yf.Ticker(name)
    long_name.append(k.info['longName'].replace("Inc.", "").replace(",", "").strip())

  # SHOW DETAILS
  result = ""

  for i in range(5):
    result += f"""
{long_name[i]} ({top5_names[i]}) - {top5_percent[i]} - {top5_price[i]}"""
  
  result += f"""
  
📈 {yesterday.strftime("%B %d, %Y")}
"""
  return result

def postTwitter(ACCESS_TOKEN: str, ACCESS_TOKEN_SECRET: str, API_KEY: str, API_KEY_SECRET: str, MESSAGE: str):
  
  """
  Use Tweepy to access twitter API and make a post.
  """
  
  # INITIALIZE TOKENS
  api = tweepy.Client(
      access_token=ACCESS_TOKEN,
      access_token_secret=ACCESS_TOKEN_SECRET,
      consumer_key=API_KEY,
      consumer_secret=API_KEY_SECRET,
  )

  # POST TO TWITTER
  tweet = api.create_tweet(text=MESSAGE)

  # STATUS MESSAGE
  print(MESSAGE)
  print("Post Successful!")

def main():

  """
  Get the message using the getDailyTopStocks() method
  and post its result using the postTwitter() method.
  """

  # TOKENS AND SECRETS
  ACCESS_TOKEN = os.environ["ACCESS_TOKEN"]
  ACCESS_TOKEN_SECRET = os.environ["ACCESS_TOKEN_SECRET"]
  API_KEY = os.environ["API_KEY"]
  API_KEY_SECRET = os.environ["API_KEY_SECRET"]

  # RUN METHODS
  result = getDailyTopStocks()
  postTwitter(ACCESS_TOKEN, ACCESS_TOKEN_SECRET, API_KEY, API_KEY_SECRET, result)

if __name__ == "__main__":
  main()

import praw
import config
from textblob import TextBlob
from binance.client import Client
from binance.enums import *
from ta.momentum import RSIIndicator

client=Client(config.BINANCE_KEY,config.BINANCE_SECRET)

reddit = praw.Reddit(
    client_id=config.REDDIT_ID,
    client_secret=config.REDDIT_SECRET,
    password=config.REDDIT_PASS,
    user_agent="USERAGENT",
    username=config.REDDIT_USER,
)

sentimentList=[]
dogePrices=[]
neddedSentiments=3

TRADE_SYMBOL='BTCUSDT'
TRADE_QUANTITY=0.001
in_position=False
 
def average(lst):
    if(len(lst)==0):
        return len(lst);
    else:
         return sum(lst[-neddedSentiments:])/neddedSentiments
# print(reddit);
# for comment in reddit.subreddit("test").comments(limit=25):
#     print(comment.author)

# for submission in reddit.subreddit("bitcoin").hot(limit=25):
#     print(submission.title)

def order(side,quantity,symbol,order_type=ORDER_TYPE_MARKET):
    try:
        print('sending order')
        order=client.create_order(symbol=symbol,side=side,type=order_type,quantity=quantity)
        print(order)
    except Exception as e:
            print('an exception has occured '+ str(e))    
            return False
    return True         

for comment in reddit.subreddit("bitcoin").stream.comments():
     print(comment.body)
     redditComment=comment.body
     blob=TextBlob(redditComment)

     sent=blob.sentiment
     print(" ************ sentiment is: "+ str(sent.polarity))
     candles=client.get_historical_klines(TRADE_SYMBOL,Client.KLINE_INTERVAL_5MINUTE,"5 Minutes ago UTC")
     print(candles[-1][1])

     if len(dogePrices)==0:
        dogePrices.append(candles[-1][1])
     else:
        if(dogePrices[-1]!=candles[-1][1]):
            dogePrices.append(candles[-1][1])


    #  if(sent.polarity!=0.0):
    #     sentimentList.append(sent.polarity)

    #  if(len(sentimentList)>neddedSentiments and round(average(sentimentList))>0.1) :
    #     print("BUY")
    #     if in_position :
    #         print(" ************ BUY ORDER BUT WE OWN **************")
    #     else:
    #          print(" ************ BUY ORDER **************")
    #          order_succeded=order(SIDE_BUY,TRADE_QUANTITY,TRADE_SYMBOL)
    #          if order_succeded:
    #             in_position=True

    #  elif( len(sentimentList)>neddedSentiments and round(average(sentimentList))<-0.5) :
    #     print("SELL") 
    #     if in_position:
    #        order_succeded=order(SIDE_SELL,TRADE_QUANTITY,TRADE_SYMBOL)  
    #        if order_succeded:
    #             in_position=False
    #     else :
    #          print(" ************ SELL ORDER BUT WE DON'T OWN **************")

import requests
from twilio.rest import Client
STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"

STOCK_API_KEY = "QJVIJAQCY7JQB0AU"
NEWS_API_KEY = "182a442d812246fbb42d00a00866492b"
TWILIO_SID = "ACe4024bab8b17bb4bfac00e14c4b0196b"
TWILIO_AUTH_TOKEN = "f083e015d02330a0f69b05172df25837"

#GETTING YESTERDAYS DATA

stock_params = {"function" : "TIME_SERIES_DAILY", "symbol" : STOCK_NAME, "apikey" : STOCK_API_KEY}
response = requests.get(STOCK_ENDPOINT, params=stock_params)
data = response.json()["Time Series (Daily)"]
data_list = [value for (key, value) in data.items()]
yesterday_data = data_list[0]
yesterday_closing_price = yesterday_data["4. close"]
print(yesterday_closing_price)

#GETTING DAY BEFORE YESTERDAYS DATA

day_before_yesterday_data = data_list[1]
day_before_yesterday_closing_price = day_before_yesterday_data["4. close"]
print(day_before_yesterday_closing_price)

#DIFFERENCE OF DATA

difference = abs(float(yesterday_closing_price) - float(day_before_yesterday_closing_price))
up_down = None
if difference>0:
    up_down = "📈"
else:
    up_down= "📉"

diff_percent = round((difference/float(yesterday_closing_price)) * 100)
print(diff_percent)

#NEWS API

if abs(diff_percent) > 5:
    news_params = {"apiKey" : NEWS_API_KEY, "qInTitle" : COMPANY_NAME}
    news_response = requests.get(NEWS_ENDPOINT, params = news_params)
    articles = news_response.json()["articles"]

#GETTING NEWS

    three_articles = articles[:3]
    print(three_articles)


#FORMATTING NEWS

    formatted_articles = [f"{STOCK_NAME}: {up_down}{diff_percent}%\nHeadline: {article['title']}. \nBrief: {article['description']}" for article in three_articles]

#SMS MESSAGE
    client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)

    for article in formatted_articles:
        message = client.messages.create(
            body = article,
            from_ = "+17085463190",
            to = "+918590792815"
        )




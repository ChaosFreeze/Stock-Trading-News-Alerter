import os
from twilio.rest import Client
import requests
from datetime import date, timedelta

STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"

stock_parameters = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK_NAME,
    "apikey": "5C2V9FA55QQU4B0I"
}

news_parameter = {
    "q": COMPANY_NAME,
    "apiKey": "836f927fe1b74f2d9aeeb816132b6dcf",
}
# # STEP 1: Use https://www.alphavantage.co/documentation/#daily
# When stock price increase/decreases by 5% between yesterday and the day before yesterday then print("Get News").

# TODO 1. - Get yesterday's closing stock price. Hint: You can perform list comprehensions on Python dictionaries.
#  e.g. [new_value for (key, value) in dictionary.items()]
today = date.today()
yesterday = str(today - timedelta(days=1))
previous_day = str(today - timedelta(days=2))

response = requests.get(url=STOCK_ENDPOINT, params=stock_parameters)
response.raise_for_status()
stock_data = response.json()
yesterday_stock = float(stock_data['Time Series (Daily)'][yesterday]['4. close'])

# TODO 2. - Get the day before yesterday's closing stock price
previous_day_stock = float(stock_data['Time Series (Daily)'][previous_day]['4. close'])

# TODO 3. - Find the positive difference between 1 and 2. e.g. 40 - 20 = -20, but the positive difference is 20.
#  Hint: https://www.w3schools.com/python/ref_func_abs.asp
difference = yesterday_stock - previous_day_stock
up_down = ""
if difference > 0:
    up_down = "🔺"
else:
    up_down = "🔻"

# TODO 4. - Work out the percentage difference in price between closing price yesterday and closing price the
#  day before yesterday.
percentage_diff = round(((difference / yesterday_stock) * 100), 2)

# TODO 5. - If TODO4 percentage is greater than 5 then print("Get News").
if abs(percentage_diff) > 5:
    print("Get News")
    # # STEP 2: https://newsapi.org/
    # Instead of printing ("Get News"), actually get the first 3 news pieces for the COMPANY_NAME.
    # TODO 6. - Instead of printing ("Get News"), use the News API to get articles related to the COMPANY_NAME.
    response = requests.get(url=NEWS_ENDPOINT, params=news_parameter)
    response.raise_for_status()
    news_data = response.json()
    # TODO 7. - Use Python slice operator to create a list that contains the first 3 articles.
    #  Hint: https://stackoverflow.com/questions/509211/understanding-slice-notation
    news_list = news_data['articles'][:3]

    # # STEP 3: Use twilio.com/docs/sms/quickstart/python
    # to send a separate message with each article's title and description to your phone number.

    # TODO 8. - Create a new list of the first 3 article's headline and description using list comprehension.
    # Optional TODO: Format the message like this:
    """
    TSLA: 🔺2%
    Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
    Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to 
    file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height
     of the coronavirus market crash.
    or
    "TSLA: 🔻5%
    Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
    Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to 
    file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height
     of the coronavirus market crash.
    """
    formatted_article = [f"{COMPANY_NAME}: {up_down}{percentage_diff}% \n" 
                      f"Headline: {news['title']}\n" 
                      f"Brief: {news['description']}" for news in news_list]
    print(formatted_article)
    # TODO 9. - Send each article as a separate message via Twilio.
    account_sid = os.environ['TWILIO_ACCOUNT_SID']
    auth_token = os.environ['TWILIO_AUTH_TOKEN']
    client = Client(account_sid, auth_token)
    for article in formatted_article:
        message = client.messages \
            .create(
            body=article,
            from_='+15017122661',
            to='+15558675310'
        )

    print(message.sid)

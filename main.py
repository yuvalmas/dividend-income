import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

import sys, os
import math
import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
from termcolor import colored

os.system('cls' if os.name == 'nt' else 'clear')
print(colored("This program will calculate and compare the value of a stock with DRIP, and without DRIP to show the difference in value over time.", "blue"))
print()
print()
# get a number of years
years = input("Enter number of years: ")
while (years.isnumeric() == False or int(years) < 1):
    print("Please enter a valid number of years")
    years = input("Enter number of years: ")
# get a stock ticker
years = int(years)
stock = input("Enter stock ticker: ")

# get start and end dates
start = (datetime.now() - timedelta(days=365*years)).strftime('%Y-%m-%d')
end = (datetime.now()).strftime('%Y-%m-%d')

# get the price of stock x years ago and calculate number of shares
price = yf.Ticker(stock).history(start=start, end=end).iloc[0]['Close']

money = input("Enter amount of money to invest: ")
while (money.isdigit() == False or int(money) < price):
    print("Please enter a valid amount of money that can buy at least one share of the stock")
    money = input("Enter amount of money to invest: ")

money = int(money)
shares = math.floor(money / price)

try: 
    series = yf.Ticker(stock).dividends.loc[start:end]
    print(series[0])
except:
    print("No dividends found for this stock")
    # end the program
    exit(1)

print("Calculating...")
# loop through the series and add all dividends
dividends = 0
cashLeft = money - (shares * price)
# create a dataframe for the dates and worth of dividends
df = pd.DataFrame(columns=['Date', 'Dividend', 'Worth'])

dripValue = 0

for date, dividend in series.items():
    # conert date to string
    date = date.strftime('%Y-%m-%d')
    # get end date
    end = (pd.to_datetime(date) + timedelta(days=1)).strftime('%Y-%m-%d')
    # multiply number of shares by dividend
    dividends = dividends + (dividend * shares)    # get the price of the stock on the date of the dividend
    price = yf.Ticker(stock).history(start=date, end=end).iloc[0]['Close']
    # calculate the worth of the dividend
    worth = (price*shares) + dividends    
    # add dividend to cash left
    cashLeft = cashLeft + (dividend * shares)
    newShares = shares
    # calculate if can buy more shares
    if (cashLeft>price):
        newShares = math.floor(cashLeft/price)
        cashLeft = cashLeft - (math.floor(cashLeft/price))
        newShares = newShares + shares
    dripValue = (price*newShares)+cashLeft
    # add the date, dividend and worth to the dataframe
    df = df.append({'Date': date, 'Dividend': dividend, 'Dividends': worth, 'cashLeft': (dividends+cashLeft), "price": (price*shares), "dripValue": dripValue}, ignore_index=True)


# set the x graph axis to the dates
x = df['Date']
# set the y graph axis to the worth
worth = df['Dividends']
price = df['price']
dripValue = df['dripValue']
# plot the graph
fig, ax = plt.subplots()
ax.plot(x, worth, label='Drip Value')
ax.plot(x, price, label='Stock Price')
ax.plot(x, dripValue, label='With Dividends')
plt.xlabel("Date", labelpad=10)
plt.ylabel("Worth", labelpad=10)
plt.title("DRIP vs Dividends vs Stock price", pad=10)
plt.xticks(rotation=90)
ax.yaxis.set_major_formatter('${x:,.2f}')
# show the graph
plt.legend()
plt.show()

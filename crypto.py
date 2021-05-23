import cryptocompare
from datetime import datetime
from matplotlib import pyplot as plt
import time

COIN = 'DOGE'
CURRENCY = 'USD'

def init_plot():
    plt.title(f'{COIN}/{CURRENCY}\nPrice: {current_price} USD\nChange: {round(change_percent(P[-2], P[-1]), 2)}%\n24h change: {round(change_percent(P[0], P[-1]), 2)}%')
    plt.xlim(-50, len(T)+200)
    plt.xlabel('Time [day]')
    plt.ylabel('Price [USD]')
    plt.ion()

def get_history(coin, currency):
    prices = []
    times = []
    price_history = cryptocompare.get_historical_price_minute(coin, currency)
    #price_history = price_history[1260:]

    for dic in range(len(price_history)):
        times.append(datetime.utcfromtimestamp(price_history[dic]['time']).strftime('%m.%d. %H:%M'))
        prices.append(price_history[dic]['close'])

    return prices, times

def plot_prices(price_lst, time_lst):
    plt.xticks(ticks=[0, len(price_lst)], labels=[time_lst[0], time_lst[-1]])
    if change_percent(price_lst[-2], price_lst[-1]) >= 0:
        plt.plot(price_lst, 'g')
    else:
        plt.plot(price_lst, 'r')

def change_percent(prev, curr):
    return round(100*(curr-prev)/prev, 6)

def price_text(price_lst, time_lst, current_price):
    plt.text(len(time_lst), price_lst[-1], str(current_price) + '$')
    max_price = max(price_lst)
    min_price = min(price_lst)
    plt.text(price_lst.index(max_price), price_lst[price_lst.index(max_price)], str(max_price) + '$')
    plt.text(price_lst.index(min_price), price_lst[price_lst.index(min_price)], str(min_price) + '$')

P, T = get_history(COIN, CURRENCY)

while True:
    current_price = cryptocompare.get_price(COIN, CURRENCY)[COIN][CURRENCY]

    P.append(current_price)
    T.append(datetime.now().strftime('%m.%d. %H:%M'))
    P.pop(0); T.pop(0)

    init_plot()
    price_text(P, T, current_price)
    plot_prices(P, T)
    plt.draw()
    plt.pause(60)
    plt.clf()

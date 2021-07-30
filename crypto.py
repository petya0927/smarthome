import cryptocompare
from datetime import datetime
from cryptocompare.cryptocompare import CURRENCY
from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter
from tkinter import Canvas, ttk
import time

def config_plot(ax, coin, currency, current_price, price_lst, time_lst):
    ax.set_title(f'{coin}/{currency}\nPrice: {current_price} USD\nChange: {round(change_percent(price_lst[-2], price_lst[-1]), 2)}%\n24h change: {round(change_percent(price_lst[0], price_lst[-1]), 2)}%' + str(time.strftime('%H:%M')))
    ax.set_xticks(ticks=[0, len(price_lst)// 2, len(price_lst)]) 
    ax.set_xticklabels([time_lst[0], time_lst[len(price_lst) // 2], time_lst[-1]])
    ax.set_xlabel('Time [day]')
    ax.set_ylabel(f'Price [{currency}]')

def get_history(coin, currency):
    prices, times = [], []
    price_history = cryptocompare.get_historical_price_minute(coin, currency)
    # price_history = price_history[1260:]

    yesterday = int(time.time()) - 86400
    for dic in range(len(price_history)):
        times.append(datetime.fromtimestamp(yesterday + dic * 60).strftime('%m.%d. %H:%M'))
        prices.append(price_history[dic]['close'])

    return prices, times

def plot_prices(ax, price_lst):
    if change_percent(price_lst[0], price_lst[-1]) >= 0:
        ax.plot(price_lst, 'g')
    else:
        ax.plot(price_lst, 'r')

def change_percent(prev, curr):
    return 100*(curr-prev)/prev

def price_text(ax, price_lst, time_lst, current_price):
    ax.text(len(time_lst), price_lst[-1], str(current_price) + '$')
    max_price = max(price_lst)
    min_price = min(price_lst)
    ax.text(price_lst.index(max_price), price_lst[price_lst.index(max_price)], str(max_price) + '$')
    ax.text(price_lst.index(min_price), price_lst[price_lst.index(min_price)], str(min_price) + '$')

def plot_ui(root, fig):
    from main_menu import Main_menu

    [child.destroy() for child in root.winfo_children()]
    root.grid()
    # root.grid_rowconfigure(0, weight=1)
    # root.grid_rowconfigure(1, weight=1)
    # root.grid_columnconfigure(0, weight=1)
    # root.grid_columnconfigure(1, weight=1)
    # root.grid_columnconfigure(2, weight=1)

    canvas = FigureCanvasTkAgg(fig, root)
    canvas.get_tk_widget().grid()

    mainmenu_button = tkinter.Button(root, text='Main menu', command= lambda: Main_menu.menu_ui(root))
    mainmenu_button.grid()

def plotting(fig, ax, coin, currency):

    current_price = cryptocompare.get_price(coin, currency)[coin][currency]
    prices, times = get_history(coin, currency)

    ax.cla()
    config_plot(ax, coin, currency, current_price, prices, times)
    price_text(ax, prices, times, current_price)
    plot_prices(ax, prices)
    fig.canvas.draw()

    root.after(60000, lambda: plotting(fig, ax, coin, currency))

def main(root, coin, currency):
    print(coin, currency)
    fig, ax = plt.subplots()
    plot_ui(root, fig)

    plotting(fig, ax, coin, currency)

    root.mainloop()

if __name__ == '__main__':
    root = tkinter.Tk()
    COIN = 'DOGE'
    CURRENCY = 'USD'
    main(root, COIN, CURRENCY)
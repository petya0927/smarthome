import tkinter
from tkinter import ttk
import crypto

COINS = [
    'BTC',
    'DOGE',
    'XRP',
    'ADA']

CURRENCIES = [
    'USD',
    'EUR',
    'HUF']

coin_choosed, currency_choosed = False, False

def change_coin(value):
    global COIN
    global coin_choosed
    COIN = value
    coin_choosed = True
    print(COIN, coin_choosed)
    return COIN, coin_choosed

def change_curr(value):
    global CURRENCY
    global currency_choosed
    CURRENCY = value
    currency_choosed = True
    print(CURRENCY, currency_choosed)
    return CURRENCY, currency_choosed

def choose_coin(root):

    [child.destroy() for child in root.winfo_children()]
    root.grid()
    canvas = tkinter.Canvas(root)
    canvas.grid()

    for coin_opt in range(len(COINS)):
        btn = ttk.Button(canvas, text=COINS[coin_opt], command=None)
        btn.grid(row=coin_opt, column=0)
        btn['command'] =  lambda btn=btn: [change_coin(btn['text']), crypto.main(root, COIN, CURRENCY) if currency_choosed and coin_choosed else None]

    for currency_opt in range(len(CURRENCIES)):
        btn = ttk.Button(canvas, text=CURRENCIES[currency_opt], command=None)
        btn.grid(row=currency_opt, column=1)
        btn['command'] = lambda btn=btn: [change_curr(btn['text']), crypto.main(root, COIN, CURRENCY) if currency_choosed and coin_choosed else None]

    #tkinter.Button(root, text='Plot!', command=lambda: crypto.main(root, COIN, CURRENCY)).grid()

def main(root):
    choose_coin(root)
    root.mainloop()

if __name__ == '__main__':
    root = tkinter.Tk()
    main(root)
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

def change_coin(value):
    global COIN
    COIN = value
    return COIN

def change_curr(value):
    global CURRENCY
    CURRENCY = value
    return CURRENCY

def choose_coin(root):

    [child.destroy() for child in root.winfo_children()]
    root.grid()
    canvas = tkinter.Canvas(root)
    canvas.grid()

    for coin_opt in COINS:
        btn = ttk.Button(canvas, text=coin_opt, command=None)
        btn.grid()
        btn['command'] = lambda btn=btn: change_coin(btn['text'])

    for currency_opt in CURRENCIES:
        btn = ttk.Button(canvas, text=currency_opt, command=None)
        btn.grid()
        btn['command'] = lambda btn=btn: change_curr(btn['text'])

    tkinter.Button(root, text='Plot!', command=lambda:crypto.main(root, COIN, CURRENCY)).grid()

def main(root):
    choose_coin(root)
    root.mainloop()

if __name__ == '__main__':
    root = tkinter.Tk()
    main(root)
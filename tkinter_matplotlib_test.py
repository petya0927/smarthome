from bs4 import element
from matplotlib import figure
import matplotlib
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import tkinter as tk

def main_menu(root):
    root.attributes('-fullscreen', True)
    exit_button = tk.Button(root, text='Exit', command=exit)
    exit_button.grid(row=1, column=0, sticky="NSEW")

    update_button = tk.Button(root, text='Update')
    update_button.grid(row=2, column=0, sticky="NSEW")

    rain_button = tk.Button(root, text='Rain data', command=lambda: rain_plot(root))
    rain_button.grid(row=3, column=0, sticky="NSEW")

# DATA AND PLOTTING
def rain_plot(root):
    [child.destroy() for child in root.winfo_children()]

    fig, ax = plt.subplots()

    plot_ui(root, fig)

    x = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
    y = [4, 7, 1, 4, 8, 5, 2, 5, 2, 6, 7, 9]

    bar = ax.bar(x, y)
    ax.set_xlabel('Days')
    ax.set_ylabel('Rain [mm]')

    for rect in bar:
        height = rect.get_height()
        ax.text(rect.get_x() + rect.get_width()/2., 1.05*height, int(height))

# UI INIT AND SETUP
def plot_ui(root, fig):
    root.grid()
    root.grid_rowconfigure(0, weight=1)
    root.grid_rowconfigure(1, weight=1)
    root.grid_columnconfigure(0, weight=1)
    root.grid_columnconfigure(1, weight=1)
    root.grid_columnconfigure(2, weight=1)

    canvas = FigureCanvasTkAgg(fig, root)
    canvas.get_tk_widget().grid(row=0, columnspan=3, sticky="NSEW")

    exit_button = tk.Button(root, text='Exit', command=exit)
    exit_button.grid(row=1, column=0, sticky="NSEW")

    update_button = tk.Button(root, text='Update')
    update_button.grid(row=1, column=1, sticky="NSEW")

    next_button = tk.Button(root, text='Next', command=exit)
    next_button.grid(row=1, column=2, sticky="NSEW")


root = tk.Tk()
win_width = root.winfo_screenwidth() 
win_height = root.winfo_screenheight()

main_menu(root)

root.mainloop()
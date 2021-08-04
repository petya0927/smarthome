import tkinter
from weather import Weather
import choose_crypto
import subprocess

def update():
    subprocess.Popen(['python', 'update_script.py'])
    exit()

class Main_menu():

    def menu_ui(root):
        [child.destroy() for child in root.winfo_children()]
        Main_menu.ui_config(root)

        temp_button = tkinter.Button(root, text='Temperature data', command=lambda: Weather.temp_plot(root))
        temp_button.grid(sticky="NSEW")

        rain_button = tkinter.Button(root, text='Rain data', command=lambda: Weather.rain_plot(root))
        rain_button.grid(sticky="NSEW")

        crypto_button = tkinter.Button(root, text='Actual crypto price', command=lambda: choose_crypto.main(root))
        crypto_button.grid(sticky="NSEW")

        update_button = tkinter.Button(root, text='Update application', command='')
        update_button.grid(sticky="NSEW")

        exit_button = tkinter.Button(root, text='Exit application', command=exit)
        exit_button.grid(sticky="NSEW")

    def ui_config(root):
        #root.attributes('-fullscreen', True)
        win_width = root.winfo_screenwidth()
        win_height = root.winfo_screenheight()

    def main():
        root = tkinter.Tk()
        Main_menu.menu_ui(root)
        root.mainloop()

if __name__ == '__main__':
    Main_menu.main()
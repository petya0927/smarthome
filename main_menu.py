import tkinter
import weather
import subprocess

def update():
    subprocess.Popen(['python3', 'update_script.py'])
    exit()

def main_menu(root):
    [child.destroy() for child in root.winfo_children()]

    temp_button = tkinter.Button(root, text='Temperature data', command=lambda: weather.temp_plot(root))
    temp_button.grid(sticky="NSEW")

    rain_button = tkinter.Button(root, text='Rain data', command=lambda: weather.rain_plot(root))
    rain_button.grid(sticky="NSEW")

    update_button = tkinter.Button(root, text='Update', command=update)
    update_button.grid(sticky="NSEW")

    exit_button = tkinter.Button(root, text='Exit', command=exit)
    exit_button.grid(sticky="NSEW")

root = tkinter.Tk()
win_width = root.winfo_screenwidth()
win_height = root.winfo_screenheight()
#root.attributes('-fullscreen', True)

main_menu(root)

root.mainloop()
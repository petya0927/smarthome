from matplotlib import pyplot as plt
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import os
import tkinter
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
import subprocess
import sys

mainpage = requests.get('https://www.idokep.hu/idojaras/Szada')
soup = BeautifulSoup(mainpage.content, 'html.parser')

def actual_weather():
    act_desc = soup.find(class_='ik current-weather-short-desc d-block d-md-inline ml-md-2 mt-2 mt-xl-0').get_text().strip()
    act_shortdesc = soup.find(class_='ik current-weather').get_text().strip()
    act_temp = soup.find(class_='ik current-temperature').get_text().strip()
    act_icon = soup.find(class_='ik forecast-bigicon pr-2 pd-md-0')['src']

    return act_desc, act_shortdesc, act_temp, act_icon

def main_maps():
    url = requests.get('https://www.idokep.hu/idojaras/Szada')
    soup = BeautifulSoup(url.content, 'html.parser')

    weather_map = soup.find(id='ik-cur-weather-nav-idokep').find(class_='img-fluid w-100')['src']
    cloud_map = soup.find(id='ik-cur-weather-nav-felhokep').find(class_='img-fluid w-100')['src']
    heat_map = soup.find(id='ik-cur-weather-nav-hoterkep').find(class_='img-fluid w-100')['src']
    return weather_map, cloud_map, heat_map

def radar_maps():
    url = requests.get('https://www.idokep.hu/radar')
    soup = BeautifulSoup(url.content, 'html.parser')

    video = soup.find(class_='video w-100').find(type='video/mp4')['src']
    warning_3hour = soup.find(title='1-3 órás riasztás')['src']
    warning_midnight = soup.find(title='Mára szóló figyelmeztetés')['src']
    warning_tomorrow = soup.find(title='Holnapra szóló figyelmeztetés')['src']
    return video, warning_3hour, warning_tomorrow, warning_midnight

def rain_map():
    url = requests.get('https://www.idokep.hu/csapadek')
    soup = BeautifulSoup(url.content, 'html.parser')
    return soup.find(class_='pb-4 img-fluid')['src']

def pressure_map():
    url = requests.get('https://www.idokep.hu/legnyomas')
    soup = BeautifulSoup(url.content, 'html.parser')
    return soup.find(class_='pb-4 ik max970')['src']

def min_max_map():
    url = requests.get('https://www.idokep.hu/minmax')
    soup = BeautifulSoup(url.content, 'html.parser')
    return soup.find(class_='pb-4 img-fluid').find(name='tmax')['src'], soup.find(class_='pb-4 img-fluid').find(name='tmin')['src']

def nextday_hourly():
    forecastpage = requests.get('https://www.idokep.hu/elorejelzes/Szada')
    fsoup = BeautifulSoup(forecastpage.content, 'html.parser')
    #div = list(list(list(list(list(list(list(list(list(list(fsoup.children)[2].children)[3].children)[17].children)[1].children)[1].children)[3].children)[1].children)[3].children)[1].children)[5]
    div = fsoup.find(class_='ik hourly-forecast-card-container')

    winds, rain_chances, rains = [], [], []

    for div_i in range(1, len(list(div.children))-1, 2):
        act = list(div.children)[div_i]

        wind_data = list(list(list(act.children)[7].children)[1].children)[0]['class']
        wind = [wind_data[2], wind_data[3][1:]]

        rain_cont = act.find(class_='ik hourly-rainlevel-container')
        if rain_cont == None:
            rain = '0 mm'
        elif rain_cont != None:
            rain = list(rain_cont.find(class_='ik hourly-rainlevel').children)[1]

        rain_chance_cont = act.find(class_='ik hourly-rain-chance')
        if rain_chance_cont == None:
            rain_chance = '0%'
        elif rain_chance_cont != None:
            rain_chance = rain_chance_cont.find(class_='interact').get_text()

        winds.append(wind)
        rain_chances.append(rain_chance)
        rains.append(rain)

    times = [time.get_text().strip() for time in fsoup.find_all(class_='ik hourly-forecast-hour')]
    data_descs = [temp['data-content'] for temp in fsoup.select('.interact')]
    temps = [int(temp.get_text().strip()) for temp in fsoup.find_all(class_='ik temperature-circled flex-v-m mx-auto')]
    icons = [temp['src'] for temp in fsoup.find_all(class_='ik forecast-icon')]

    return times[:24], temps[:24], winds[:24], rain_chances[:24], rains[:24], data_descs[:24], icons[:24]

def text_forecast():
    forecastpage = requests.get('https://www.idokep.hu/elorejelzes/Szada')
    fsoup = BeautifulSoup(forecastpage.content, 'html.parser')
    #text_container = fsoup.find(class_='ik hosszutavu-elorejelzes m-sm-4 p-4 rounded-soft').select('div')
    text_container = list(fsoup.find(style='position: relative; left:0;top:0; z-index: 99999; display: block;').children)
    title = text_container[1].get_text()
    today = text_container[3].get_text()
    tomorrow = list(filter(None, text_container[5].get_text().split('\n')))[0].strip()
    after = list(filter(None, text_container[5].get_text().split('\n')))[1].strip()
    return title, today, tomorrow, after

def get_sun_data():
    sun = soup.find(class_='col-6 col-sm-8 col-md-12 pt-4 pt-md-2')
    sun_rise = sun.find(class_=None).get_text().strip()
    sun_set = sun.find(class_='pt-2').get_text().strip()
    return sun_rise, sun_set

def dwnld_pic(src_lst):

    today = datetime.now().strftime('%Y%m%d')
    base_url = 'https://www.idokep.hu/'
    
    if not os.path.exists('idokep_kepek_' + today):
        os.mkdir('idokep_kepek_' + today)

    directory = 'idokep_kepek_' + today
    
    if type(src_lst) == 'list':
        for src in src_lst:
            image = requests.get(base_url + src)
            filename = src.split('/')[-1]
            f = open(directory + '/' + filename, 'wb')
            f.write(image.content)
            f.close()
    else:
        image = requests.get(base_url + src_lst)
        filename = src_lst.split('/')[-1]
        f = open(directory + '/' + filename, 'wb')
        f.write(image.content)
        f.close()

def plot_text(plot, times, temps):
    for point in range(len(times)):
        plot.text(times[point], temps[point], f'{temps[point]} C°')

def init_tkinter():
    root = tkinter.Tk()
    root.title('Weather widget')

    fig = Figure(figsize=(5, 4), dpi=100)

    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.draw()
    
    toolbar = NavigationToolbar2Tk(canvas, root, pack_toolbar=False)
    toolbar.update()

    return root, fig, canvas

def update():
    subprocess.Popen(['python', 'update_script.py'])
    sys.exit(0)

# INIT
root, fig, canvas = init_tkinter()
times, temps, winds, rain_chances, rains, data_descs, icons = nextday_hourly()

temp_plot = fig.add_subplot()

# PLOTTING
plot_text(temp_plot, times, temps)
temp_plot.plot(times, temps, '-o', linewidth=3)
plt.xticks([0, len(temps)])

# BUTTONS
update_button = tkinter.Button(root, text='Update', command=update)
quit_button = tkinter.Button(root, text="Quit", command=root.quit)

# PACKING
update_button.pack(side=tkinter.TOP)
quit_button.pack(side=tkinter.TOP)
canvas.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)
tkinter.mainloop()
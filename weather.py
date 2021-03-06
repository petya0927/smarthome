# -*- coding: utf-8 -*-
from choose_crypto import main
from tkinter.constants import BOTH, BOTTOM, CENTER, TOP
from matplotlib import pyplot as plt
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import os
import tkinter
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class Weather():

    __test__ = False

    def actual_weather():
        mainpage = requests.get('https://www.idokep.hu/idojaras/Szada')
        soup = BeautifulSoup(mainpage.content, 'html.parser')

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
        # INIT 
        forecastpage = requests.get('https://www.idokep.hu/elorejelzes/Szada')
        fsoup = BeautifulSoup(forecastpage.content, 'html.parser')
        
        # FIND CARD CONTAINER
        div = list(fsoup.find(class_='ik new-hourly-forecast-card-container'))
        del div[::2]

        winds, rain_chances, rains = [], [], []

        for card_div in div:

            #WIND
            wind_data = card_div.select('div .ik .wind')[0]['class']
            wind = [wind_data[2], int(wind_data[3][1:])]

            # RAIN
            rain_cont = card_div.find(class_='ik hourly-rainlevel-container')
            if rain_cont == None:
                rain = '0 mm'
            elif rain_cont != None:
                rain = list(rain_cont.find(class_='ik hourly-rainlevel').children)[1]

            # RAIN CHANCE
            rain_chance_cont = card_div.find(class_='ik hourly-rain-chance')
            if rain_chance_cont == None:
                rain_chance = '0%'
            elif rain_chance_cont != None:
                rain_chance = rain_chance_cont.find(class_='interact').get_text()

            # APPEND TO LISTS
            winds.append(wind)
            rains.append(rain)
            rain_chances.append(rain_chance)

        # GET OTHER DATA
        times = [time.get_text().strip() for time in fsoup.find_all(class_='ik new-hourly-forecast-hour')]
        data_descs = [temp['data-content'] for temp in fsoup.select('.interact')]
        temps = [int(temp.get_text().strip()) for temp in fsoup.find_all(class_='ik hover-over d-block') if temp.get_text().strip() != '']
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
        url = requests.get('https://www.idokep.hu/idojaras/Szada')
        soup = BeautifulSoup(url.content, 'html.parser')

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

    def test():
        times = [1, 2, 3, 4, 5]
        temps = [20, 25, 23, 26, 21]
        winds = [['gyenge', 84], ['gyenge', 88], ['mérsékelt', 152], ['gyenge', 213], ['erős', 130]]
        rain_chances = ['0%', '10%', '20%', '50%', '80%']
        rains = ['0 mm', '1 mm', '1 mm', '3 mm', '7 mm']
        data_descs = []
        icons = []
        return times, temps, winds, rain_chances, rains, data_descs, icons

    def plot_ui(root, fig):

        from main_menu import Main_menu

        root.grid()
        root.grid_rowconfigure(0, weight=1)
        root.grid_rowconfigure(1, weight=1)
        root.grid_columnconfigure(0, weight=1)
        root.grid_columnconfigure(1, weight=1)

        canvas = FigureCanvasTkAgg(fig, root)
        canvas.get_tk_widget().pack(fill=BOTH, expand=True)

        mainmenu_button = tkinter.Button(root, text='Main menu', command=lambda: Main_menu.menu_ui(root))
        mainmenu_button.pack(fill=BOTH)

    def temp_plot(root):
        [child.destroy() for child in root.winfo_children()]
        fig, ax = plt.subplots()
        Weather.plot_ui(root, fig)

        if Weather.__test__:
            times, temps, winds, rain_chances, rains, data_descs, icons = Weather.test()
        else:   
            times, temps, winds, rain_chances, rains, data_descs, icons = Weather.nextday_hourly()

        ax.plot(times, temps)
        for point in range(len(times)):
            ax.text(times[point], temps[point], str(temps[point]))

    def rain_plot(root):
        [child.destroy() for child in root.winfo_children()]
        fig, ax = plt.subplots()
        Weather.plot_ui(root, fig)

        if Weather.__test__:
            times, temps, winds, rain_chances, rains, data_descs, icons = Weather.test()
        else:   
            times, temps, winds, rain_chances, rains, data_descs, icons = Weather.nextday_hourly()

        rains_data = [int(i[:-3]) for i in rains]

        ax.bar(times, rains_data)
        ax.set_xlabel('Days')
        ax.set_ylabel('Rain [mm]')
        
        for i, v in enumerate(rains_data):
            ax.text(i+1, v, str(v))

if __name__ == '__main__':
    root = tkinter.Tk()
    Weather.temp_plot(root)
    root.mainloop()
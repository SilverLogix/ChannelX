# Retro Winnipeg Weather Channel
# By probnot
# Revisions by DamagedDolphin
# Remaster by Faxanidu

import os
import asyncio
import urllib.request
import gc
import json
import time
from tkinter import Canvas, Tk, Label

import timeit

from Setup import *
from Observations import loadWeather, getWeather
from News import loadNews
from Alert import weatherAlerts

fontSet = "VCR OSD Mono"

loadWeather()
weatherAlerts()
#print('loadWeather()\t\t', timeit.timeit(loadWeather, number=1))
#print('weatherAlerts()\t\t', timeit.timeit(weatherAlerts, number=1))

#  Setup variables
alertValue = 0
dayValue = 0
data = 0


#  US WEATHER FORECAST LOADER, CHANGE VALUES IN SETUP.PY

def forecast():
    urllib.request.urlretrieve(obsUrl, 'weatherForecast.json')
    global data
    with open('weatherForecast.json') as json_file:
        data = json.load(json_file)


def forecastCount(isDayValue):
    isDayValue = isDayValue + 1
    try:
        data['time']['startPeriodName'][isDayValue]
    except:
        isDayValue = 0
    return isDayValue


### US WEATHER ALERT LOADER, CHANGE VALUES IN SETUP.PY

def alertCount(isAlertValue):
    isAlertValue = isAlertValue + 1
    try:
        weatherAlert[isAlertValue]
    except:
        isAlertValue = 0
    return isAlertValue


def clock():
    current = time.strftime("%a %b %d %G          %r")
    timeText.configure(text=current.upper())
    root.after(1000, clock)  # run every 1sec

### CHANGE IN SETUP.PY
if loadMusic == 1:
    os.system('nohup mpg321 --loop 0 --list playlist.lst &')

# main weather pages
### LOAD FORECAST AND RELOAD EVERY HOUR
forecast()


def weather_page():
    global dayValue
    global alertValue
    global weatherAlert
    checkTime = time.gmtime()[4]

    if checkTime == 0:
        loadWeather()
        forecast()

    ### THIS SECTION DISPLAYS WEATHER FORECAST INFORMATION
    # pull in current seconds and minutes -- to be used to cycle the middle section every 30sec
    time_sec = time.localtime().tm_sec
    time_min = time.localtime().tm_min

    if time_sec < 30:
        weathercol = "Blue"
        if (time_min % 2) == 0:  # screen 1 -- today's forecast in text + start of tomorrow's forecast
            dayString = data['time']['startPeriodName'][dayValue]
            tempLabel = data['time']['tempLabel'][dayValue]
            tempString = str(data['data']['temperature'][dayValue])
            textString = data['data']['text'][dayValue]
            s = dayString + " " + tempLabel + " " + tempString + " " + textString + "\n"
            s = s.upper()
            s1 = s[:47]
            s2 = s[47:94]
            s3 = s[94:141]
            s4 = s[141:188]
            s5 = s[188:235]
            s6 = s[235:282]
            s7 = s[282:329]
            s8 = s[329:376]
            dayValue = forecastCount(dayValue)

        ### THIS SECTION DISPLAYS WEATHER CURRENT CONDITIONS
        else:
            weatherLocation, weatherLastObs, weatherSkyConds, weatherTemp, weatherDewpoint, weatherFeelsLike, weatherWinds, weatherGusts, weatherHumidity, weatherBarometer, weatherVisibility, weatherCredit = getWeather()
            s1 = weatherLocation.upper()
            s2 = weatherLastObs.upper()
            s3 = "TEMP " + weatherTemp.upper() + " FEELS LIKE " + weatherFeelsLike.upper()
            s4 = "WIND " + weatherWinds.upper() + "  VISIBILITY " + weatherVisibility.upper()
            s5 = "HUMIDITY " + weatherHumidity.upper() + "  DEWPOINT " + weatherDewpoint.upper()
            s6 = "PRESSURE " + weatherBarometer.upper()
            s7 = ""
            s8 = weatherCredit.upper()
    if time_sec >= 30:
        ### US WEATHER ALERT CHECKING SECTION *** DO NOT MODIFY ***

        weatherAlert = weatherAlerts()
        alertCheck = ""
        try:
            alertCheck = weatherAlert[alertValue].upper()
        except:
            alertCheck = "ERROR CHECKING FOR WEATHER ALERTS - PLEASE CHECK YOUR LOCAL FORECAST OFFICE"
        ### IF ACTIVE WEATHER ALERTS WEATHER FORECAST AND WEATHER ALERT SHOWN
        if alertCheck != "NONE":
            weathercol = "Purple"
            if (time_min % 2) == 0:  # screen 2 -- next day forecast cont'd + 3rd day
                dayString = data['time']['startPeriodName'][dayValue]
                tempLabel = data['time']['tempLabel'][dayValue]
                tempString = str(data['data']['temperature'][dayValue])
                textString = data['data']['text'][dayValue]
                s = dayString + " " + tempLabel + " " + tempString + " " + textString + "\n"
                s = s.upper()
                s1 = s[:47]
                s2 = s[47:94]
                s3 = s[94:141]
                s4 = s[141:188]
                s5 = s[188:235]
                s6 = s[235:282]
                s7 = s[282:329]
                s8 = s[329:376]
                dayValue = forecastCount(dayValue)
            else:  # ACTIVE WEATHER ALERT MESSAGE
                weathercol = "Red"
                s = alertCheck
                s1 = s[:47]
                s2 = s[47:94]
                s3 = s[94:141]
                s4 = s[141:188]
                s5 = s[188:235]
                s6 = s[235:282]
                s7 = s[282:329]
                s8 = s[329:376]
                alertValue = alertCount(alertValue)
        else:
            ### IF NO ACTIVE WEATHER ALERTS ONLY WEATHER FORECAST SHOWN
            weathercol = "Purple"
            dayString = data['time']['startPeriodName'][dayValue]
            tempLabel = data['time']['tempLabel'][dayValue]
            tempString = str(data['data']['temperature'][dayValue])
            textString = data['data']['text'][dayValue]
            s = dayString + " " + tempLabel + " " + tempString + " " + textString + "\n"
            s = s.upper()
            s1 = s[:47]
            s2 = s[47:94]
            s3 = s[94:141]
            s4 = s[141:188]
            s5 = s[188:235]
            s6 = s[235:282]
            s7 = s[282:329]
            s8 = s[329:376]
            dayValue = forecastCount(dayValue)
    # create the canvas for middle page text

    weather = Canvas(root, height=270, width=800, bg=weathercol)
    weather.place(x=0, y=100)
    weather.config(highlightbackground=weathercol)

    # place the 8 lines of text
    weather.create_text(15, 15, anchor='nw', text=s1, font=(fontSet, 20, "bold"), fill="white")
    weather.create_text(15, 45, anchor='nw', text=s2, font=(fontSet, 20, "bold"), fill="white")
    weather.create_text(15, 75, anchor='nw', text=s3, font=(fontSet, 20, "bold"), fill="white")
    weather.create_text(15, 105, anchor='nw', text=s4, font=(fontSet, 20, "bold"), fill="white")
    weather.create_text(15, 135, anchor='nw', text=s5, font=(fontSet, 20, "bold"), fill="white")
    weather.create_text(15, 165, anchor='nw', text=s6, font=(fontSet, 20, "bold"), fill="white")
    weather.create_text(15, 195, anchor='nw', text=s7, font=(fontSet, 20, "bold"), fill="white")
    weather.create_text(15, 225, anchor='nw', text=s8, font=(fontSet, 20, "bold"), fill="white")

    root.after(30000, weather_page)  # re-run every 30sec from program launch


# setup main stuff

root = Tk()
root.attributes('-fullscreen', fullScreen)
root.geometry(screenSize)  # Change in Setup.py
root.config(cursor="none", bg="green")
root.wm_title("Channel 3")

# Clock - Top RIGHT

timeText = Label(root, text="", font=(fontSet, 20), fg="white", bg="green")
timeText.place(x=335, y=40)
clock()

# Title - Top LEFT

Title = Label(root, text=cableCo, font=(fontSet, 20), fg="white", bg="green")
Title.place(x=20, y=40)

# Middle Section (Cycling weather pages, every 30sec)
weather_page()


# scrolling text canvas
def marqueeCreate():
    global marquee
    marquee = Canvas(root, height=120, width=760, bg="green")
    marquee.config(highlightbackground="green")
    marquee.place(x=20, y=420)


# read in RSS data and prepare it

width = 35
pad = ""
for r in range(width):  # create an empty string of 35 characters
    pad = pad + " "

### RSS FEED LOADER
### CHANGE VALUES IN SETUP.PY


def main():
    try:
        getNews
    except:
        getNews = loadNews()
        newsItem = ""
    while True:
        global marquee
        for item in getNews:
            try:
                marquee
            except:
                marqueeCreate()
            newsItem = item.upper() + pad

            # use the length of the news feeds to determine the total pixels in the scrolling section
            marquee_length = len(newsItem)
            pixels = marquee_length * 24  # roughly 24px per char

            # setup scrolling text

            text = marquee.create_text(1, 2, anchor='nw', text=pad + newsItem + pad, font=(fontSet, 25,), fill="white")

            for p in range(pixels + 601):
                marquee.move(text, -1, 0)  # shift the canvas to the left by 1 pixel
                marquee.update()
                time.sleep(0.005)  # scroll every 5ms

            del text
            del marquee
            gc.collect()

        if item == len(getNews):
            getNews = loadNews()
            del newsItem


if __name__ == '__main__':
   # main()
    print('main()\t\t', timeit.timeit(main, number=1))

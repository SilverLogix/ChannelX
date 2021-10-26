import json
import urllib.request
from Setup import obsUrl

urllib.request.urlretrieve(obsUrl, 'weatherForecast.json')

with open('weatherForecast.json') as json_file:
    data = json.load(json_file)

dictLen = len(data['time']) - 1
n = 0  # New line

for weatherData in data:
    dayString = data['time']['startPeriodName'][n]
    tempLabel = data['time']['tempLabel'][n]
    tempString = str(data['data']['temperature'][n])
    textString = data['data']['text'][n]
    weatherString = dayString + " " + tempLabel + " " + tempString + " " + textString + "\n"
    print(weatherString.upper())
    n = n + 1

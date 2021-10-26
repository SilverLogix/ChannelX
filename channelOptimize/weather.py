import feedparser

from Setup import weatherAlertCode
import json
import urllib.request
from Setup import obsUrl

# --------------------

alert = ""
alert_type = ""

# --------------------


def get_forcast():
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


def weatherAlerts():
    # Load URL from NOAA's National Weather Service weather alerts
    global alert
    global alert_type
    alert_items = []
    alert_return = []
    del alert_items[:]
    del alert_return[:]
    alert_feeds = [
        'https://alerts.weather.gov/cap/wwaatmget.php?x=' + weatherAlertCode + '&y=0'
    ]
    for url in alert_feeds:
        alert_feed = feedparser.parse(url)
        alerts = alert_feed["items"]
        for alert in alerts:
            alert_items.append(alert)
        for alert_item in alert_items:
            alert_text = alert_item["title"]
            alert_type = ""
            if "warning" in (alert["title"].lower()) or "warning" in (alert["summary"].lower()):
                alert_type = "warning"
            elif "advisory" in (alert["title"].lower()) or "advisory" in (alert["summary"].lower()):
                alert_type = "advisory"
            elif "watch" in (alert["title"].lower()) or "watch" in (alert["summary"].lower()):
                alert_type = "watch"
            else:
                alert_type = "other"
            # Check if "There are no active watches, warnings or advisories" does not exist
            if "There are no active watches, warnings or advisories" in alert_text:
                alert_return.append("NONE")
            else:
                alert_text = alert_item["title"] + " - " + alert_item["summary"]
                alert_return.append(alert_text)
        return alert_return

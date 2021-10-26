

# Download weather XML file from NWS, change location code in Setup.py
def loadWeather():
    import os
    import urllib.request
    from Setup import weatherObservationURL

    data = 0
    os.remove('weatherObservations.xml')


    urllib.request.urlretrieve(weatherObservationURL, 'weatherObservations.xml')
    # print("Removed and downloaded new observation file")


tree = ""
root = ""
weatherCredit = ""


def getWeather():
    from xml.etree.ElementTree import ElementTree
    global tree, weatherCredit, root
    tree = ElementTree(file='weatherObservations.xml')
    root = tree.getroot()

    # Parse XML tree into variables

    # Get Location Name
    weather_test = root.find('location')
    if weather_test is not None:
        observation_location = root.find('location').text
    else:
        observation_location = "Not Reported"

    # Get Last Update Info
    weather_test = root.find('observation_time')
    if weather_test is not None:
        observation_time = root.find('observation_time').text
    else:
        observation_time = "Unknown"

    # Get Sky Conditions
    weather_test = root.find('weather')
    if weather_test is not None:
        current_sky = root.find('weather').text
    else:
        current_sky = "Not Reported"

    # Get Last Reported Temperature
    weather_test = root.find('temperature_string')
    if weather_test is not None:
        current_temp = root.find('temperature_string').text
    else:
        current_temp = "Not Reported"

    # Get Last Reported Dewpoint
    weather_test = root.find('dewpoint_string')
    if weather_test is not None:
        current_dew = root.find('dewpoint_string').text
    else:
        current_dew = "Not Reported"

    # Get Last Reported Heat Indext - If not reported, use current temperature as feels like
    weather_test = root.find('heat_index_string')
    if weather_test is not None:
        current_heat_index = root.find('heat_index_string').text
    else:
        current_heat_index = root.find('temperature_string').text

    # Get Last Reported Winds and concatenate
    current_wind_dir = root.find('wind_dir')
    current_wind_spd = root.find('wind_mph')
    if current_wind_dir is not None and current_wind_spd is not None:
        current_wind = root.find('wind_dir').text
        current_wind = current_wind + " " + root.find('wind_mph').text + " mph"
    else:
        current_wind = "Not Reported"

    # Get Last Reported Wind Guests or if none Not Observed
    current_wind_gusts = root.find('wind_gust_mph')
    if current_wind_gusts is not None:
        current_wind_gusts = root.find('wind_gust_mph').text + " mph"
    else:
        current_wind_gusts = "Not Observed"

    # Get Last Reported Humidity
    current_humidity_test = root.find('relative_humidity')
    if current_humidity_test is not None:
        current_humidity = root.find('relative_humidity').text + " %"
    else:
        current_humidity = "Not Reported"

    # Get Last Reported Pressure in inHg and mb
    current_pressure_test = root.find('pressure_in')
    if current_pressure_test is not None:
        current_pressure = root.find('pressure_in').text + "\""
    else:
        current_pressure = "Not Reported"
    current_pressure_test = root.find('pressure_mb')
    if current_pressure_test is not None:
        current_pressure = current_pressure + " (" + root.find('pressure_mb').text + "mb)"

    # Get Last Reported Visibility
    current_visibility_test = root.find('visibility_mi')
    if current_visibility_test is not None:
        current_visibility = root.find('visibility_mi').text + " mi"
    else:
        current_visibility = "Not Reported"

    # Get Weather Source Info
    weather_credit_test = root.find('credit')
    if weather_credit_test is not None:
        weatherCredit = root.find('credit').text

    # Retun Values
    return (observation_location, observation_time, current_sky, current_temp, current_dew, current_heat_index,
            current_wind, current_wind_gusts, current_humidity, current_pressure, current_visibility, weatherCredit)

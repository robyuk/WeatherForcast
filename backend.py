from os import getenv
import requests
from time import strftime, gmtime
import pandas as pd
import streamlit as st


@st.cache_data
def get_openweather(place):
    """ Gets 5-day weather forecast data for a place from openweathermap.org"""
    API_KEY = getenv('OPENWEATHER_API_KEY')
    url = f'http://api.openweathermap.org/data/2.5/forecast?q={place}&units=metric&appid={API_KEY}'
    return requests.get(url).json()


def get_weather_data(openweather_data, days):
    """ Filters the 5-day weather forecast data from openweathermap.org
    Parameters:
        openweather_data: JSON string containing thw 5-day weather forecast data from openweathermap.org.
        days:             Integer between 1 and 5 inclusive, the number of days for which to return data
    Returns a pandas dataframe containing the filtered forecast data."""

    points = days * 8
    weather_data = openweather_data['list'][:points]
    return pd.DataFrame(
        [[i['main']['temp'],
          i['main']['pressure'],
          i['main']['humidity'],
          i['clouds']['all'],
          i['wind']['speed'],
          i['visibility'],
          i['weather'][0]['description'],
          i['weather'][0]['icon']
          ] for i in weather_data],
        [i['dt_txt'] for i in weather_data],
        columns=['Temperature (C)', 'Pressure (mB)', 'Humidity %', 'Clouds Cover (%)', 'Wind Speed (m/s)',
                 'Visibility (m)', 'Description', 'Sky Conditions']
    )


@st.cache_data
def get_openweathermap_icon(icon):
    """ Gets the image data for a weather icon"""
    url = f'http://openweathermap.org/img/w/{icon}.png'
    return requests.get(url).content


# Uncomment (Ctrl /) the next block to enable fake data for testing
# import numpy as np
# from datetime import datetime
# def get_fake_data(days):
#          weather_data = pd.DataFrame(
#              np.random.randn(days, 1),
#              index=[datetime(2023, 3, i) for i in range(1, days + 1)],
#              columns=['Temperature (C)']
#          )
#          # x = [datetime(2023, 3, i) for i in range(1, days+1)]
#          return weather_data

if __name__ == '__main__':
    json_data = get_openweather('London')
    # print(json_data)
    if json_data['cod'] == '200':
        city = json_data['city']
        print(json_data['cnt'], 'records received for', city['name'], city['country'])
        print('Co-ordinates: Lat:', city['coord']['lat'], ', Lon:', city['coord']['lon'])
        time_fmt = '%a, %d %b %Y %H:%M:%S'
        print('Sunrise: ', strftime(time_fmt, gmtime(city['sunrise'] + city['timezone'])))
        print('Sunset:  ', strftime(time_fmt, gmtime(city['sunset'] + city['timezone'])))
        # print(f'')
        df = get_weather_data(json_data, 1)
        print(df)
    else:
        print(json_data['message'])

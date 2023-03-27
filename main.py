import streamlit as st

from backend import get_openweather, get_weather_data
from time import strftime, gmtime

_debug_ = False

if __name__ == '__main__':
    st.set_page_config(page_title="Weather Forecast", layout='wide')
    st.title('Weather Forecast for the Next Few Days')

    # Select a place
    city = st.text_input('City', key='City', placeholder="Enter a city name")
    days = st.slider('Forecast Days', 1, 5, 1)  # No. of days to display

    # Select the data to display
    view_options = ('Temperature (C)', 'Pressure (mB)', 'Humidity %', 'Clouds Cover (%)', 'Wind Speed (m/s)',
                    'Visibility (m)', 'Sky Conditions')
    dataview = st.selectbox('Select data to view', options=view_options, index=0, key='dataview')

    json_data = get_openweather(city)

    if json_data['cod'] == '200':  # then response is OK
        city = json_data['city']

        st.header(f"{dataview} for the next {days} days in {city['name']}, {city['country']}")

        if _debug_:
            st.write(json_data['cnt'], 'records received for', city['name'], city['country'])

        # Get the city or place information and display it
        time_fmt = '%a, %d %b %Y %H:%M:%S'
        city_info = f"Co-ordinates: lat: {city['coord']['lat']}, lon: {city['coord']['lon']} ;  "
        city_info += f"Sunrise: {strftime(time_fmt, gmtime(city['sunrise'] + city['timezone']))} ;  "
        city_info += f"Sunset: {strftime(time_fmt, gmtime(city['sunset'] + city['timezone']))}"
        st.text(city_info)

        # Filter the weather data
        chart_data = get_weather_data(json_data, days)

        if dataview == 'Sky Conditions':  # then display weather icons
            icon_dir = 'http://openweathermap.org/img/w/'
            icons = []  # List of urls to the icons
            timestamps = []  # List of timestamps, captions for the icons
            for timestamp in chart_data.index:
                icons.append(f'{icon_dir}{chart_data[dataview][timestamp]}.png')
                timestamps.append(timestamp)

            st.image(icons, caption=timestamps)  # Display the list of icons with timestamps as captions

        else:  # Display the graph
            st.line_chart(data=chart_data, y=dataview, width=0, height=0)

    else:  # Response was not OK, display the message
        st.text(json_data['message'])

# See PyCharm help at https://www.jetbrains.com/help/pycharm/

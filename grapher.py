from requests import get
import matplotlib.pyplot as plt
from dateutil import parser
from datetime import datetime, timedelta
from json import loads
from pprint import pprint

KEY = 'e6133b0687157f6722716b5fda6ff7e8'
JSON_FILE = 'city.list.json'


def read_json_file(json_file_name):
    '''(str) -> list of dict
    '''
    print('Reading JSON data from %s...' % json_file_name)
    with open(json_file_name, 'r') as file_handle:
        data = [loads(line) for line in file_handle]
    file_handle.close()
    print('%d items processed' % (len(data)))
    return data


def get_country_data(json_data, country):
    '''(list of dict, str) -> list of dict
    '''
    print('Processing country data from JSON data...')
    country_data = [item for item in json_data
                    if item['country'] == country]
    print('%d items processed' % (len(country_data)))
    return country_data


def get_list_of_cities(country_data):
    '''(list in JSON) -> list of str

    Return a list of city names in that country.
    '''
    print('Obtaining a list of all cities...')
    return [city['name'] for city in country_data]


def get_set_of_duplicate_cities(country_data):
    '''(list in JSON) -> set of str

    Return a set of city names that appear more than once in that country.
    '''
    # Get all the city names in that country.
    all_city_names = get_list_of_cities(country_data)
    # Populate the set of all city names that appear more than once.
    duplicates = {city for city in all_city_names
                  if all_city_names.count(city) > 1}
    # Return the set.
    return duplicates


def get_city_data(country_data, city):
    '''(list in JSON, str) -> dict in JSON
    '''
    print('Searching for %s\'s city data...' % city)
    data = None
    found = False

    # Loop until a match for city name is found.
    index = 0
    while index < len(country_data) and not found:
        item = country_data[index]
        if item['name'].upper() == city.upper():
            print('%s data located in position %d.' % (city, index))
            data = item
            found = True
        else:
            index += 1

    if data == None:
        print('Sorry. City is not found.')
    else:
        print('Data successfully found for %s.' % city)

    return data


def get_city_id(json_data, city):
    '''(list of dict, str) -> int or NoneType
    '''
    print('Searching for %s\'s city ID...' % city)
    city_id = None
    found = False

    # Loop until a match for city name is found.
    index = 0
    while index < len(json_data) and not found:
        item = json_data[index]
        if item['name'].upper() == city.upper():
            print('%s data located in position %d.' % (city, index))
            city_id = item['_id']
            found = True
        else:
            index += 1

    if city_id == None:
        print('Sorry. City is not found.')
    else:
        print('ID found for %s is' % city, city_id)

    return city_id


def get_weather_data(city_id):
    url = 'http://api.openweathermap.org/data/2.5/forecast'
    url += '?id={}&APPID={}'.format(city_id, KEY)
    weather_data = get(url)
    return weather_data.json()


def get_compatible_time(target_day, hour):
    '''(int, int) -> str

    REQ: 1 <= day <= 31
    REQ: 0 <= hour <= 24
    '''
    today = datetime.now()
    hour -= hour % 3
    compatible_time = convert_to_dt_format(today, target_day, hour)
    return compatible_time


def convert_to_dt_format(dt, day=None, hour=None):
    '''(datetime, int) -> str
    '''
    if day == None:
        day = dt.strftime('%d')
    if hour == None:
        hour = dt.strftime('%H')

    dt_format = '{}-{}-{} {}:00:00'.format(
        dt.strftime('%Y'), dt.strftime('%m'),
        str(day), str(hour))

    return dt_format


def get_city_data_dt_range(city_data):
    '''(JSON dict) -> list
    '''
    data_list = city_data['list']
    first_date = data_list[0]['dt_txt']
    last_date = data_list[-1]['dt_txt']

    return [first_date, last_date]


def forecast(city_data, time):
    '''(JSON dict, str) -> dict or NoneType
    '''
    forecast = None
    data_list = city_data['list']

    found_forecast = False
    index = 0
    while index < len(data_list) and not found_forecast:
        item = data_list[index]
        if item['dt_txt'] == time:
            forecast = item
            found_forecast = True
        else:
            index += 1

    return forecast

def generate_temperature_graph(city_data):
    '''(dict in JSON) -> NoneType
    Generate a 5-day temperature graph of the given city.
    '''
    times, temperatures = list(), list()
    for forecast in city_data['list']:
        # Get the datetime as string from the JSON data
        dt_str = forecast['dt_txt'][:13]
        # Build a list of datetimes, format as "%Y-%m-%d %H:%M:%S".
        times.append(datetime.strptime(dt_str, "%Y-%m-%d %H"))
        # Build a list of temperatures in Celsius.
        temperatures.append(forecast['main']['temp'] - 273.15)
        #print("Data at", dt_str, "formatted and added.")

    pprint(times)
    fig = plt.figure()

    geninfo = city_data['city']
    fig_title = "5-Day Temperature Forecasts For %s, %s" % (geninfo['name'], geninfo['country'])
    fig.canvas.set_window_title(fig_title)
    plt.plot(times, temperatures)
    plt.xlabel('Date and time')
    plt.ylabel('Temperature')
    fig.autofmt_xdate()

    plt.show()


if __name__ == '__main__':
    '''
    main_data = read_json_file(JSON_FILE)
    canada_data = get_country_data(main_data, 'CA')
    canada_cities = [city['name'] for city in canada_data]
    toronto_id = get_city_id(canada_data, 'Toronto')
    '''
    toronto_id = 6167865
    toronto_data = get_weather_data(toronto_id)
    generate_temperature_graph(toronto_data)

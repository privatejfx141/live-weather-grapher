from requests import get
import matplotlib.pyplot as plt
from dateutil import parser
from datetime import datetime, timedelta
from json import loads
from pprint import pprint

COUNTRIES_CSV_FILE = "country_abbvs.csv"
KEY = 'e6133b0687157f6722716b5fda6ff7e8'
JSON_FILE = 'city.list.json'

class CountryAbbvs:
    """docstring for CountryAbbvs"""
    def __init__(self):
        super(CountryAbbvs, self).__init__()
        
    def read_country_abbreviations(self, file_name):
        '''(str) -> dict

        Given a file name, return a dictionary of country names mapped to their
        two letter abbreviations.

        REQ: file must be a .csv file
        '''
        # Open the file.
        file = open(file_name, 'r', encoding="utf8")
        # Create the result dictionary for the abbreviation mapping.
        abbreviations = dict()
        # Skip the header, then loop through each line in that file.
        header = file.readline()
        for line in file:
            # Add a new entry into the result dictionary.
            item = line.split(',')
            abbreviations[item[0]] = item[1]
        # Close the file.
        file.close()
        # Return the result dictionary.
        return abbreviations


    def get_countries_dict(self):
        '''() -> dict

        Return the dictionary from the default .csv file.
        '''
        return self.read_country_abbreviations(COUNTRIES_CSV_FILE)


class Weather:
    """docstring for Weather"""
    def __init__(self):
        super(Weather, self).__init__()
    
    def forecast(self, city_data, time):
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

    def get_weather_data(self, city_id):
        url = 'http://api.openweathermap.org/data/2.5/forecast'
        url += '?id={}&APPID={}'.format(city_id, KEY)
        weather_data = get(url)
        return weather_data.json()

class Parser:
    """docstring for Parser"""
    def __init__(self):
        super(Parser, self).__init__()

    def read_json_file(self, json_file_name):
        '''(str) -> list of dict
        '''
        print('Reading JSON data from %s...' % json_file_name)
        with open(json_file_name, mode='r', encoding="utf8") as file_handle:
            data = [loads(line) for line in file_handle]
        file_handle.close()
        print('%d items processed' % (len(data)))
        return data
        

class Grapher:
    """docstring for Grapher"""
    def __init__(self):
        super(Grapher, self).__init__()
        

    def generate_temperature_graph(self, city_data):
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

class Converter:
    """docstring for Converter"""
    def __init__(self):
        super(Converter, self).__init__()

    def get_city_data_dt_range(self, city_data):
        '''(JSON dict) -> list
        '''
        data_list = city_data['list']
        first_date = data_list[0]['dt_txt']
        last_date = data_list[-1]['dt_txt']

        return [first_date, last_date]

    def convert_to_dt_format(self, dt, day=None, hour=None):
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

    def get_compatible_time(self, target_day, hour):
        '''(int, int) -> str

        REQ: 1 <= day <= 31
        REQ: 0 <= hour <= 24
        '''
        today = datetime.now()
        hour -= hour % 3
        compatible_time = self.convert_to_dt_format(today, target_day, hour)
        return compatible_time
        

class Country:
    """docstring for Country"""
    def __init__(self):
        super(Country, self).__init__()
        
    def get_country_data(self, json_data, country):
        '''(list of dict, str) -> list of dict
        '''
        print('Processing country data from JSON data...')
        country_data = [item for item in json_data
                        if item['country'] == country]
        print('%d items processed' % (len(country_data)))
        return country_data

    def get_list_of_cities(self, country_data):
        '''(list in JSON) -> list of str

        Return a list of city names in that country.
        '''
        print('Obtaining a list of all cities...')
        return [city['name'] for city in country_data]


    def get_set_of_duplicate_cities(self, country_data):
        '''(list in JSON) -> set of str

        Return a set of city names that appear more than once in that country.
        '''
        # Get all the city names in that country.
        all_city_names = self.get_list_of_cities(country_data)
        # Populate the set of all city names that appear more than once.
        duplicates = {city for city in all_city_names
                      if all_city_names.count(city) > 1}
        # Return the set.
        return duplicates

    def get_city_data(self, country_data, city):
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


    def get_city_id(self, json_data, city):
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

class UserInput:
    """docstring for UserInput"""
    def __init__(self):
        super(UserInput, self).__init__()
        self.country = Country()
        self.weather = Weather()

    def user_input_country(self, city_list_data, abbvs):
        data = None

        while data is None:
            name = input('Enter a country name: ')
            # If name is not already an abbreviation, make it so.
            if len(name) != 2:
                name = abbvs[name]
            # Get the data.
            if name in abbvs.values():
                
                data = self.country.get_country_data(city_list_data, name)
            else:
                print('Oops! Country does not exist in data.')
        return data


    def user_input_city(self, country_data):
        weather_data = None

        city_list = self.country.get_list_of_cities(country_data)
        dup_city_set = {city for city in city_list if city_list.count(city) > 1}
        while weather_data is None:
            name = input('Enter a city name: ')
            if name in city_list:

                # If there are more than one city with the same name.
                if name in dup_city_set:
                    # Search through the data for cities with that same name.
                    instances, index = 0, 0
                    while index < len(city_list) and instances < city_list.count(name):
                        item = country_data[index]
                        if item['name'].upper() == name.upper():
                            instances += 1
                            print(item['_id'], item['name'], item['coord'])
                        index += 1
                    city_id = input('Select the city id: ')

                else:
                    city_data = self.country.get_city_data(country_data, name)
                    print('Obtaining city id from %s at' % name, city_data['coord'])
                    city_id = city_data['_id']
                print('Requesting weather data for %s...' % name)
                weather_data = self.weather.get_weather_data(int(city_id))

            else:
                print('Oops! %s does not exist!' % name)

        return weather_data


def main():
    '''() -> NoneType
    '''
    # Read and get the starting JSON data.
    countryAbbvs = CountryAbbvs()
    parser = Parser()
    city_list_data = parser.read_json_file(JSON_FILE)
    abbvs = countryAbbvs.read_country_abbreviations(COUNTRIES_CSV_FILE)
    while True:
        user_input = UserInput()
        graph = Grapher()
        # Get the country and city weather JSON data.
        country_data = user_input.user_input_country(city_list_data, abbvs)
        city_weather_data = user_input.user_input_city(country_data)
        # Generate the graph.
        graph.generate_temperature_graph(city_weather_data)
        

if __name__ == '__main__':
    main()
        
from CountryAbbvs import *
from grapher import *


def user_input_country(city_list_data, abbvs):
    data = None

    while data is None:
        name = input('Enter a country name: ')
        # If name is not already an abbreviation, make it so.
        if len(name) != 2:
            name = abbvs[name]
        # Get the data.
        if name in abbvs.values():
            data = get_country_data(city_list_data, name)
        else:
            print('Oops! Country does not exist in data.')
    return data


def user_input_city(country_data):
    weather_data = None

    city_list = get_list_of_cities(country_data)
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
                city_data = get_city_data(country_data, name)
                print('Obtaining city id from %s at' % name, city_data['coord'])
                city_id = city_data['_id']
            print('Requesting weather data for %s...' % name)
            weather_data = get_weather_data(int(city_id))

        else:
            print('Oops! %s does not exist!' % name)

    return weather_data


def main():
    '''() -> NoneType
    '''
    # Read and get the starting JSON data.
    city_list_data = read_json_file(JSON_FILE)
    countryAbbvs = CountryAbbvs
    abbvs = countryAbbvs.read_country_abbreviations(COUNTRIES_CSV_FILE)
    while True:
        # Get the country and city weather JSON data.
        country_data = user_input_country(city_list_data, abbvs)
        city_weather_data = user_input_city(country_data)
        # Generate the graph.
        generate_temperature_graph(city_weather_data)
        

if __name__ == '__main__':
    main()

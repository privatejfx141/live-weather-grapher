COUNTRIES_CSV_FILE = "country_abbvs.csv"


def read_country_abbreviations(file_name):
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


def get_countries_dict():
    '''() -> dict

    Return the dictionary from the default .csv file.
    '''
    return read_country_abbreviations(COUNTRIES_CSV_FILE)


if __name__ == '__main__':
    from pprint import pprint

    abbvs = get_countries_dict()
    print('Countries in dictionary:', len(abbvs))
    pprint(abbvs)

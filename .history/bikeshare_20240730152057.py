## TODO: import all necessary packages and functions

import pandas as pd
import numpy as np
from datetime import datetime
from datetime import timedelta
import time

## Filenames
CITY_DATA = {'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv'}

def get_city():
    '''Asks the user for a city and returns the filename for that city's bike share data.

    Args:
        none.
    Returns:
        (str) Filename for a city's bikeshare data.
    '''
    city = ''
    while city.lower() not in CITY_DATA.keys():
        city = input('\nHello! Let\'s explore some US bikeshare data!\n'
                     'Would you like to see data for Chicago, New York City, or'
                     ' Washington?\n').strip().lower()
        if city in CITY_DATA:
            return CITY_DATA[city]
        else:
            print('Sorry, I do not understand your input. Please input either '
                  'Chicago, New York City, or Washington.')

def get_time_period():
    '''Asks the user for a time period and returns the specified filter.

    Args:
        none.
    Returns:
        (str) Time filter for the bikeshare data.
    '''
    time_period = ''
    while time_period.lower() not in ['month', 'day', 'none']:
        time_period = input('\nWould you like to filter the data by month, day,'
                            ' or not at all? Type "none" for no time filter.\n')
        if time_period.lower() not in ['month', 'day', 'none']:
            print('Sorry, I do not understand your input.')
    return time_period

def get_month():
    '''Asks the user for a month and returns the specified month.

    Args:
        none.
    Returns:
        (tuple) Lower limit, upper limit of month for the bikeshare data.
    '''
    month_input = ''
    months_dict = {'january': 1, 'february': 2, 'march': 3, 'april': 4,
                   'may': 5, 'june': 6}
    while month_input.lower() not in months_dict.keys():
        month_input = input('\nWhich month? January, February, March, April,'
                            ' May, or June?\n')
        if month_input.lower() not in months_dict.keys():
            print('Sorry, I do not understand your input. Please type in a '
                  'month between January and June')
    month = months_dict[month_input.lower()]
    return ('2017-{}'.format(month), '2017-{}'.format(month + 1))

def get_day():
    '''Asks the user for a day and returns the specified day.

    Args:
        none.
    Returns:
        (tuple) Lower limit, upper limit of date for the bikeshare data.
    '''
    this_month = get_month()[0]
    month = int(this_month[5:])
    valid_date = False
    while valid_date == False:    
        is_int = False
        day = input('\nWhich day? Please type your response as an integer.\n')
        while is_int == False:
            try:
                day = int(day)
                is_int = True
            except ValueError:
                print('Sorry, I do not understand your input. Please type your'
                      ' response as an integer.')
                day = input('\nWhich day? Please type your response as an integer.\n')
        try:
            start_date = datetime(2017, month, day)
            valid_date = True
        except ValueError as e:
            print(str(e).capitalize())
    end_date = start_date + timedelta(days=1)
    return (str(start_date), str(end_date))

def popular_month(df):
    '''Finds and prints the most popular month for start time.
    Args:
        bikeshare dataframe
    Returns:
        none
    '''
    months = ['January', 'February', 'March', 'April', 'May', 'June']
    index = int(df['start_time'].dt.month.mode())
    most_pop_month = months[index - 1]
    print('The most popular month is {}.'.format(most_pop_month))

def popular_day(df):
    '''Finds and prints the most popular day of week (Monday, Tuesday, etc.) for start time.
    Args:
        bikeshare dataframe
    Returns:
        none
    '''
    days_of_week = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday',
                    'Saturday', 'Sunday']
    index = int(df['start_time'].dt.dayofweek.mode())
    most_pop_day = days_of_week[index]
    print('The most popular day of week for start time is {}.'.format(most_pop_day))

def popular_hour(df):
    '''Finds and prints the most popular hour of day for start time.
    Args:
        bikeshare dataframe
    Returns:
        none
    '''
    most_pop_hour = int(df['start_time'].dt.hour.mode())
    if most_pop_hour == 0:
        am_pm = 'am'
        pop_hour_readable = 12
    elif 1 <= most_pop_hour < 13:
        am_pm = 'am'
        pop_hour_readable = most_pop_hour
    elif 13 <= most_pop_hour < 24:
        am_pm = 'pm'
        pop_hour_readable = most_pop_hour - 12
    print('The most popular hour of day for start time is {}{}.'.format(pop_hour_readable, am_pm))

def trip_duration(df):
    '''Finds and prints the total trip duration and average trip duration in
       hours, minutes, and seconds.
    Args:
        bikeshare dataframe
    Returns:
        none
    '''
    total_duration = df['trip_duration'].sum()
    minute, second = divmod(total_duration, 60)
    hour, minute = divmod(minute, 60)
    print('The total trip duration is {} hours, {} minutes and {}'
          ' seconds.'.format(hour, minute, second))
    average_duration = round(df['trip_duration'].mean())
    m, s = divmod(average_duration, 60)
    if m > 60:
        h, m = divmod(m, 60)
        print('The average trip duration is {} hours, {} minutes and {}'
              ' seconds.'.format(h, m, s))
    else:
        print('The average trip duration is {} minutes and {} seconds.'.format(m, s))

def popular_stations(df):
    '''Finds and prints the most popular start station and most popular end station.
    Args:
        bikeshare dataframe
    Returns:
        none
    '''
    pop_start = df['start_station'].mode().to_string(index = False)
    pop_end = df['end_station'].mode().to_string(index = False)
    print('The most popular start station is {}.'.format(pop_start))
    print('The most popular end station is {}.'.format(pop_end))

def popular_trip(df):
    '''Finds and prints the most popular trip.
    Args:
        bikeshare dataframe
    Returns:
        none
    '''
    most_pop_trip = df['journey'].mode().to_string(index = False)
    # The 'journey' column is created in the statistics() function.
    print('The most popular trip is {}.'.format(most_pop_trip))

def users(df):
    '''Finds and prints the counts of each user type.
    Args:
        bikeshare dataframe
    Returns:
        none
    '''
    subs = df.query('user_type == "Subscriber"').user_type.count()
    cust = df.query('user_type == "Customer"').user_type.count()
    print('There are {} Subscribers and {} Customers.'.format(subs, cust))

def gender(df):
    '''Finds and prints the counts of gender.
    Args:
        bikeshare dataframe
    Returns:
        none
    '''
    male_count = df.query('gender == "Male"').gender.count()
    female_count = df.query('gender == "Male"').gender.count()
    print('There are {} male users and {} female users.'.format(male_count, female_count))

def birth_years(df):
    ''' Finds and prints the earliest (i.e. oldest user), most recent (i.e. 
        youngest user), and most popular birth years.
    Args:
        bikeshare dataframe
    Returns:
        none
    '''
    earliest = int(df['birth_year'].min())
    latest = int(df['birth_year'].max())
    mode = int(df['birth_year'].mode())
    print('The oldest users are born in {}.\nThe youngest users are born in {}.'
          '\nThe most popular birth year is {}.'.format(earliest, latest, mode))

def display_data(df):
    '''Displays five lines of data if the user specifies that they would like to.
    After displaying five lines, ask the user if they would like to see five more,
    continuing asking until they say stop.

    Args:
        data frame
    Returns:
        none
    '''
    def is_valid(display):
        if display.lower() in ['yes', 'no']:
            return True
        else:
            return False
    head = 0
    tail = 5
    valid_input = False
    while valid_input == False:
        display = input('\nWould you like to view individual trip data? '
                        'Type \'yes\' or \'no\'.\n')
        if is_valid(display) == True:
            valid_input = True
            if display.lower() == 'yes':
                print(df[df.columns[0:-1]].iloc[head:tail])
                head += 5
                tail += 5
                while display.lower() == 'yes':
                    valid_input = False
                    while valid_input == False:
                        display = input('\nWould you like to view more trip data? '
                                        'Type \'yes\' or \'no\'.\n')
                        if is_valid(display) == True:
                            valid_input = True
                            if display.lower() == 'yes':
                                print(df[df.columns[0:-1]].iloc[head:tail])
                                head += 5
                                tail += 5
                            elif display.lower() == 'no':
                                break
                        else:
                            print('Sorry, I do not understand your input. Please type \'yes\' or \'no\'.')

def statistics():
    '''Calculates and prints out the descriptive statistics about a city and
    time period specified by the user via raw input.
    Args:
        none
    Returns:
        none
    '''
    city = get_city()
    time_period = get_time_period()
    print('Reading the {} file...'.format(city))
    df = pd.read_csv(city, parse_dates = ['Start Time', 'End Time'])
    df.columns = df.columns.str.replace(' ', '_').str.lower()
    df['journey'] = df['start_station'].str.cat(df['end_station'], sep = ' to ')
    if time_period == 'none':
        start_date, end_date = (df['start_time'].min(), df['start_time'].max())
    elif time_period == 'day':
        start_date, end_date = get_day()
    elif time_period == 'month':
        start_date, end_date = get_month()
    print('Filtering the data between {} and {}...'.format(start_date, end_date))
    df = df[(df['start_time'] >= start_date) & (df['start_time'] < end_date)]
    print('\nCalculating the first statistic...')
    if time_period == 'none':
        start_time = time.time()
        popular_month(df)
        print("That took %s seconds." % (time.time() - start_time))
        print('\nCalculating the next statistic...')
    if time_period == 'none' or time_period == 'month':
        start_time = time.time()
        popular_day(df)
        print("That took %s seconds." % (time.time() - start_time))
        print('\nCalculating the next statistic...')
    start_time = time.time()
    popular_hour(df)
    print("That took %s seconds." % (time.time() - start_time))
    print('\nCalculating the next statistic...')
    start_time = time.time()
    trip_duration(df)
    print("That took %s seconds." % (time.time() - start_time))
    print('\nCalculating the next statistic...')
    start_time = time.time()
    popular_stations(df)
    print("That took %s seconds." % (time.time() - start_time))
    print('\nCalculating the next statistic...')
    start_time = time.time()
    popular_trip(df)
    print("That took %s seconds." % (time.time() - start_time))
    print('\nCalculating the next statistic...')
    start_time = time.time()
    users(df)
    print("That took %s seconds." % (time.time() - start_time))
    try:
        print('\nCalculating the next statistic...')
        start_time = time.time()
        gender(df)
        print("That took %s seconds." % (time.time() - start_time))
    except KeyError:
        print('Gender data is not available for {}.'.format(city.title()))
    try:
        print('\nCalculating the next statistic...')
        start_time = time.time()
        birth_years(df)
        print("That took %s seconds." % (time.time() - start_time))
    except KeyError:
        print('Birth year data is not available for {}.'.format(city.title()))
    display_data(df)

def main():
    ''' The main function that runs the bikeshare statistics script.'''
    while True:
        statistics()
        restart = input('\nWould you like to restart? Type \'yes\' or \'no\'.\n')
        if restart.lower() != 'yes':
            break

if __name__ == "__main__":
    main()

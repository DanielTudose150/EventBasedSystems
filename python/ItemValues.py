"""File containing the constant values that are used by a publication item."""

import numpy as np
import weather
import dates

STATION_IDS = np.array([i for i in range(1, 10)])
CITIES = np.array(
    ['Bucharest', 'Iasi', 'Cluj-Napoca', 'Timisoara', 'Sibiu', 'Brasov', 'Constanta', 'Craiova', 'Oradea'])
DIRECTIONS = np.array(['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW'])
DATES = dates.DATES


def get_station_ids():
    return np.random.choice(STATION_IDS, 1)[0]


def get_cities():
    return np.random.choice(CITIES, 1)[0]


def get_direction():
    return np.random.choice(DIRECTIONS, 1)[0]


def get_date():
    return np.random.choice(DATES, 1)[0]


GET_STATIONID = get_station_ids
GET_CITY = get_cities
GET_TEMP = weather.get_temp
GET_RAIN = weather.get_rain
GET_WIND = weather.get_wind
GET_DIRECTION = get_direction
GET_DATE = get_date

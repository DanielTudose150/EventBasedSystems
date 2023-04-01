"""File containing the constant values that are used by a publication item."""

import numpy as np
import weather
import dates

STATION_IDS = np.array([i for i in range(1, 10)])
CITIES = np.array(
    ['Bucharest', 'Iasi', 'Cluj-Napoca', 'Timisoara', 'Sibiu', 'Brasov', 'Constanta', 'Craiova', 'Oradea'])
DIRECTIONS = np.array(['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW'])
DATES = dates.DATES

GET_TEMP = weather.get_temp
GET_RAIN = weather.get_rain
GET_WIND = weather.get_wind



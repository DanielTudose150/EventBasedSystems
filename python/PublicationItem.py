import ItemValues as IV
import numpy as np


class PublicationItem:
    def __init__(self):
        self.stationid = np.random.choice(IV.STATION_IDS, 1)[0]
        self.city = np.random.choice(IV.CITIES, 1)[0]
        self.temp = IV.GET_TEMP()
        self.rain = IV.GET_RAIN()
        self.wind = IV.GET_WIND()
        self.direction = np.random.choice(IV.DIRECTIONS, 1)[0]
        self.date = np.random.choice(IV.DATES, 1)[0]

    def __str__(self):
        return f'{{(stationid, {self.stationid});(city,{self.city});(temp,{self.temp});(rain,{self.rain});(wind,{self.wind});(direction,{self.direction});(date,{self.date})}}'

    def __repr__(self):
        return f'{{(stationid, {self.stationid});(city,{self.city});(temp,{self.temp});(rain,{self.rain});(wind,{self.wind});(direction,{self.direction});(date,{self.date})}}'
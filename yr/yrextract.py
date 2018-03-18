from datetime import datetime
from collections import OrderedDict

class YrExtract:

    def __init__(self, forecast: OrderedDict, date_start: datetime, date_end: datetime):
        self._forecast = forecast
        self._start = date_start
        self._end = date_end

    def _get_extract(self):
        out = []
        for line in self._forecast:
            from_time = datetime.strptime(line['@from'], "%Y-%m-%dT%H:%M:%S")
            if from_time < self._start:
                continue

            to_time = datetime.strptime(line['@to'], "%Y-%m-%dT%H:%M:%S")
            if to_time > self._end:
                break

            out.append(line)
        return out

    @property
    def min_temperature(self) -> float:
        min_temperature = 1000
        for line in self._get_extract():
            temperature = float(line['temperature']['@value'])
            min_temperature = min(min_temperature, temperature)
        return min_temperature

    @property
    def max_temperature(self) -> float:
        max_temperature = -1000
        for line in self._get_extract():
            temperature = float(line['temperature']['@value'])
            max_temperature = max(max_temperature, temperature)
        return max_temperature

    @property
    def min_wind_speed(self) -> float:
        min_v = 1000
        for line in self._get_extract():
            v = float(line['windSpeed']['@mps'])
            min_v = min(min_v, v)
        return min_v


    @property
    def max_wind_speed(self) -> float:
        max_v = -1000
        for line in self._get_extract():
            v = float(line['windSpeed']['@mps'])
            max_v = max(max_v, v)
        return max_v

    @property
    def max_temperature(self) -> float:
        max_temperature = -1000
        for line in self._get_extract():
            temperature = float(line['temperature']['@value'])
            max_temperature = max(max_temperature, temperature)
        return max_temperature

    @property
    def min_precipitation(self) -> float:
        sum = 0
        for line in self._get_extract():
            sum += float(line['precipitation']['@minvalue'])
        return sum

    @property
    def max_precipitation(self) -> float:
        sum = 0
        for line in self._get_extract():
            sum += float(line['precipitation']['@maxvalue'])
        return sum

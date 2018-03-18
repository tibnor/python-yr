import unittest

from datetime import datetime
from yr.libyr import Yr
from yr.yrextract import YrExtract


class TestLibYr(unittest.TestCase):
    def setUp(self):
        weather_data = Yr(
            location_name='Norge/Trøndelag/Trondheim/Tyholt',
            forecast_link='forecast_hour_by_hour',
            language_name='nb',
        )
        from test.test_dict import tyholt_dictionary
        weather_data.dictionary = tyholt_dictionary
        self.weather_data = weather_data
        start = datetime(2018, 3, 18, 19)
        end = datetime(2018, 3, 18, 23)
        self.weather_extract = YrExtract(self.weather_data, start, end)

    def test_extract_min_temperature(self):
        self.assertEqual(self.weather_extract.min_temperature, 3)

    def test_extract_max_temperature(self):
        self.assertEqual(self.weather_extract.max_temperature, 4)

    def test_extract_min_precipitation(self):
        self.assertEqual(self.weather_extract.min_precipitation, 0.5 + 0.7 + 0.8)

    def test_extract_max_precipitation(self):
        self.assertEqual(self.weather_extract.max_precipitation, 1.2 + 2.6 + 2.2)


if __name__ == '__main__':
    unittest.main()

import unittest
from collections import OrderedDict
from yr.libyr import Yr


class TestLibYr(unittest.TestCase):
    def test_forecast(self):
        weatherdata = Yr(
            location_name='Czech_Republic/Prague/Prague',
            forecast_link='forecast',
            language_name='en',
        ).now(as_json=True)
        self.assertIsInstance(weatherdata, str)

    def test_forecast_hour_by_hour(self):
        weatherdata = Yr(
            location_name='Czech_Republic/Prague/Prague',
            forecast_link='forecast_hour_by_hour',
            language_name='en',
        ).now(as_json=True)
        self.assertIsInstance(weatherdata, str)

    def test_forecast_xyz(self):
        xyz = (14.4656239, 50.0596696, 11)
        weather_data = Yr(
            location_xyz=xyz,
            language_name='en',
        )
        self.assertIsInstance(weather_data.now(as_json=True), str)

    def test_forecast_xyz_2(self):
        weatherdata = Yr(
            coordinates=(50.0596696, 14.4656239, 11),
            language_name='en',
        ).now(as_json=True)
        self.assertIsInstance(weatherdata, str)

    def test_forecast_xyz_3(self):
        weatherdata = Yr(
            coordinates=(63.4066631, 10.4426724, 10),
            language_name='en'
        ).now(as_json=True)
        self.assertIsInstance(weatherdata, str)

    def test_forecast_now_double(self):
        weatherdata = Yr(
            location_name='Czech_Republic/Prague/Prague',
            forecast_link='forecast',
            language_name='en',
        )
        now1 = weatherdata.now(as_json=True)
        now2 = weatherdata.now(as_json=True)
        self.assertSequenceEqual(now1, now2)

    def test_forecast_hour_by_hour_Trondheim_fixed_file(self):
        weatherdata = Yr(
            location_name='Norge/Trøndelag/Trondheim/Tyholt',
            forecast_link='forecast_hour_by_hour',
            language_name='nb',
        )
        # Use this to generate new test file
        # with open('test_dict.py','w') as f:
        #    f.write(str(weatherdata.dictionary))
        from test_dict import tyholt_dictionary
        weatherdata.dictionary = tyholt_dictionary
        print(weatherdata.now())
        expecting = OrderedDict([('@from', '2018-03-18T11:00:00'), ('@to', '2018-03-18T12:00:00'), (
        'symbol', OrderedDict([('@number', '12'), ('@numberEx', '47'), ('@name', 'Light sleet'), ('@var', '47')])), (
                                 'precipitation',
                                 OrderedDict([('@value', '0.1'), ('@minvalue', '0'), ('@maxvalue', '0.5')])), (
                                 'windDirection',
                                 OrderedDict([('@deg', '256.9'), ('@code', 'WSW'), ('@name', 'West-southwest')])),
                                 ('windSpeed', OrderedDict([('@mps', '9.2'), ('@name', 'Fresh breeze')])),
                                 ('temperature', OrderedDict([('@unit', 'celsius'), ('@value', '2')])),
                                 ('pressure', OrderedDict([('@unit', 'hPa'), ('@value', '1021.0')]))])

        self.assertEqual(weatherdata.now(), expecting)



if __name__ == '__main__':
    unittest.main()

#!/usr/bin/env python3

import logging
import json
import xmltodict  # <~ the only external dependency
from yr.utils import Connect, Location, API_Locationforecast, Language, YrException


class Yr:

    default_forecast_link = 'forecast'
    default_language_name = 'en'

    def py2json(self, python):
        return json.dumps(python, indent=4)

    def xml2dict(self, xml):
        return xmltodict.parse(xml)

    def dict2xml(self, dictionary):
        return xmltodict.unparse(dictionary, pretty=True)

    def py2result(self, python, as_json=False):  # default is return result as dictionary ;)
        if as_json:
            return self.py2json(python)
        else:
            return python

    def forecast(self, as_json=False):
        if self.coordinates:
            times = self.dictionary['weatherdata']['product']['time']
        else:
            times = self.dictionary['weatherdata']['forecast']['tabular']['time']
        for time in times:
            yield self.py2result(time, as_json)

    def now(self, as_json=False):
        return next(self.forecast(as_json))

    def __init__(
            self,
            location_name=None,
            coordinates=None,
            location_xyz=None,
            forecast_link=default_forecast_link,
            language_name=default_language_name,
    ):
        self.forecast_link = forecast_link
        self.language_name = language_name
        self.language = Language(language_name=self.language_name)

        if location_xyz:
            coordinates = (location_xyz[1], location_xyz[0], location_xyz[2])
            self.location_xyz = location_xyz

        if location_name:
            self.location_name = location_name
            self.coordinates = None
            self.location = Location(
                location_name=self.location_name,
                forecast_link=self.forecast_link,
                language=self.language,
            )
        elif coordinates:
            self.location_name = None
            self.coordinates = coordinates
            self.location = API_Locationforecast(
                lat=self.coordinates[0],
                lon=self.coordinates[1],
                msl=self.coordinates[2],
                language=self.language,
            )
        else:
            raise YrException('location_name or location_xyz parameter must be set')

        self.connect = Connect(location=self.location)
        self.xml_source = self.connect.read()
        self.dictionary = self.xml2dict(self.xml_source)
        self.credit = self.language.dictionary['credit']

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    logging.info('starting __main__')

    logging.info('stopping __main__')

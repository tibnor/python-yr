#!/usr/bin/env python3
import json

import xmltodict  # <~ the only external dependency

from yr.utils import Connect, Location, ApiLocationForecast, Language, YrException


class Yr:

    default_forecast_link = 'forecast'
    default_language_name = 'en'

    @staticmethod
    def py2json(python):
        return json.dumps(python, indent=4)

    @staticmethod
    def xml2dict(xml):
        return xmltodict.parse(xml)

    @staticmethod
    def dict2xml(dictionary):
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
        language = Language(language_name=language_name)

        if location_xyz:
            coordinates = (location_xyz[1], location_xyz[0], location_xyz[2])

        if location_name:
            self.coordinates = None
            location = Location(
                location_name=location_name,
                forecast_link=forecast_link,
                language=language,
            )
        elif coordinates:
            self.coordinates = coordinates
            location = ApiLocationForecast(
                lat=self.coordinates[0],
                lon=self.coordinates[1],
                msl=self.coordinates[2]
            )
        else:
            raise YrException('location_name or location_xyz parameter must be set')

        connect = Connect(location=location)
        xml_source = connect.read()
        self.dictionary = Yr.xml2dict(xml_source)
        self.credit = language.dictionary['credit']

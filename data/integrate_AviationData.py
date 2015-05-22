#!/usr/bin/env python
# encoding: utf-8

import datetime
from dateutil import parser
from datetime import date, time, datetime
import xml.etree.ElementTree as ET
import re
from model import *
from data_util import add_event, process_data, match_country
from string_utils import unicodize, orNone, intOrNone


path = '../AviationDataFormatted.xml'

def parse_phase(phase):
    if phase:
        phase = phase.lower()
        if 'unknown' not in phase:
            return phase

def parse_weather(weather):
    if weather:
        weather = weather.lower()
        if weather != 'unk':
            return weather


def process(data, session):
    if data['InvestigationType'] == 'Accident':
        date = parser.parse(data['EventDate']).date()
        time = None
        airline = data.get('AirCarrier')
        manufacturer = data['Make']
        plane_type = data['Model']
        registration = data['RegistrationNumber']
        country = orNone(data['Country'])
        if country:
            country = match_country(country)
        location = orNone(data['Location'])
        weather = parse_weather(data['WeatherCondition'])
        phase = parse_phase(data['BroadPhaseOfFlight'])
        deaths_total = intOrNone(data['TotalFatalInjuries'])
        total = None
        deaths_passengers = None
        passengers = None
        deaths_crew = None
        crew = None
        departure = None
        destination = None
        number = None
        source = u'ntsb'

        add_event(**locals())


def input_stream():
    tree = ET.parse(path)
    root = tree.getroot()

    for row in root[0]:
        data = dict(**row.attrib)
        yield unicodize(data, encoding=None)

if __name__ == '__main__':
    process_data(input_stream(), process)

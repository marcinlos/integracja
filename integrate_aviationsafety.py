#!/usr/bin/env python

from dateutil import parser
from datetime import date, time, datetime
from model import *
import re

from data_util import add_event, process_data
from string_utils import orNone, intOrNone, unicodize


def get_date(data):
    try:
        s = data['Date']
        if s not in ('', 'date unk.') and s.lower()[0] != 'x':
            return parser.parse(s).date()
    except KeyError:
        pass
    except Exception as e:
        print u'Could not parse date: "{}"'.format(s)
        print e

def get_time(data):
    try:
        s = data['Time']
        s = re.sub(r'^ca?\.?', '', s)
        s = re.sub(',', ':', s)
        if s != '*':
            return parser.parse(s).time()
    except KeyError:
        pass
    except Exception as e:
        print u'Could not parse time: "{}"'.format(s)
        print e

def parse_people(people):
    if people:
        try:
            m = re.match(r'Fatalities: (\d*) / Occupants: (\d*)', people)
            dead, total = m.groups()
            dead = intOrNone(dead)
            total = intOrNone(total)
            return (dead, total)
        except Exception as e:
            print u'Could not parse peolpe: "{}"'.format(people)
            print e
    return (None, None)

def parse_phase(phase):
    if phase:
        try:
            phase = re.sub(r' \([A-Z]+\)$', '', phase)
            phase = phase.lower()
            if not phase or phase.startswith('unknown') or phase == '()':
                phase = None
        except Exception as e:
            print u'Could not parse phase: "{}"'.format(phase)
            print e

def parse_location(location):
    if location:
        try:
            location = location.strip()
            m = re.search(r'\(   (.*)\)$', location)
            country = orNone(m.group(1))
            if not country or 'unknown' in country.lower():
                country = None

            m = re.match(r'^(.+) \(   .*\)$', location)
            place = orNone(m.group(1))
            if place:
                for s in ('near', 'off', 'within'):
                    place = re.sub(s + ' ', '', place)
            if not place or 'unknown' in place.lower():
                place = None

            return (country, place)
        except Exception as e:
            print u'Could not parse location: "{}"'.format(location)
            print e

def parse_point(point):
    if point:
        if point not in ('-', '?'):
            return point

def parse_airline(airline):
    if airline:
        airline = airline.strip()
        airline = re.sub(r'\([A-Z]+\)$', '', airline)
        airline = re.sub(r'\s*-\s*[A-Z]+$', '', airline)
        airline = airline.strip()
        return airline

def process(data, session):
    date = get_date(data)
    time = get_time(data)
    airline = parse_airline(data.get('Operator'))
    plane_type = orNone(data.get('Type'))
    registration = orNone(data.get('Registration'))
    number = orNone(data.get('Flightnumber'))
    departure = parse_point(data.get('Departure airport'))
    destination = parse_point(data.get('Destination airport'))
    deaths_crew, crew = parse_people(data.get('Crew'))
    deaths_total, total = parse_people(data.get('Total'))
    deaths_passengers, passengers = parse_people(data.get('Passengers'))
    phase = parse_phase(data.get('Phase'))
    country, location = parse_location(data.get('Location'))
    weather = None

    add_event(**locals())

def input_stream():
    with open('../aviation-safety-data') as input:
        for row in input.readlines():
            data = eval(row)
            yield unicodize(data)

if __name__ == '__main__':
    process_data(input_stream(), process)


#!/usr/bin/env python
# encoding: utf-8

from sqlalchemy.orm.exc import NoResultFound
from dateutil import parser
from datetime import date, time, datetime
from model import *
import re

from data_util import add_event, process_data, match_country,\
    find_manufacturer, find_event
from string_utils import *

'''
{"Date": "March 31, 2006", "Time": "17:35", "Location": "Rio Bonito, Brazil",
"Operator": "Team Air", "Flight #": "6865", "Route": "Maca\xe9 - Rio de
Janeiro", "AC\n        Type": "Let L410UVP-E20", "Registration": "PT-FSE", "cn /
ln": "912532", "Aboard": "19   (passengers:17  crew:2)", "Fatalities": "19
(passengers:17  crew:2)", "Ground": "0", "Summary": "Twenty minutes after taking
off from Maca\xe9, the plane disappeared of Rio de Janeiro radar. The crew was
flying VFR in poor weather conditions and changed their route attempting to fly
to the coast. The plane crashed in a wooded area, exploded and burned."}
'''

def get_date(data):
    try:
        s = data['Date']
        if s not in ('?',):
            return parser.parse(s).date()
    except KeyError:
        pass
    except Exception as e:
        print u'Could not parse date: "{}"'.format(s)
        print e

def get_time(data):
    try:
        s = data['Time']
        if s not in ('?',):
            s = re.sub(r'^[cCd]\:? ?', '', s)
            s = re.sub('[;"]', ':', s)
            s = re.sub(r'[^0-9:]', '', s)
            return parser.parse(s).time()
    except KeyError:
        pass
    except Exception as e:
        print u'Could not parse time: "{}"'.format(s)
        print e


def parse_people(people):
    m = re.match(r'(\d+|\?)\s+\(passengers:(\d+|\?)\s+crew:(\d+|\?)', people)
    total = intOrNone(m.group(1))
    passengers = intOrNone(m.group(2))
    crew = intOrNone(m.group(3))
    return (total, passengers, crew)

def parse_route(route):
    if route:
        parts = route.split(' - ')
        if len(parts) >= 2:
            departure = parts[0]
            destination = parts[-1]
            return (departure, destination)
    return (None, None)


def parse_location(location):
    if location and location != '?':
        location = location.strip()
        parts = [s.strip() for s in location.split(',')]
        country, location = parts[-1], u', '.join(parts[:-1])
        return match_country(country), location
    else:
        return None, None


def parse_airline(airline):
    if airline:
        airline = re.sub(r'/.*', '', airline)
        airline = re.sub(r'^Military -', '', airline)
        airline = airline.strip()
        return airline

def process(data, session):
    date = get_date(data)
    time = get_time(data)
    airline = parse_airline(data.get('Operator'))
    type = clean_string(data.get('AC\n        Type'))
    manufacturer, plane_type = find_manufacturer(type, session)
    registration = clean_string(data.get('Registration'))
    number = clean_string(data.get('Flight #'))

    departure, destination = parse_route(data.get('Route'))

    total, passengers, crew = parse_people(data.get('Aboard'))
    deaths_total, deaths_passengers, deaths_crew = parse_people(data.get('Fatalities'))

    phase = None
    weather = None
    country, location = parse_location(data.get('Location'))
    source = u'planecrash.info'

    add = True
    if date is not None:
        event = find_event(date, registration, session)
        if event is not None:
            print 'Duplicate'
            add = False

    if add:
        add_event(**locals())


def input_stream():
    with open('../planecrashinfo-data') as input:
        for row in input.readlines():
            data = eval(row)
            yield unicodize(data)

if __name__ == '__main__':
    process_data(input_stream(), process)


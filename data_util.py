
import countries
import us_states as USA
import canadian_provinces as Canada

from model import PlaneManufacturer, Plane, PlaneType, Airline, Flight, Event
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.exc import NoResultFound
import re
from string_utils import *


def get_engine(name):
    return create_engine('sqlite:///{}'.format(name))

def get_airline(airline, session):
    if airline:
        flat = flatten_name(airline)
        try:
            return session.query(Airline).filter(Airline.name_lower==flat).one()
        except NoResultFound:
            a = Airline(name=airline, name_lower=flat)
            session.add(a)
            return a

def get_manufacturer(name, session):
    if name:
        flat = flatten_name(name)
        try:
            return session.query(PlaneManufacturer)\
                    .filter(PlaneManufacturer.name_lower==flat).one()
        except NoResultFound:
            m = PlaneManufacturer(name=name, name_lower=flat)
            session.add(m)
            return m

def get_plane_type(type, manufacturer, session):
    if type:
        flat = flatten_name(type)
        try:
            return session.query(PlaneType)\
                    .filter(PlaneType.manufacturer==manufacturer,
                            PlaneType.model_lower==flat).one()
        except NoResultFound:
            t = PlaneType(model=type, model_lower=flat, manufacturer=manufacturer)
            session.add(t)
            return t

def get_plane(registration, type, session):
    if registration:
        try:
            return session.query(Plane)\
                .filter(Plane.registration_number==registration).one()
        except NoResultFound:
            p = Plane(registration_number=registration, type=type)
            session.add(p)
            return p

def process_data(input_stream, process):
    e = get_engine('database')
    session_factory = sessionmaker(bind=e)
    session = session_factory()

    for i, data in enumerate(input_stream):
        if i % 500 == 0:
            print 'Row {}'.format(i)
            session.commit()
            print 'commited'
        process(data, session)
    session.commit()

def dict_subset(data, *entries):
    return {k: data[k] for k in entries}

def add_event(session, **p):
    airline = get_airline(p['airline'], session)
    manufacturer = get_manufacturer(p['manufacturer'], session)
    plane_type = get_plane_type(p['plane_type'], manufacturer, session)
    plane = get_plane(p['registration'], plane_type, session)

    flight_data = dict_subset(p,
            'number', 'departure', 'destination',
            'total', 'crew', 'passengers')
    event_data = dict_subset(p,
            'date', 'time', 'deaths_total', 'deaths_crew', 'deaths_passengers',
            'weather', 'phase', 'country', 'location')

    flight = Flight(airline=airline, plane=plane, **flight_data)
    event = Event(flight=flight, **event_data)

    session.add_all([flight, event])

def match_country(country):
        country = re.sub('[Nn]ear ', '', country, flags=re.I)
        country = re.sub('[Oo]ff', '', country, flags=re.I)
        country = re.sub('[Oo]ver( the)?', '', country, flags=re.I)
        country = re.sub(r'\d+', '', country)
        country = re.sub(r'\(.*\)', '', country)
        country = country.strip()
        options = list(countries.names) + list(USA.full_names) + list(USA.shortcuts) + list(Canada.provinces)

        if country not in options:
            best, d = best_match(country, options)
            q = d / float(len(country))
            if q > 0.2:
                country2 = re.sub(r'(north|south|east|west)(ern)?', '', country, flags=re.I)
                country2 = re.sub(r'(north|south|east|west)(ern)?', '', country2, flags=re.I)
                country2 = re.sub(r'central', '', country2, flags=re.I)
                country2 = re.sub(r'(republic|of|miles|the) ', '', country2, flags=re.I)
                country2 = re.sub(r'coast', '', country2, flags=re.I)
                country2 = country2.strip()
                if country != country2:
                    country = country2
                    best, d = best_match(country, options)
                    q = d / float(len(country))
            if q <= 0.2:
                country = best
            else:
                print repr(country), '-->', best, '({:2.1%})'.format(q)
        if country in USA.full_names or country in USA.shortcuts:
            return u'USA'
        elif country in Canada.provinces:
            return u'Canada'
        else:
            return country
        return None

def try_find_manufacturer(name, session):
    try:
        flat = flatten_name(name)
        return session.query(PlaneManufacturer)\
                .filter(PlaneManufacturer.name_lower==flat).one()
    except NoResultFound:
        pass

def is_it_a_model_number(name):
    if any(c.isdigit() for c in name):
        return True
    if is_roman_numeral(name):
        return True
    if name.lower() in 'model':
        return False
    return False

def split_at_manufacturer_name(parts):
    for i in xrange(len(parts)):
        if is_it_a_model_number(parts[i]):
            make, model = parts[:i], parts[i:]
            return (' '.join(make), ' '.join(model))
    return (None, None)

def find_manufacturer_with_separator(name):
    if name:
        parts = name.split('|')
        if len(parts) > 1:
            manufacturer, model = parts
            return (manufacturer, model)

def find_manufacturer(name, session):
    with_sep = find_manufacturer_with_separator(name)
    if with_sep:
        return tuple(with_sep)
    if name:
        name = clean_string(name)
        parts = name.split()
        for i in xrange(1, len(parts) + 1):
            make = u' '.join(parts[:i])
            manufacturer = try_find_manufacturer(make, session)
            if manufacturer:
                manufacturer_name = manufacturer.name
                type = u' '.join(parts[i:])
                break
        else:
            print u'Fuk, dupa dla {!r}'.format(name)
            manufacturer_name, type = split_at_manufacturer_name(parts)
            if not manufacturer_name:
                print u'I am clueless :('
                return (None, name)
            else:
                print u'How about {!r} ?'.format(manufacturer_name)

        return (manufacturer_name, type)
    return (None, None)

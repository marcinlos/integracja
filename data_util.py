
from model import Plane, PlaneType, Airline, Flight, Event
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.exc import NoResultFound
import re
from string_utils import flatten_name, orNone, intOrNone


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

def get_plane_type(type, session):
    if type:
        flat = flatten_name(type)
        try:
            return session.query(PlaneType).filter(PlaneType.name_lower==flat).one()
        except NoResultFound:
            t = PlaneType(name=type, name_lower=flat)
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
    plane_type = get_plane_type(p['plane_type'], session)
    plane = get_plane(p['registration'], plane_type, session)

    flight_data = dict_subset(p,
            'number', 'departure', 'destination',
            'total', 'crew', 'passengers')
    event_data = dict_subset(p,
            'date', 'time', 'deaths_total', 'deaths_crew', 'deaths_passengers',
            'weather', 'phase', 'country', 'location')

    flight = Flight(airline=airline, **flight_data)
    event = Event(flight=flight, **event_data)

    session.add_all([flight, event])


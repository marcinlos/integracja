
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, ForeignKey, Integer, Unicode, Date, Time
from sqlalchemy.orm import relationship, backref

Base = declarative_base()

class PlaneManufacturer(Base):
    __tablename__ = 'manufacturer'

    id = Column(Integer, primary_key=True)
    name = Column(Unicode, index=True, unique=True)
    name_lower = Column(Unicode, index=True, unique=True)

    def __repr__(self):
        return 'PlaneManufacturer(name = {})'.format(self.name)

class PlaneType(Base):
    __tablename__ = 'plane_types'

    id = Column(Integer, primary_key=True)
    model = Column(Unicode)
    model_lower = Column(Unicode, index=True)
    manufacturer_id = Column(Integer, ForeignKey('manufacturer.id'))
    manufacturer = relationship('PlaneManufacturer')

    def __repr__(self):
        return 'PlaneType(model = {})'.format(self.model)

class Plane(Base):
    __tablename__ = 'planes'

    id = Column(Integer, primary_key=True)
    type_id = Column(Integer, ForeignKey('plane_types.id'))
    registration_number = Column(Integer, index=True, unique=True)
    type = relationship('PlaneType')

    def __repr__(self):
        return 'Plane(registration = {})'.format(self.registration_number)

class Airline(Base):
    __tablename__ = 'airlines'

    id = Column(Integer, primary_key=True)
    name = Column(Unicode, index=True, unique=True)
    name_lower = Column(Unicode, index=True, unique=True)

    def __repr__(self):
        return 'Airline(name = {})'.format(self.name)

class Flight(Base):
    __tablename__ = 'flights'

    id = Column(Integer, primary_key=True)
    number = Column(Unicode)
    departure = Column(Unicode)
    destination = Column(Unicode)
    crew = Column(Integer)
    passengers = Column(Integer)
    total = Column(Integer)
    airline_id = Column(Integer, ForeignKey('airlines.id'))
    plane_id = Column(Integer, ForeignKey('planes.id'))

    airline = relationship('Airline', backref='flights')
    plane = relationship('Plane', backref='flights')

    def __repr__(self):
        return 'Flight(number={}, departure={}, destination={}, people={})'\
            .format(self.number, self.departure, self.destination, self.people)

class Event(Base):
    __tablename__ = 'event'

    id = Column(Integer, primary_key=True)
    date = Column(Date)
    time = Column(Time)
    deaths_total = Column(Integer)
    deaths_crew = Column(Integer)
    deaths_passengers = Column(Integer)
    weather = Column(Unicode)
    phase = Column(Unicode)
    country = Column(Unicode)
    location = Column(Unicode)
    description = Column(Unicode)
    source = Column(Unicode)
    flight_id = Column(Integer, ForeignKey('flights.id'))

    flight = relationship('Flight', backref='events')

    def __repr__(self):
        return 'Event(date={}, time={}, deaths={} ({}/{}), weather={}, phase={},\
            country={}, location={}, desc={}'.format(self.date, self.time,
                    self.deaths_total, self.deaths_crew, self.deaths_passengers,
                    self.weather, self.phase, self.place, self.description)




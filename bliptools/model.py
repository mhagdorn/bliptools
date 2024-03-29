__all__ = ['Entry', 'BlipDB']

import numpy

from sqlalchemy import Column, Integer, String, Date, Float, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

Base = declarative_base()


class Entry(Base):
    __tablename__ = 'entries'

    entry_id = Column(Integer, primary_key=True)
    date = Column(Date)
    title = Column(String)
    username = Column(String)
    lat = Column(Float)
    lon = Column(Float)
    thumbnail_url = Column(String)
    image_url = Column(String)


class BlipDB:
    def __init__(self, dbstring):
        self._eng = create_engine(dbstring)
        Base.metadata.bind = self._eng
        Base.metadata.create_all()
        Session = sessionmaker(bind=self._eng)
        self._session = Session()

    @property
    def session(self):
        return self._session

    @property
    def latest(self):
        return self.session.query(func.max(Entry.date)).one_or_none()[0]

    def commit(self):
        self.session.commit()

    def add(self, entry_id, date, title, username, lat, lon,
            thumbnail_url, image_url):
        self.session.add(Entry(entry_id=entry_id,
                               date=date,
                               title=title,
                               username=username,
                               lat=lat,
                               lon=lon,
                               thumbnail_url=thumbnail_url,
                               image_url=image_url))

    def get_locations(self):
        locations = []
        for l in self.session.query(Entry.lon, Entry.lat).all():
            if l[0] is not None and l[1] is not None:
                locations.append(l)
        return numpy.array(locations)

    def get_entries_with_location(self, start=None, end=None):
        filter = [Entry.lat.isnot(None), Entry.lon.isnot(None)]
        if start is not None:
            filter.append(Entry.date >= start)
        if end is not None:
            filter.append(Entry.date <= end)
        for l in self.session.query(Entry).filter(*filter).all():
            yield l


if __name__ == '__main__':
    db = BlipDB('sqlite:///test.sqlite')

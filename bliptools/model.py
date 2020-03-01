__all__ = ['Entry','get_session']

from sqlalchemy import Column, Integer, String, Date, Float
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

class DBSession:
    def __init__(self):
        self._eng = None
        self._session = None
        
    def __call__(self,dbstring):
        if self._session is None:
            self._eng = create_engine(dbstring)
            Base.metadata.bind = self._eng
            Base.metadata.create_all()
            Session = sessionmaker(bind=self._eng)
            self._session = Session()
        return self._session

get_session = DBSession()


if __name__ == '__main__':
    session = get_session('sqlite:///test.sqlite')

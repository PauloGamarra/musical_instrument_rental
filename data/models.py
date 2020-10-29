from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date, Boolean, ForeignKey, CheckConstraint
from flask_login import UserMixin, LoginManager

Base = declarative_base()

class Users(UserMixin, Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String, unique=True)
    password = Column(String)

    def __repr__(self):
        return "<User(name='%s', email='%s', password='%s')>" % (self.name, self.email, self.password)

class Instruments(Base):
    __tablename__ = 'instruments'

    id = Column(String, primary_key=True)
    instrument_class = Column(String)
    instrument = Column(String)
    brand = Column(String)
    model = Column(String)
    registry = Column(String)
    
    def __repr__(self):
        return "<Instrument(class='%s', instrument='%s', brand='%s', model='%s', registry='%s')>" % (self.instrument_class, self.instrument, self.brand, self.model, self.registry)

class AdvertsData(Base):
    __tablename__ = 'adverts_data'

    id = Column(String, primary_key=True)
    prices = Column(String)
    locator = Column(String, ForeignKey('users.email'))
    instrument = Column(String, ForeignKey('instruments.id'))

    def __repr__(self):
        return "<AdvertData(prices='%s', locator='%s', instrument='%s')>" % (self.prices, self.locator, self.instrument)

class Adverts(Base):
    __tablename__ = 'adverts'

    id = Column(Integer, primary_key=True)
    active = Column(Boolean, default=True)
    data = Column(String, ForeignKey('adverts_data.id'))

    def __repr__(self):
        return "<Advert(active='%s', data='%s')>" % (self.active, self.data)

class Loans(Base):
    __tablename__ = 'loans'

    id = Column(String, primary_key=True)
    withdrawal = Column(Date)
    devolution = Column(Date)
    lessee = Column(String, ForeignKey('users.email'))
    ad = Column(String, ForeignKey('adverts.data'))

    def __repr__(self):
        return "<Loan(withdrawal='%s', devolution='%s', lessee='%s', ad='%s')>" % (self.withdrawal, self.devolution, self.lessee, self.ad)

class Records(Base):
    __tablename__ = 'records'

    id = Column(Integer, primary_key=True)
    loan = Column(String, ForeignKey('loans.id'))
    rating = Column(Integer, CheckConstraint('rating >= 0 AND rating <= 10'))

    def __repr__(self):
        return "<Record(loan='%s', rating='%s')>" % (self.loan, self.rating)

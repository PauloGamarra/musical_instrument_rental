from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
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

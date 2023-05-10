import sqlalchemy
import sqlalchemy.orm
from sqlalchemy import Column, String, Integer, FLOAT
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Store(Base):
    __tablename__ = 'store'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    latitude = Column(FLOAT)
    longitude = Column(FLOAT)
    flyer_url = Column(String)
    url_type = Column(Integer)

class Item(Base):
    __tablename__ = 'item'

    id = Column(Integer, primary_key=True)
    name = Column(String)

class Recipe(Base):
    __tablename__ = 'recipe'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    time = Column(Integer)
    url = Column(String)

class Ingredient(Base):
    __tablename__ = 'ingredient'

    id = Column(Integer, primary_key=True)
    name = Column(String)

class Handling(Base):
    __tablename__ = 'handling'

    store_id = Column(Integer, primary_key=True)
    item_id = Column(Integer, primary_key=True)
    price = Column(Integer)

class Need(Base):
    __tablename__ = 'need'

    recipe_id = Column(Integer, primary_key=True)
    ingredient_id = Column(Integer, primary_key=True)

engine = sqlalchemy.create_engine('sqlite:///db.sqlite3', echo=True)
Session = sqlalchemy.orm.sessionmaker(bind=engine)
session = Session()
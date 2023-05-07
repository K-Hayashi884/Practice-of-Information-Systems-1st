import sqlalchemy
import sqlalchemy.orm
from sqlalchemy import Column, String, Integer, FLOAT
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
engine = sqlalchemy.create_engine('sqlite:///db.sqlite3', echo=True)
Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)
Session = sqlalchemy.orm.sessionmaker(bind=engine)
session = Session()

class Store(Base):
    __tablename__ = 'store'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    latitude = Column(FLOAT)
    longitude = Column(FLOAT)
    flyer_url = Column(String)

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
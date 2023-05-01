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

def add_data():
    engine = sqlalchemy.create_engine('sqlite:///db.sqlite3', echo=True)
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    Session = sqlalchemy.orm.sessionmaker(bind=engine)
    session = Session()

    print("======== Store data reset ========")
    session.query(Store).delete()
    stores = [
        Store(id=1, name="コープ岩倉", latitude=135.51, longitude=36.51, flyer_url="url1"),
        Store(id=2, name="エムジーショップ岩倉", latitude=135.52, longitude=36.52, flyer_url="url2"),
        Store(id=3, name="Aコープ岩倉", latitude=135.53, longitude=36.53, flyer_url="url3"),
    ]
    session.add_all(stores)

    print("======== Item data reset ========")
    session.query(Item).delete()
    items = [
        Item(id=1, name="ばれいしょ"),
        Item(id=2, name="インカのめざめ"),
        Item(id=3, name="メークイン"),
    ]
    session.add_all(items)

    print("======== Recipe data reset ========")
    session.query(Recipe).delete()
    recipes = [
        Recipe(id=1, name="じゃがいもスープ", time=10, url="http1"),
        Recipe(id=2, name="にんじんスープ", time=20, url="http2"),
        Recipe(id=3, name="きゅうりスープ", time=30, url="http3"),
    ]
    session.add_all(recipes)

    print("======== Ingredient data reset ========")
    session.query(Ingredient).delete()
    ingredients = [
        Ingredient(id=1, name="じゃがいも"),
        Ingredient(id=2, name="にんじん"),
        Ingredient(id=3, name="きゅうり"),
    ]

    session.add_all(ingredients)

    print("======== Handling data reset ========")
    session.query(Handling).delete()
    handlings = [
        Handling(store_id=1, item_id=1, price=100),
        Handling(store_id=1, item_id=2, price=150),
        Handling(store_id=2, item_id=3, price=300),
    ]

    session.add_all(handlings)

    print("======== Need data reset ========")
    session.query(Need).delete()
    needs = [
        Need(recipe_id=1, ingredient_id=1),
        Need(recipe_id=1, ingredient_id=2),
        Need(recipe_id=2, ingredient_id=3),
    ]

    session.add_all(needs)

    session.commit()

def print_all_store(session):
    stores = session.query(Store).all()
    for store in stores:
        print(store.name)


if __name__ == '__main__':
    add_data()
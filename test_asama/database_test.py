import sqlalchemy
import sqlalchemy.orm
from db_model import (
    session,
    Store,
    Item,
    Handling,
    Recipe,
    Ingredient,
    Need
)

def get_store(id: int = -1, name: str = ""):
    if id == -1 and name == "":
        stores = session.query(Store).all()
    elif id == -1:
        stores = session.query(Store).filter(Store.name==name)
    else:
        stores = session.query(Store).filter(Store.id==id)
    
    result: list[tuple[int, str, float, float, str]] = []
    for store in stores:
        result.append((store.id, store.name, store.latitude, store.longitude, store.flyer_url))

    return stores

def get_item(id: int = -1, name: str = ""):
    if id == -1 and name == "":
        items = session.query(Item).all()
    elif id == -1:
        items = session.query(Item).filter(Item.name==name)
    else:
        items = session.query(Item).filter(Item.id==id)
    
    result: list[tuple[int, str]] = []
    for item in items:
        result.append((item.id, item.name))

    return result

def get_recipe():
    recipes = session.query(Recipe).all()
    return recipes

def add_item(name: str):
    item = Item(name=name)
    session.add(item)
    session.commit()
    return item.id

def add_handling(store_id: int, item_id: int):
    handling = Handling(store_id=store_id, item_id=item_id)
    session.add(handling)
    session.commit()

def add_store(store_name: str, latitude: float, longitude: float, url:str):
    store = Store(name=store_name, latitude=latitude, longitude=longitude, flyer_url = url)
    session.add(store)
    session.commit()
    return store.id

def clear_item():
    session.query(Item).delete()
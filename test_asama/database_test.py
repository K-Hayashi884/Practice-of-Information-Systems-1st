import sqlalchemy
import sqlalchemy.orm
from db_Init import Store, Item, Recipe, Ingredient, Handling, Need

def get_session():
    engine = sqlalchemy.create_engine('sqlite:///db.sqlite3', echo=True)
    Session = sqlalchemy.orm.sessionmaker(bind=engine)
    session = Session()
    return session

def get_store(id: int = -1, name: str = ""):
    session = get_session()
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
    session = get_session()
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

def add_item(name: str):
    session = get_session()
    item = Item(name=name)
    session.add(item)
    session.commit()
    return item.id

def add_handling(store_id: int, item_id: int):
    session = get_session()
    handling = Handling(store_id=store_id, item_id=item_id)
    session.add(handling)
    session.commit()

def clear_item():
    session = get_session()
    session.query(Item).delete()
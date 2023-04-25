import sqlite3

def connect():
    return sqlite3.connect('test_asama/TestDB.db')

def searchByStore():
    db = connect()
    res = db.execute("SELECT * FROM store")
    print(res)
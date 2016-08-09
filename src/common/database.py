import os

import pymongo

class Database(object):

    URI = os.environ.get("MONGOLAB_URI")
    DATABASE = None

    @staticmethod
    def initialize():
        client = pymongo.MongoClient(Database.URI)
        Database.DATABASE = client['fullstack']

    @staticmethod
    def insert(collection, data):
        Database.DATABASE[collection].insert(data)

    @staticmethod
    def find(collection, query):
        return Database.DATABASE[collection].find(query) # devuelve un cursor

    @staticmethod
    def find_one(collection, query):
        return Database.DATABASE[collection].find_one(query) # No trae un cursor. el cursor se usa para empezar al ppio de la collection y despues ir a cada uno.
                                                        # trae el primer elemento que devuelve el cursor
                                                        # devuelve un objeto json

    @staticmethod
    def update(collection, query, data):
        Database.DATABASE[collection].update(query, data, upsert=True) # upsert --> si no encontras elemento de esta query, en lugar de update hace insert


    @staticmethod
    def remove(colletion, query):
        Database.DATABASE[colletion].remove(query)
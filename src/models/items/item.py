import re
import uuid

import requests
from bs4 import BeautifulSoup
from src.models.items import constants as ItemConstants

from src.common.database import Database
from src.models.stores.store import Store


class Item(object):

    def __init__(self, name, url, price=None, _id=None):
        self.name = name
        self.url = url
        store = Store.find_by_url(url)
        self.tag_name = store.tag_name # cada stores puede usar un tag distinto en el html para el precio - pero dentro del stores va a ser siempre el mismo
        self.query = store.query  #   l identificador de html va a ser el mismo para el stores
        self.price = None if price is None else price # Antes estaba asi --> self.load_price(tag_name, query) --> pero no quiere ponerlo en el constructor
        self._id = uuid.uuid4().hex if _id == None else _id


    def __repr__(self):
        return "<Item {} wth URL {}>".format(self.name, self.price)


    def load_price(self):
        request = requests.get(self.url)
        content = request.content
        soup = BeautifulSoup(content, "html.parser")
        element = soup.find(self.tag_name, self.query)  # ('span', {'id':'priceblock_ourprice'})

        string_price = element.text.strip()
        if string_price.find(",") != -1:
            string_price = string_price[:string_price.find(",")] + string_price[string_price.find(",")+1:] # agregue esto porque no reconocia la coma de mil

        pattern = re.compile("(\d+.\d+)") # \d -> set of numbers . set of numbers

        match = pattern.search(string_price)  # asi encuentra la primera ocurrencia (por si hay mas de u precio)


        self.price = float(match.group())
        return self.price


    def save_to_mongo(self):
        Database.update(ItemConstants.COLLECTION, {'_id': self._id}, self.json())


    def json(self):
        return{
            '_id': self._id,
            'name': self.name,
            'url': self.url,
            'price': self.price
        }


    def from_mongo(self):
        Database.find_one(ItemConstants.COLLECTION, {'_id': self._id})


    @classmethod
    def get_by_id(cls, id):
        return cls(**Database.find_one(ItemConstants.COLLECTION, {'_id': id}))

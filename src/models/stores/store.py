import uuid
import src.models.stores.constants as StoreConstants
from src.common.database import Database
import src.models.stores.errors as StoreErrors


class Store(object):

    def __init__(self, name, url_prefix, tag_name, query, _id=None):
        self.name = name
        self.url_prefix = url_prefix
        self.tag_name = tag_name
        self.query = query
        self._id = uuid.uuid4().hex if _id == None else _id


    def __repr__(self):
        return "<Store {}>".format(self.name)


    def json(self):
        return {
            '_id': self._id,
            'name': self.name,
            'url_prefix': self.url_prefix,
            'tag_name':  self.tag_name,
            'query': self.query
        }


    @classmethod
    def get_by_id(cls, id):
        return cls(**Database.find_one(StoreConstants.COLLECTION, {'_id': id}))


    def save_to_mongo(self):
        Database.update(StoreConstants.COLLECTION, {'_id': self._id}, self.json())


    @classmethod
    def get_by_name(cls, store_name):
        return cls(**Database.find_one(StoreConstants.COLLECTION, {'name': store_name}))


    @classmethod
    def get_by_url_prefix(cls, url_prefix):
        #Al ponerle el prefijo va a ir buscando letra por letra si encuentra un match en la bd con las url de las stores
        return cls(**Database.find_one(StoreConstants.COLLECTION, {'url_prefix': {"$regex":'^{}'.format(url_prefix)}}))     #  {"$regex":'^{}'.format(url_prefix)}  --> decimos que va a ser regex y ^ marca el inicio y metemos en formato el url_prefix


    @classmethod
    def find_by_url(cls, url):
        '''
        Rerurrn a stores from a url like "http://www.johnlewis.com/item/ndcbbckjebceui"
        :param url: item's url
        :return: a stores, or raises a StoreNotFoundException if no Store matches the url
        '''
        for i in  range(0, len(url)+1): # +1 porque en [:] el ultimo no se tiene en cuenta
            try:
                store = cls.get_by_url_prefix(url[:i])
                return store
            except:
              #  pass # en este caso es lo mismo que  return None porque por default pthon devuelve None si no encunetra
                raise StoreErrors.StoreNotFoundException("The URL Prefix used to find the stores didn't give us any result!")


    @classmethod
    def all(cls):
        return [cls(**elem) for elem in Database.find(StoreConstants.COLLECTION, {})]


    def delete(self):
        Database.remove(StoreConstants.COLLECTION, {'_id':self._id})
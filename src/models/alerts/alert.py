import uuid
import datetime


import requests
import src.models.alerts.constants as AlertConstants
from src.common.database import Database
from src.models.items.item import Item


class Alert(object):

    def __init__(self, user_email, price_limit, item_id, active=True,  last_checked=None, _id=None):
        self.user_email = user_email
        self.price_limit = price_limit
        self.item = Item.get_by_id(item_id)
        self.last_checked = datetime.datetime.utcnow() if last_checked is None else last_checked # si viene de la bd
        self._id = uuid.uuid4().hex if _id is None else _id
        self.active = active


    def __repr__(self):
        return "<Alert for {} on item {} with price {}>".format(self.user_email, self.item.name, self.price_limit)


    def send(self):
        return requests.post(
            AlertConstants.URL,
            auth=("api", AlertConstants.API_KEY),
            data={
                "from": AlertConstants.FROM,
                "to": self.user_email,
                "subject": "Price limit reached for {}".format(self.item.name),
                "text": "We've found a deal! ({}).\nTo navigate to the alert visit {}.".format(
                    self.item.url, "http://pricing.jslvtr.com/alerts/{}".format(self._id)) # como el alert updater es independiente no tiene los endpoints asi que no podemos usar url_for() y hay que hardcodear
            }
        )

    @classmethod
    def find_needing_update(cls, minutes_since_update=AlertConstants.ALERT_TIMEOUT):
        last_updated_limit = datetime.datetime.utcnow() - datetime.timedelta(minutes_since_update)
        return [cls(**elem) for elem in Database.find(AlertConstants.COLLECTION, {"active": True,
                                                                                  "last_checked":
                                                                                      {"$lte":last_updated_limit}
                                                                                  })]   #$lte-> less than or equal
                                                                                        # $gte greater than or equal to

    def save_to_mongo(self):
        Database.update(AlertConstants.COLLECTION, {"_id": self._id}, self.json()) # --> busco el alert con ese id y le updateo con la info del json. si no existe la creo


    def json(self):
        return {
            "_id":self._id,
            "price_limit": self.price_limit,
            "last_checked": self.last_checked,
            "user_email": self.user_email,
            "item_id": self.item._id,
            "active": self.active
        }

    def load_item_price(self):
        self.item.load_price()
        self.last_checked = datetime.datetime.utcnow()
        self.item.save_to_mongo()
        self.save_to_mongo()
        return self.item.price


    def send_email_if_price_reached(self):
        if self.item.price < self.price_limit:
            self.send()

    @classmethod
    def find_by_user_email(cls, email):
        return [cls(**elem) for elem in Database.find(AlertConstants.COLLECTION, {'user_email': email})]

    @classmethod
    def find_by_id(cls, alert_id):
        return cls(**Database.find_one(AlertConstants.COLLECTION, {'_id': alert_id}))

    def deactivate(self):
        self.active = False
        self.save_to_mongo()


    def activate(self):
        self.active = True
        self.save_to_mongo()


    def delete(self):
        Database.remove(AlertConstants.COLLECTION, {'_id': self._id})
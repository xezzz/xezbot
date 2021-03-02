from core import config
from pymongo import MongoClient



class Database(MongoClient):
    def __init__(self, host=config.DB_PASS, port=None, **kwargs):
        super().__init__(host=host, port=port, **kwargs)


    @property
    def channels(self):
        cluster = self.general
        return cluster.channels


    @property
    def commands(self):
        cluster = self.general
        return cluster.commands

    
    @property
    def configs(self):
        cluster = self.general
        return cluster.channel_configs

    

    @staticmethod
    def get(collection, filter_obj, filter_value, key):
        for _ in collection.find({f"{filter_obj}": f"{filter_value}"}):
            return _[f"{key}"]


    @staticmethod
    def insert(collection, model):
        collection.insert(model)


    @staticmethod
    def update(collection, filter_obj, filter_value, key, value):
        collection.update({f"{filter_obj}": f"{filter_value}"}, {"$set": {f"{key}": value}}, upsert=False, multi=False)


    @staticmethod
    def delete(collection, filter_obj, filter_value):
        collection.delete_one({f"{filter_obj}": f"{filter_value}"})
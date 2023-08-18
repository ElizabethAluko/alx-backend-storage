#!/usr/bin/env python3
"""The module contains a function that insert a new documents in a collection"""


def insert_school(mongo_collection, **kwargs):
    """Insert a new document in a collection based on kwargs
       
       Returns: new _id

       mongo_collection is a pymongo collection object
    """
    new_document = mongo_collection.insert_one(kwargs)
    return new_document.inserted_id

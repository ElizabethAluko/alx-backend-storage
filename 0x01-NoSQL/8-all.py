#!/usr/bin/env python3
"""The module contains a function that list all documents in a collection"""


def list_all(mongo_collection):
    """Returns lists of all documents in a collection
       Return an empty list if no document in the collection
       mongo_collection is a pymongo collection object
    """
    documents = list(mongo_collection.find({}))
    return documents

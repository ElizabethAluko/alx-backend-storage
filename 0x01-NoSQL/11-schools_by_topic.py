#!/usr/bin/env python3

"""
This module provides functions to interact with a MongoDB collection.
"""

import pymongo

def schools_by_topic(mongo_collection, topic):
    """
    Get a list of schools that have a specific topic.

    Args:
        mongo_collection (pymongo.collection.Collection): The pymongo collection object.
        topic (str): The topic to search for.

    Returns:
        list: List of school documents matching the topic.
    """
    # Find documents that have the specified topic in their "topics" field
    schools = list(mongo_collection.find({ "topics": topic }))
    
    return schools

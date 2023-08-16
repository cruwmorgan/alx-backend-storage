#!/usr/bin/env python3
""" function that changes all topics of a school document based on the name """
import pymongo
from typing import List


def update_topics(mongo_collection, name, topics):
    """ Change all topics
    
        Args:
            mongo_collection: the pymongo collection object
            name: school name to update
            topics: list of topics approached in the school

        Return:
            Nothing
    """
    query: dict = {'name': name}
    mongo_collection.update_many(query, {"$set": {"topics": topics}})

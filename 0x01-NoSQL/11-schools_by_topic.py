#!/usr/bin/env python3
"""function that returns the list of school having a specific topic:"""
import pymongo


def schools_by_topic(mongo_collection, topic: str):
    """ Search the school based on topic

        Args:
            mongo_collection: pymongo collection object
            topic: topic searched

        Return:
            List of school
    """
    query: dict = {"topics": topic}
    schools: list = []

    for school in mongo_collection.find(query):
        schools.append(school)

    return schools

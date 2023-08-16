#!/usr/bin/env python3
"""function that returns all students sorted by average score:"""
import pymongo


def top_students(mongo_collection):
    """function that returns all students sorted by average score:
        Args:
            mongo_collection: pymongo collection object

        Return:
            all students sorted by average score:
    """
    top_students = mongo_collection.aggregate([
        {
            "$project": {
                "name": "$name",
                "averageScore": {"$avg": "$topics.score"}
            }
        },
        {"$sort": {"averageScore": -1}}
    ])

    return top_students
#!/usr/bin/env python3

"""
This module provides functions to interact with a MongoDB collection.
"""

import pymongo

def top_students(mongo_collection):
    """
    Get all students sorted by average score.

    Args:
        mongo_collection (pymongo.collection.Collection): The pymongo collection object.

    Returns:
        list: List of students sorted by average score.
    """
    students = list(mongo_collection.find({}))

    for student in students:
        total_score = sum(student["scores"])
        student["averageScore"] = total_score / len(student["scores"])

    sorted_students = sorted(students, key=lambda x: x["averageScore"], reverse=True)

    return sorted_students

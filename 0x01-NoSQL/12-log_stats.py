#!/usr/bin/env python3

"""
This script provides statistics about Nginx logs stored in a MongoDB collection.
"""


def get_nginx_logs_stats(mongo_collection):
    """
    Get statistics about Nginx logs stored in the collection.

    Args:
        mongo_collection (pymongo.collection.Collection): The pymongo collection object.

    Returns:
        dict: A dictionary containing the required statistics.
    """
    stats = {}

    # Get the total number of documents in the collection
    total_logs = mongo_collection.count_documents({})
    stats["total_logs"] = total_logs

    # Get statistics about different HTTP methods
    http_methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]
    method_stats = {}
    for method in http_methods:
        method_count = mongo_collection.count_documents({ "method": method })
        method_stats[method] = method_count
    stats["method_stats"] = method_stats

    # Get the number of documents with method=GET and path=/status
    status_path_count = mongo_collection.count_documents({
        "method": "GET",
        "path": "/status"
    })
    stats["status_path_count"] = status_path_count

    return stats

#!/usr/bin/env python3
"""
This module defines the Cache class, which allows storing data in a Redis cache.
"""

import uuid
import redis
from typing import Union

class Cache:
    """
    A class for storing data in a Redis cache.

    Attributes:
        _redis (redis.Redis): The Redis client instance.
    """

    def __init__(self):
        """
        Initializes the Cache instance and flushes the Redis database.
        """
        self._redis = redis.Redis()
        self._redis.flushdb()

    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        Stores the provided data in the Redis cache.

        Args:
            data (Union[str, bytes, int, float]): The data to be stored.

        Returns:
            str: The generated key under which the data is stored in Redis.
        """
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

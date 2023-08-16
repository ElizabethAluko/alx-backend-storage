#!/usr/bin/env python3
"""
This module defines the Cache class, which allows storing and retrieving data in a Redis cache.
"""

import uuid
import redis
from typing import Union, Callable
from functools import wraps

def count_calls(method: Callable) -> Callable:
    """
    Decorator that counts the number of calls to a method.

    Args:
        method (Callable): The method to be decorated.

    Returns:
        Callable: The decorated method.
    """
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        key = method.__qualname__
        self._redis.incr(key)
        return method(self, *args, **kwargs)
    return wrapper

class Cache:
    """
    A class for storing and retrieving data in a Redis cache.

    Attributes:
        _redis (redis.Redis): The Redis client instance.
    """

    def __init__(self):
        """
        Initializes the Cache instance and flushes the Redis database.
        """
        self._redis = redis.Redis()
        self._redis.flushdb()

    @count_calls
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

    def get(self, key: str, fn: Callable = None) -> Union[str, bytes, int, float, None]:
        """
        Retrieves data from the Redis cache using the provided key.

        Args:
            key (str): The key under which the data is stored in Redis.
            fn (Callable, optional): A callable to convert the data to the desired format.

        Returns:
            Union[str, bytes, int, float, None]: The retrieved data, or None if key does not exist.
        """
        data = self._redis.get(key)
        if data is not None and fn is not None:
            return fn(data)
        return data

    def get_str(self, key: str) -> Union[str, None]:
        """
        Retrieves a string from the Redis cache using the provided key.

        Args:
            key (str): The key under which the data is stored in Redis.

        Returns:
            Union[str, None]: The retrieved string, or None if key does not exist.
        """
        return self.get(key, fn=lambda x: x.decode("utf-8"))

    def get_int(self, key: str) -> Union[int, None]:
        """
        Retrieves an integer from the Redis cache using the provided key.

        Args:
            key (str): The key under which the data is stored in Redis.

        Returns:
            Union[int, None]: The retrieved integer, or None if key does not exist.
        """
        return self.get(key, fn=int)

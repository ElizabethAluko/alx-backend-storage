#!/usr/bin/env python3
"""
This module defines the Cache class, related decorators, replay function, and main code.
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

def call_history(method: Callable) -> Callable:
    """
    Decorator that stores the history of inputs and outputs for a function.

    Args:
        method (Callable): The method to be decorated.

    Returns:
        Callable: The decorated method.
    """
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        input_key = method.__qualname__ + ":inputs"
        output_key = method.__qualname__ + ":outputs"
        self._redis.rpush(input_key, str(args))
        result = method(self, *args, **kwargs)
        self._redis.rpush(output_key, str(result))
        return result
    return wrapper

class Cache:
    """
    A class for storing and retrieving data in a Redis cache.
    """

    def __init__(self):
        """
        Initializes the Cache instance and flushes the Redis database.
        """
        self._redis = redis.Redis()
        self._redis.flushdb()

    @count_calls
    @call_history
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

def replay(method: Callable) -> None:
    """
    Displays the history of calls for a given method.

    Args:
        method (Callable): The method to display history for.
    """
    input_key = method.__qualname__ + ":inputs"
    output_key = method.__qualname__ + ":outputs"
    inputs = [eval(args_str) for args_str in cache._redis.lrange(input_key, 0, -1)]
    outputs = cache._redis.lrange(output_key, 0, -1)
    print(f"{method.__qualname__} was called {len(inputs)} times:")
    for args, output in zip(inputs, outputs):
        print(f"{method.__qualname__}{args} -> {output.decode('utf-8')}")

cache = Cache()
cache.store("foo")
cache.store("bar")
cache.store(42)
replay(cache.store)

#!/usr/bin/env python3
"""Writing strings to Redis"""
from uuid import uuid4
import redis
from typing import Union, Callable
from functools import wraps


def count_calls(method: Callable = None) -> Callable:
    """ Decorator and returns the value returned by the original method. """
    name = method.__qualname__

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """ Wrapper method """
        self._redis.incr(name)
        return method(self, *args, **kwargs)

    return wrapper


class Cache:
    """Functionalities"""

    def __init__(self):
        """ Redis Instance """
        self._redis = redis.Redis()
        self._redis.flushdb()

    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """Store the cache

            Args:
                data: bring the information to store

            Return:
                Key or number uuid
        """
        key = str(uuid4())
        self._redis.set(key, data)

        return key

    def get(self, key: str, fn: Callable = None)\
            -> Union[str, bytes, int, float]:
        """
            Get method

            Args:
                key: Redis cached key
                fn: used to convert the data back to the desired format

            Return:
                Key or number uuid
        """
        key = self._redit.get(key)

        if fn:
            return fn(key)

        return key

    def get_str(self, key: str) -> str:
        """ Parametrized get str """
        return self._redit.get(key).decode("utf-8")

    def get_int(self, key: str) -> int:
        """ Parametrized get int """
        value = self._redis.get(key)
        try:
            value = int(value.decode('utf-8'))
        except Exception:
            value = 0

        return value

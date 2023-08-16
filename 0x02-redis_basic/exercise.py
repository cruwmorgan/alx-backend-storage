"""Writing strings to Redis"""
from uuid import uuid4
import redis
from typing import Union, Callable
from functools import wraps


class Cache:
    """Functionalities"""

    def __init__(self):
        """ Redis Instance """
        self._redis = redis.Redis()
        self._redis.flushdb()

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

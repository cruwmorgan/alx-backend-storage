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


def call_history(method: Callable) -> Callable:
    """ Decorator call history that store the history of inputs and outputs
    for a particular function. """

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """ Wraper function """
        input: str = str(args)
        self._redis.rpush(method.__qualname__ + ":inputs", input)

        output = str(method(self, *args, **kwargs))
        self._redis.rpush(method.__qualname__ + ":outputs", output)

        return output

    return wrapper


def replay(func: Callable):
    """ Replay function """
    r = redis.Redis()
    func_name = func.__qualname__
    number_calls = r.get(func_name)

    try:
        number_calls = number_calls.decode('utf-8')
    except Exception:
        number_calls = 0

    print(f'{func_name} was called {number_calls} times:')

    ins = r.lrange(func_name + ":inputs", 0, -1)
    outs = r.lrange(func_name + ":outputs", 0, -1)

    for cin, cout in zip(ins, outs):
        try:
            cin = cin.decode('utf-8')
        except Exception:
            cin = ""
        try:
            cout = cout.decode('utf-8')
        except Exception:
            cout = ""

        print(f'{func_name}(*{cin}) -> {cout}')


class Cache:
    """Functionalities"""

    def __init__(self):
        """ Redis Instance """
        self._redis = redis.Redis()
        self._redis.flushdb()

    @count_calls
    @call_history
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

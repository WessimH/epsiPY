import abc
import math
import threading
import time
import unittest.mock
from abc import abstractmethod


class Shape(abc.ABC):
    @abstractmethod
    def area(self) -> float:
        pass


class Circle(Shape):
    def __init__(self, r: float):
        self.r = r

    def area(self) -> float:
        return math.pi * self.r ** 2


class Rectangle(Shape):
    def __init__(self, h, w):
        self.h = h
        self.w = w

    def area(self) -> float:
        return self.h * self.w


def check_positive(func):
    def wrapper(n: int):
        if n < 0:
            raise ValueError()
        return func(n)

    return wrapper


import time


def timeout_limit(timeout: int):
    def decorator(func):
        def wrapper(*args, **kwargs):
            t0 = time.time()
            func()
            if time.time() - t0 > timeout:
                raise TimeoutError()

        return wrapper

    return decorator


def timeout_limit(timeout: int, raise_exception: bool = False):
    def decorator(func):
        def wrapper(*args, **kwargs):
            result = [None]
            exception = [None]

            def target():
                try:
                    result[0] = func(*args, **kwargs)
                except Exception as e:
                    exception[0] = e

            if raise_exception:
                thread = threading.Thread(target=target)
                thread.start()
                thread.join(timeout)
            else:
                t0 = time.time()
                target()
                if time.time() - t0 > timeout:
                    raise TimeoutError()

            if raise_exception and thread.is_alive():
                raise TimeoutError(f"Function exceeded the time limit of {timeout} second(s).")
            else:
                if exception[0]:
                    raise exception[0]
                return result[0]

        return wrapper

    return decorator

#
# from contextlib import contextmanager
#
# @contextmanager
# def patch(func):

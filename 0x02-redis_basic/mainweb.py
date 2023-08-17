#!/usr/bin/env python3
""" simulate a slow response and test caching. """

from web import get_page

URL: str = "http://slowwly.robertomurray.co.uk"

print(get_page(URL))

print("----------------------------------\n" * 3)

print(get_page(URL))

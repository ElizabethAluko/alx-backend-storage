#!/usr/bin/env python3
"""
This module defines the get_page function that fetches and caches web pages using Redis.
"""

import redis
import requests

def get_page(url: str) -> str:
    """
    Fetches and caches the HTML content of a web page using Redis.

    Args:
        url (str): The URL of the web page.

    Returns:
        str: The HTML content of the web page.
    """
    redis_instance = redis.Redis()

    count_key = f"count:{url}"
    content_key = f"content:{url}"

    # Increment the access count for this URL
    redis_instance.incr(count_key)

    # Check if the content is already cached
    cached_content = redis_instance.get(content_key)
    if cached_content:
        return cached_content.decode("utf-8")

    # Fetch the page content using requests
    response = requests.get(url)
    content = response.text

    # Cache the content with a 10-second expiration
    redis_instance.setex(content_key, 10, content)

    return content

url = "http://slowwly.robertomurray.co.uk/delay/1000/url/https://www.example.com"
page_content = get_page(url)
print(page_content)

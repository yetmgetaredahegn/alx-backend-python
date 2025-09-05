#!/usr/bin/python3
"""
2-lazy_paginate.py
Generator-based lazy loading of paginated user data.
"""

import seed  # your seed.py module for DB connection


def paginate_users(page_size, offset):
    """
    Fetch a page of users from the database.

    Args:
        page_size (int): Number of users per page
        offset (int): Row offset in the table

    Returns:
        list of dict: List of user rows
    """
    connection = seed.connect_to_prodev()
    cursor = connection.cursor(dictionary=True)
    cursor.execute(f"SELECT * FROM user_data LIMIT {page_size} OFFSET {offset}")
    rows = cursor.fetchall()
    cursor.close()
    connection.close()
    return rows


def lazy_paginate(page_size):
    """
    Generator that lazily fetches users from the database page by page.

    Args:
        page_size (int): Number of users per page

    Yields:
        list of dict: One page of users at a time
    """
    offset = 0  # start at the beginning
    while True:  # only one loop as required
        page = paginate_users(page_size, offset)
        if not page:  # stop when no more rows
            break
        yield page  # yield current page
        offset += page_size  # move offset to next page
    return
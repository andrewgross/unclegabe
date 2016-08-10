# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import redis
from mock import patch, Mock
from urlparse import urlparse

from shql.shql import Shql
from shql.helpers import get_connection

test_key = "test_shql"
endpoint = "redis://127.0.0.1:6379/5"


@patch('shql.helpers.error', Mock())  # Silence startup messages
def get_cli():
    clear_redis()
    _, connection = get_connection(endpoint)
    cli = Shql(connection, key=test_key)
    return cli


def clear_redis():
    result = urlparse(endpoint)
    db = result.path[1:]  # Trim leading /
    conn = redis.StrictRedis(host=result.hostname, port=result.port, db=db)
    test_keys = conn.keys(pattern="{}*".format(test_key))
    if test_keys:
        conn.delete(*test_keys)


def add_record(cli, record):
    """
    Adds a record to the queue

        cli: a Shql cli
        record: a tuple of (value, seconds from now)
    """
    cli.client.sheqel.write(record[0], seconds=record[1])

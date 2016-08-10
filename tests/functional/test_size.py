# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from mock import patch

from tests.helpers import get_cli, add_record


@patch('shql.shql.print_result')
@patch('shql.shql.get_input')
def test_size_with_no_queue(user_input, output):
    """Size should return 0 for a queue that does not exist"""
    # When I have an empty queue
    cli = get_cli()

    # And I get the size
    cli.onecmd("size")

    # Then I get a size of 0
    output.assert_called_once_with(0)


@patch('shql.shql.print_result')
@patch('shql.shql.get_input')
def test_size_with_items(user_input, output):
    """Size should return the size of a queue"""
    # When I have a queue with items
    cli = get_cli()
    add_record(cli, ("foo", 0))

    # And I get the size
    cli.onecmd("size")

    # Then I get a size of 1
    output.assert_called_once_with(1)


@patch('shql.shql.print_result')
def test_size_with_items_in_future(output):
    """Size should return the size of a queue including items not available yet"""
    # When I have a queue with items
    cli = get_cli()
    add_record(cli, ("foo", 0))
    add_record(cli, ("bar", 100))

    # And I get the size
    cli.onecmd("size")

    # Then I get a size of 1
    output.assert_called_once_with(2)

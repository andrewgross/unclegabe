# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from mock import patch
from freezegun import freeze_time
from tests.helpers import get_cli, add_record


@patch('shql.shql.print_result')
@patch('shql.shql.get_input')
def test_peek_when_queue_empty(user_input, output):
    """Peek should return nothing if the queue is empty"""
    # When I have queue with no items
    cli = get_cli()

    # And I peek into the queue
    cli.onecmd("peek")

    # Then I get nothing back
    output.call_count.should.equal(0)


@freeze_time("2012-01-14 03:21:34")
@patch('shql.shql.print_result')
@patch('shql.shql.get_input')
def test_peek_when_queue_is_not_empty(user_input, output):
    """Peek should return an item and it's scheduled time"""
    # When I have queue with an item
    cli = get_cli()
    add_record(cli, ("foo", 0))

    # And I peek into the queue
    cli.onecmd("peek")

    # Then I get that the item exists
    output.assert_called_once_with("foo", "2012-01-14 03:21:34")

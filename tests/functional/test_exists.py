# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from mock import patch
from freezegun import freeze_time

from tests.helpers import get_cli, add_record


@freeze_time("2012-01-14 03:21:34")
@patch('shql.shql.print_result')
@patch('shql.shql.get_input')
def test_exists_when_item_exists(user_input, output):
    """Exists should return true if the item exists"""
    # When I have queue with an item
    cli = get_cli()
    add_record(cli, ("foo", 0))

    # And I check for the item
    cli.onecmd("exists foo")

    # Then I get that the item exists and is scheduled
    output.assert_called_once_with(True, "2012-01-14 03:21:34")


@patch('shql.shql.print_result')
@patch('shql.shql.get_input')
def test_exists_when_item_doesnt_exist(user_input, output):
    """Exists should return false if the item does not exist"""
    # When I have queue with an item
    cli = get_cli()
    add_record(cli, ("foo", 0))

    # And I check for a different item
    cli.onecmd("exists bar")

    # Then I get that the item does not exist
    output.assert_called_once_with(False)

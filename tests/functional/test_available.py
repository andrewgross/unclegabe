# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from mock import patch
from freezegun import freeze_time
from tests.helpers import get_cli, add_record
from shql.exceptions import TooManyArguments


@freeze_time("2012-01-14 03:21:34")
@patch('shql.shql.print_result')
def test_available_with_no_time(output):
    """Available should return a count of items currently available but not include items in the future"""
    # When I have queue with items
    cli = get_cli()
    add_record(cli, ("foo", -10))
    add_record(cli, ("bar", 0))
    add_record(cli, ("baz", 10))

    # And I check for item availablility with no [time]
    cli.onecmd("available")

    # Then I get a count of the items available now
    output.assert_called_with(2)


@freeze_time("2012-01-14 03:21:34")
@patch('shql.shql.print_result')
def test_available_with_time(output):
    """Available should return a count of items available in the future when given a time"""
    # When I have queue with items
    cli = get_cli()
    add_record(cli, ("foo", -10))
    add_record(cli, ("bar", 0))
    add_record(cli, ("baz", 10))

    # And I check for item availablility with time
    cli.onecmd("available 11")

    # Then I get a count of the items available by that time
    output.assert_called_with(3)


@freeze_time("2012-01-14 03:21:34")
@patch('shql.helpers.print_error')
def test_available_with_too_many_arguments(output):
    """Available should raise an error when given too many arguments"""
    # When I have queue with items
    cli = get_cli()
    add_record(cli, ("foo", -10))
    add_record(cli, ("bar", 0))
    add_record(cli, ("baz", 10))

    # And I check for item availablility with too many arguments
    cli.onecmd("available 11 extra_argument")

    # Then I get an error
    output.assert_called_once_with(TooManyArguments('Too many arguments!',))

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from mock import patch
from freezegun import freeze_time
from tests.helpers import get_cli, add_record
from shql.exceptions import TooManyArguments


@freeze_time("2012-01-14 03:21:34")
@patch('shql.shql.print_result')
@patch('shql.shql.get_input')
def test_reschedule_without_confirming(user_input, output):
    """Reschedule should return nothing if the queue is empty"""
    # When I have queue with items
    cli = get_cli()
    add_record(cli, ("foo", 60))

    # And I don't confirm
    user_input.side_effect = ["No"]

    # Then I don't reschedule
    cli.onecmd("reschedule")
    output.assert_called_once_with("Aborting!")

    # And my queue stays the same
    cli.onecmd("peek")
    output.assert_called_with("foo", "2012-01-14 03:22:34")


@freeze_time("2012-01-14 03:21:34")
@patch('shql.shql.print_result')
@patch('shql.shql.get_input')
def test_reschedule_with_confirming(user_input, output):
    """Reschedule with no args should reschedules all arguments to now"""
    # When I have queue with items
    cli = get_cli()
    add_record(cli, ("foo", 60))
    add_record(cli, ("bar", 600))

    # And I confirm
    user_input.side_effect = ["Yes"]

    # Then I reschedule all items
    cli.onecmd("reschedule")
    output.assert_called_once_with("Rescheduled all items in queue test_shql to current")

    # And my queue is rescheduled to now
    cli.onecmd("exists foo")
    output.assert_called_with(True, "IMMEDIATELY")

    cli.onecmd("exists bar")
    output.assert_called_with(True, "IMMEDIATELY")


@freeze_time("2012-01-14 03:21:34")
@patch('shql.shql.print_result')
@patch('shql.shql.get_input')
def test_reschedule_with_item(user_input, output):
    """Reschedule with an item should reschedule the item to now"""
    # When I have queue with items
    cli = get_cli()
    add_record(cli, ("foo", 60))
    add_record(cli, ("bar", 600))

    # And I confirm
    user_input.side_effect = ["Yes"]

    # And I reschedule one item
    cli.onecmd("reschedule foo")
    output.assert_called_once_with("Rescheduled foo in queue test_shql to 0 seconds from now")

    # And my queue is rescheduled to now
    cli.onecmd("exists foo")
    output.assert_called_with(True, "2012-01-14 03:21:34")

    # And I do not reschedule my other items
    cli.onecmd("exists bar")
    output.assert_called_with(True, "2012-01-14 03:31:34")


@freeze_time("2012-01-14 03:21:34")
@patch('shql.shql.print_result')
@patch('shql.shql.get_input')
def test_reschedule_with_item_and_offset(user_input, output):
    """Reschedule with an item and offset should reschedule the item to offset seconds from now"""
    # When I have queue with items
    cli = get_cli()
    add_record(cli, ("foo", 0))
    add_record(cli, ("bar", 600))

    # And I confirm
    user_input.side_effect = ["Yes"]

    # And I reschedule one item
    cli.onecmd("reschedule foo 60")
    output.assert_called_once_with("Rescheduled foo in queue test_shql to 60 seconds from now")

    # And my queue is rescheduled to now
    cli.onecmd("exists foo")
    output.assert_called_with(True, "2012-01-14 03:22:34")

    # And I do not reschedule my other items
    cli.onecmd("exists bar")
    output.assert_called_with(True, "2012-01-14 03:31:34")


@freeze_time("2012-01-14 03:21:34")
@patch('shql.helpers.print_error')
@patch('shql.shql.get_input')
def test_reschedule_with_too_many_arguments(user_input, output):
    """Reschedule with an more than 3 arguments should raise an error"""
    # When I have queue with items
    cli = get_cli()
    add_record(cli, ("foo", 0))
    add_record(cli, ("bar", 600))

    # And I confirm
    user_input.side_effect = ["Yes"]

    # And I reschedule with too many arguments
    cli.onecmd("reschedule foo 60 extra_argument")

    # Then I get an error
    output.assert_called_once_with(TooManyArguments('Too many arguments!',))


@freeze_time("2012-01-14 03:21:34")
@patch('shql.shql.print_result')
@patch('shql.shql.get_input')
def test_reschedule_with_negative_confirmation(user_input, output):
    """Reschedule with an item should reschedule the item to now"""
    # When I have queue with items
    cli = get_cli()
    add_record(cli, ("foo", 60))
    add_record(cli, ("bar", 600))

    # And I do not confirm
    user_input.side_effect = ["No"]

    # And I reschedule one item
    cli.onecmd("reschedule foo 10")
    output.assert_called_once_with("Aborting!")

    # Then nothing is rescheduled
    cli.onecmd("exists bar")
    output.assert_called_with(True, "2012-01-14 03:31:34")

    cli.onecmd("exists foo")
    output.assert_called_with(True, "2012-01-14 03:22:34")

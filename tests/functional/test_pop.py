# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from mock import patch

from tests.helpers import get_cli, add_record


@patch('shql.shql.print_result')
@patch('shql.shql.get_input')
def test_pop_no(user_input, output):
    """Pop should not remove an item when denied"""
    # When I have queue with items
    cli = get_cli()
    add_record(cli, ("foo", 0))

    # And I do not confirm clearing the queue
    user_input.side_effect = ["No"]

    # Then I do not clear the queue
    cli.onecmd("pop")
    output.assert_called_once_with("Aborting!")

    # And the queue has items
    cli.onecmd("size")
    output.assert_called_with(1)


@patch('shql.shql.print_result')
@patch('shql.shql.get_input')
def test_pop_yes(user_input, output):
    """Pop should remove an item when confirmed"""
    # When I have a queue with items
    cli = get_cli()
    add_record(cli, ("foo", 0))

    # And I confirm clearing the queue
    user_input.side_effect = ["Yes"]

    # Then I remove the item
    cli.onecmd("pop foo")
    output.assert_called_once_with("Removed foo from the queue.")

    # And the queue no items
    cli.onecmd("size")
    output.assert_called_with(0)


@patch('shql.shql.print_result')
@patch('shql.shql.get_input')
def test_pop_with_wrong_item(user_input, output):
    """Pop should remove only the item specified"""
    # When I have a queue with an item
    cli = get_cli()
    add_record(cli, ("foo", 0))

    # And I confirm clearing the queue
    user_input.side_effect = ["Yes"]

    # Then I pop a different item
    cli.onecmd("pop bar")
    output.assert_called_once_with("Removed bar from the queue.")

    # And the queue still has the original item
    cli.onecmd("size")
    output.assert_called_with(1)
